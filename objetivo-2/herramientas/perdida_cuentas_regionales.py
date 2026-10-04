"""Componente experimental OE2. No modifica el motor v1 ni habilita GPU.

Las máscaras se calculan desde la geometría, solo se usan en entrenamiento.
Cada imagen pesa igual; cada familia no vacía pesa igual dentro de la imagen.
Dentro de anomalías, las regiones válidas pesan igual. Se excluyen máscaras
con menos de min_pixels; devolver siempre los conteos de soporte al registro.
"""
import math
import torch

def regional_log_count_loss(z,reference,masks,families,scale,min_pixels=20):
    if z.ndim!=4 or z.shape[1]!=1 or reference.shape!=z.shape:
        raise ValueError('predicción y referencia requieren Bx1xHxW')
    if masks.ndim!=4 or masks.shape[0]!=z.shape[0] or masks.shape[2:]!=z.shape[2:]:
        raise ValueError('máscaras requieren BxRxHxW')
    if masks.dtype!=torch.bool or masks.device!=z.device or reference.device!=z.device:
        raise ValueError('máscaras booleanas y tensores en el mismo dispositivo')
    if len(families)!=masks.shape[1] or any(type(f)!=int or f not in range(4) for f in families):
        raise ValueError('familias 0:cielo, 1:roca, 2:borde, 3:anomalías')
    if not math.isfinite(scale) or scale<=0 or type(min_pixels)!=int or min_pixels<1:
        raise ValueError('escala/soporte inválido')
    if not torch.isfinite(z).all() or torch.any((z<0)|(z>=1)):
        raise ValueError('inversión requiere 0 <= z < 1; no se recorta')
    if not torch.isfinite(reference).all() or torch.any(reference<0):
        raise ValueError('referencia de cuentas finitas no negativas')
    # log(1+media(exp(t)-1)) = logsumexp(t) - log(n).
    # No se forma exp(t): evita desbordamiento sin limitar las cuentas.
    t=scale*z.double()/(1-z.double())
    if not torch.isfinite(t).all():raise ValueError('exponente no finito')
    per_image=[];support=[]
    for b in range(len(z)):
        by_family={};valid=[]
        for r,f in enumerate(families):
            m=masks[b,r];n=int(m.sum())
            if n<min_pixels:continue
            log_prediction=torch.logsumexp(t[b,0][m],dim=0)-math.log(n)
            log_reference=torch.log1p(reference[b,0][m].double().mean())
            by_family.setdefault(f,[]).append(torch.abs(log_prediction-log_reference))
            valid.append(r)
        if not by_family:raise ValueError('imagen sin regiones con soporte')
        per_image.append(torch.stack([torch.stack(v).mean() for v in by_family.values()]).mean())
        support.append({'valid_regions':valid,'valid_families':sorted(by_family),'family_losses':{str(f):float(torch.stack(v).mean().detach()) for f,v in by_family.items()}})
    value=torch.stack(per_image).mean()
    if not torch.isfinite(value):raise ValueError('pérdida regional no finita')
    return value,support

def combined_loss(z,target,reference,masks,families,scale,weight=1.):
    if not math.isfinite(weight) or weight<0:raise ValueError('peso inválido')
    if z.shape!=target.shape or not torch.isfinite(target).all():raise ValueError('objetivo inválido')
    l1=torch.nn.functional.l1_loss(z,target)
    regional,support=regional_log_count_loss(z,reference,masks,families,scale)
    return 100*l1+weight*regional,{'l1':l1,'regional':regional,'support':support}

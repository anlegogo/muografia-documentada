"""Candidato experimental E1: error absoluto de cuentas en el borde.
No está integrado en el entrenamiento ni habilita una ejecución GPU.
"""
import math
import torch
def spatial_edge_count_loss(z, reference, edge_masks, scale, min_pixels=20):
    if z.ndim!=4 or z.shape[1]!=1 or reference.shape!=z.shape or edge_masks.shape!=z.shape:
        raise ValueError('Se requieren Bx1xHxW coincidentes')
    if len(z)==0 or edge_masks.dtype!=torch.bool or reference.device!=z.device or edge_masks.device!=z.device:
        raise ValueError('Lote no vacío, máscara booleana y dispositivo común')
    if not math.isfinite(scale) or scale<=0 or type(min_pixels)!=int or min_pixels<1:
        raise ValueError('Escala o soporte inválido')
    if not torch.isfinite(z).all() or torch.any((z<0)|(z>=1)):
        raise ValueError('Salida fuera de 0 <= z < 1')
    if not torch.isfinite(reference).all() or torch.any(reference<0):
        raise ValueError('Referencia inválida')
    values=[]
    for b in range(len(z)):
        m=edge_masks[b,0]
        if int(m.sum())<min_pixels:raise ValueError('Borde con soporte insuficiente')
        ref=reference[b,0][m].double()
        denominator=ref.sum()
        if denominator<=0:raise ValueError('Referencia de borde vacía; no se añaden pseudocuentas')
        selected=z[b,0][m].double()
        exponent=scale*selected/(1-selected)
        if not torch.isfinite(exponent).all() or torch.any(exponent>math.log(torch.finfo(torch.float64).max)-1):
            raise ValueError('Inversión no finita')
        values.append(torch.abs(torch.expm1(exponent)-ref).sum()/denominator)
    result=torch.stack(values).mean()
    if not torch.isfinite(result):raise ValueError('Pérdida no finita')
    return result


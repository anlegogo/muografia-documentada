"""CG-04c: derivación separada y suma ordenada del gradiente del crítico."""
import torch
from losses import critic_score, gradient_penalty

GRADIENT_POLICY = 'wasserstein-then-weighted-gp-v1'

def critic_components(critic, cond, real, fake, lambda_gp):
    """Conserva puntuación, forwards, muestra alpha y pérdida del diseño."""
    d_real = critic_score(critic, cond, real).mean()
    d_fake = critic_score(critic, cond, fake).mean()
    gp = gradient_penalty(critic, cond, real, fake)
    wasserstein = d_fake - d_real
    penalty = lambda_gp * gp
    parts = {'d_real': float(d_real.detach()), 'd_fake': float(d_fake.detach()),
             'w_est': float((d_real - d_fake).detach()), 'gp': float(gp.detach())}
    return wasserstein, penalty, parts

def separated_critic_step(wasserstein, penalty, critic, optimizer):
    """Sustituye .grad; suma W + GP una vez y aplica un único paso Adam.

    Los grafos W y GP comparten hojas, pero no resultados intermedios.
    Un parámetro sin contribución GP (p. ej. sesgo de salida) aporta cero.
    Toda contribución W debe existir. No se derivan parámetros de G.
    """
    if not torch.isfinite(wasserstein) or not torch.isfinite(penalty) or not torch.isfinite(wasserstein + penalty):
        raise ValueError('Pérdida no finita')
    params = tuple(critic.parameters())
    gw = torch.autograd.grad(wasserstein, params, allow_unused=False)
    gp = torch.autograd.grad(penalty, params, allow_unused=True)
    gradients = []
    for w, p in zip(gw, gp):
        if not torch.isfinite(w).all() or (p is not None and not torch.isfinite(p).all()):
            raise ValueError('Gradiente no finito')
        combined = w if p is None else w + p
        if not torch.isfinite(combined).all():
            raise ValueError('Gradiente combinado no finito')
        gradients.append(combined.detach())
    # Ningún paso se aplica antes de comprobar todas las contribuciones.
    norm2 = sum(float(g.double().square().sum()) for g in gradients)
    for param, grad in zip(params, gradients):
        param.grad = grad
    optimizer.step()
    if any(not torch.isfinite(p).all() for p in params):
        raise ValueError('Parámetro no finito')
    return norm2 ** .5

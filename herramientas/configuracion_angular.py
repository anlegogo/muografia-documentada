"""Contrato técnico de configuración; no certifica el modelo físico."""
import json
import math


def recipe(meta):
    controls = meta.get('oe1_controles')
    reference = meta.get('reference_histogram')
    if 'oe1_controles' in meta or 'reference_histogram' in meta:
        if not isinstance(controls, dict) or not isinstance(reference, str) or not reference.strip():
            raise ValueError('configuración controlada requiere oe1_controles y reference_histogram')
        if controls.get('inject') not in ('legacy', 'edifice', 'cone'):
            raise ValueError('inyección desconocida')
        for key in ('plane_half_m', 'edifice_margin_m', 'margin_deg'):
            value = controls.get(key)
            if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
                raise ValueError('opción de control inválida: '+key)
            if key == 'plane_half_m' and value == 0:
                raise ValueError('plano de conteo nulo')
        for key in ('ecuts_gev', 'subplanes_half_m'):
            values = controls.get(key)
            if not isinstance(values, list) or any(type(x) not in (int, float) or not math.isfinite(x)
                                                   or x < 0 for x in values):
                raise ValueError('lista de controles inválida: '+key)
            if len(set(values)) != len(values):
                raise ValueError('controles repetidos: '+key)
    result = {'oe1_controles': controls, 'reference_histogram': reference}
    # Reserved explicit definitions: absent is distinct from an agreed definition.
    for key in ('source_definition', 'normalization'):
        value = meta.get(key)
        if key in meta and (not isinstance(value, dict) or not value):
            raise ValueError('definición vacía o inválida: '+key)
        result[key] = value
    json.dumps(result, allow_nan=False)
    return result


def configuration(meta):
    keys = ('grid', 'engine', 'sampling', 'physics_note', 'detector', 'exposure_days')
    result = {k: meta[k] for k in keys}
    for key in ('engine', 'sampling', 'physics_note'):
        if not isinstance(result[key], str) or not result[key].strip():
            raise ValueError('configuración vacía: '+key)
    detector = result['detector']
    if not isinstance(detector, dict):
        raise ValueError('detector inválido')
    for key in ('side_m', 'distance_m', 'height_m'):
        value = detector.get(key)
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0 or (key != 'height_m' and value == 0):
            raise ValueError('detector inválido: '+key)
    result.update(recipe(meta))
    # Reject non-finite values, including nested future fields.
    json.dumps(result, allow_nan=False)
    return result

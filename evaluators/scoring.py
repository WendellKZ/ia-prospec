def calcular_score(fit_cnae: float, tem_site: bool, indice_mes: float):
    # score entre 0 e 1
    base = 0.4*float(fit_cnae) + 0.2*(1.0 if tem_site else 0.0) + 0.4*(float(indice_mes)/100.0)
    base = max(0.0, min(1.0, base))
    p30 = round(base * 0.65, 3)
    p90 = round(min(1.0, base + 0.15), 3)
    return round(base, 3), p30, p90

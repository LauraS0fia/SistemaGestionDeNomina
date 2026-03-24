#logica de la nomina 

class Constantes:
    SMLV = 1_423_500
    auxilio_transporte = 200_000
    hSemanales = 46 / 6          # horas diarias promedio
 
    # Recargos horas extras
    eDiurnas       = 1.25
    eNocturnas     = 1.75
    eDiaFestivas   = 2.00
    eNochFestivas  = 2.50
 
    # Aportes empleado
    porcentajeSaludEmpleado   = 0.04
    porcentajePensionEmpleado = 0.04
 
    # Niveles ARL → porcentaje
    arlPorcentajes = {
        1: 0.0052,
        2: 0.0104,
        3: 0.0244,
        4: 0.0435,
        5: 0.0696,
    }
 
 
def calcular_nomina(datos: dict) -> dict:
    """
    Recibe los datos crudos del empleado y devuelve un dict
    con todos los valores calculados listos para guardar en MongoDB.
 
    Parámetros esperados en `datos`:
        nombre       str
        Sbasico      float   – sueldo básico mensual
        Dias         int     – días trabajados (máx 30)
        nivel_arl    int     – nivel de riesgo ARL (1-5)
        HED          float   – horas extra diurnas
        HEN          float   – horas extra nocturnas
        HEDF         float   – horas extra festivas diurnas
        HENF         float   – horas extra festivas nocturnas
    """
    nombre    = datos["nombre"]
    sbasico   = float(datos["Sbasico"])
    dias      = int(datos["Dias"])
    nivel_arl = int(datos["nivel_arl"])
    hed       = float(datos.get("HED",  0) or 0)
    hen       = float(datos.get("HEN",  0) or 0)
    hedf      = float(datos.get("HEDF", 0) or 0)
    henf      = float(datos.get("HENF", 0) or 0)
 
    # 1. Sueldo proporcional a días trabajados
    sueldo = (sbasico / 30) * dias
 
    # 2. Valor hora base
    valor_hora = (sbasico / 30) / Constantes.hSemanales
 
    # 3. Horas extras
    horas_extra = (
        valor_hora * hed  * Constantes.eDiurnas      +
        valor_hora * hen  * Constantes.eNocturnas    +
        valor_hora * hedf * Constantes.eDiaFestivas  +
        valor_hora * henf * Constantes.eNochFestivas
    )
 
    # 4. Auxilio de transporte (solo si sbasico < 2 SMLV)
    auxilio = Constantes.auxilio_transporte if sbasico < Constantes.SMLV * 2 else 0
 
    # 5. Total devengado
    devengado = sueldo + horas_extra + auxilio
 
    # 6. Base para deducciones (excluye auxilio de transporte)
    base_deducciones = devengado - auxilio
 
    # 7. Deducciones empleado
    salud      = base_deducciones * Constantes.porcentajeSaludEmpleado
    pension    = base_deducciones * Constantes.porcentajePensionEmpleado
    deducciones = salud + pension
 
    # 8. Neto a pagar
    neto = devengado - deducciones
 
    # 9. ARL (costo empleador, se guarda como info)
    porcentaje_arl = Constantes.arlPorcentajes.get(nivel_arl, 0)
    arl = base_deducciones * porcentaje_arl
 
    return {
        # Inputs originales (para poder editar después)
        "nombre":    nombre,
        "Sbasico":   sbasico,
        "Dias":      dias,
        "nivel_arl": nivel_arl,
        "HED":       hed,
        "HEN":       hen,
        "HEDF":      hedf,
        "HENF":      henf,
        # Resultados calculados
        "sueldo":      round(sueldo,      2),
        "horas_extra": round(horas_extra, 2),
        "auxilio":     round(auxilio,     2),
        "devengado":   round(devengado,   2),
        "salud":       round(salud,       2),
        "pension":     round(pension,     2),
        "deducciones": round(deducciones, 2),
        "neto":        round(neto,        2),
        "arl":         round(arl,         2),
    }
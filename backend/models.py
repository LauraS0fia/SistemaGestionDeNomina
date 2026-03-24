#clases empleado , constantes, sistemanomina = calculo y logica 
# ──────────────────────────────────────────────
#  models.py  –  Esquemas Pydantic
# ──────────────────────────────────────────────
from pydantic import BaseModel, Field
from typing import Optional


class EmpleadoInput(BaseModel):
    """Datos que llegan desde el formulario del frontend."""
    nombre:    str
    Sbasico:   float = Field(..., gt=0, description="Sueldo básico mensual")
    Dias:      int   = Field(..., ge=1, le=30, description="Días trabajados")
    nivel_arl: int   = Field(..., ge=1, le=5,  description="Nivel de riesgo ARL")
    HED:       float = Field(0, ge=0, description="Horas extra diurnas")
    HEN:       float = Field(0, ge=0, description="Horas extra nocturnas")
    HEDF:      float = Field(0, ge=0, description="Horas extra festivas diurnas")
    HENF:      float = Field(0, ge=0, description="Horas extra festivas nocturnas")


class EmpleadoResponse(BaseModel):
    """Lo que devuelve la API al frontend (inputs + resultados calculados)."""
    id:        str

    # Inputs
    nombre:    str
    Sbasico:   float
    Dias:      int
    nivel_arl: int
    HED:       float
    HEN:       float
    HEDF:      float
    HENF:      float

    # Calculados
    sueldo:      float
    horas_extra: float
    auxilio:     float
    devengado:   float
    salud:       float
    pension:     float
    deducciones: float
    neto:        float
    arl:         float
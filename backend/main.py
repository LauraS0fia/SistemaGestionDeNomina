#API con endpoints
# ──────────────────────────────────────────────
#  main.py  –  API FastAPI + MongoDB
# ──────────────────────────────────────────────
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
 
from database import empleados_col
from models import EmpleadoInput, EmpleadoResponse
from calculos import calcular_nomina
 
app = FastAPI(title="Sistema de Nómina API")
 
# ── CORS (permite que el frontend en otro puerto consuma la API) ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # en producción reemplaza por la URL exacta del frontend
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
# ── Helper: convierte documento Mongo → dict serializable ──────────
def doc_to_dict(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc
 
 
# ══════════════════════════════════════════════
#  GET /api/users  –  Listar todos los empleados
# ══════════════════════════════════════════════
@app.get("/api/users", response_model=list[EmpleadoResponse])
async def get_users():
    empleados = []
    async for doc in empleados_col.find():
        empleados.append(doc_to_dict(doc))
    return empleados
 
 
# ══════════════════════════════════════════════
#  POST /api/users  –  Crear empleado
# ══════════════════════════════════════════════
@app.post("/api/users", response_model=EmpleadoResponse, status_code=201)
async def create_user(empleado: EmpleadoInput):
    # Calcula nómina y arma el documento completo
    datos = calcular_nomina(empleado.model_dump())
 
    result = await empleados_col.insert_one(datos)
    doc    = await empleados_col.find_one({"_id": result.inserted_id})
    return doc_to_dict(doc)
 
 
# ══════════════════════════════════════════════
#  PUT /api/users/{id}  –  Actualizar empleado
# ══════════════════════════════════════════════
@app.put("/api/users/{id}", response_model=EmpleadoResponse)
async def update_user(id: str, empleado: EmpleadoInput):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
 
    # Recalcula con los nuevos datos
    datos = calcular_nomina(empleado.model_dump())
 
    result = await empleados_col.update_one(
        {"_id": ObjectId(id)},
        {"$set": datos}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
 
    doc = await empleados_col.find_one({"_id": ObjectId(id)})
    return doc_to_dict(doc)
 
 
# ══════════════════════════════════════════════
#  DELETE /api/users/{id}  –  Eliminar empleado
# ══════════════════════════════════════════════
@app.delete("/api/users/{id}", status_code=204)
async def delete_user(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
 
    result = await empleados_col.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
 
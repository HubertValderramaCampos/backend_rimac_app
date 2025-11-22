from pydantic import BaseModel, Field
from typing import Optional, List


class MedicineSearchRequest(BaseModel):
    """Request model para búsqueda de medicamentos"""
    nombre_medicamento: str = Field(..., description="Nombre del medicamento a buscar", min_length=1)
    departamento: str = Field(default="LIMA", description="Departamento donde buscar")
    provincia: str = Field(default="LIMA", description="Provincia donde buscar")
    distrito: str = Field(default="PUENTE PIEDRA", description="Distrito donde buscar")
    limite_resultados: int = Field(default=10, description="Número máximo de resultados a devolver", ge=1, le=50)

    class Config:
        json_schema_extra = {
            "example": {
                "nombre_medicamento": "APRONAX",
                "departamento": "LIMA",
                "provincia": "LIMA",
                "distrito": "PUENTE PIEDRA",
                "limite_resultados": 10
            }
        }


class MedicineResult(BaseModel):
    """Modelo para un resultado individual de medicamento"""
    tipo_establecimiento: str = Field(..., description="Tipo de establecimiento (Privado/Público)")
    fecha_actualizacion: str = Field(..., description="Fecha de última actualización")
    producto: str = Field(..., description="Nombre completo del producto")
    laboratorio: str = Field(..., description="Nombre del laboratorio fabricante")
    farmacia_botica: str = Field(..., description="Nombre de la farmacia o botica")
    precio_unitario: float = Field(..., description="Precio unitario en soles")
    nombre_comercial: str = Field(default="", description="Nombre comercial de la farmacia")
    direccion: str = Field(default="", description="Dirección de la farmacia")
    telefono: str = Field(default="", description="Teléfono de la farmacia")
    departamento_farmacia: str = Field(default="", description="Departamento donde está la farmacia")
    provincia_farmacia: str = Field(default="", description="Provincia donde está la farmacia")

    class Config:
        json_schema_extra = {
            "example": {
                "tipo_establecimiento": "Privado",
                "fecha_actualizacion": "23/10/2025 07:44:00 PM",
                "producto": "NAPROXENO SODICO 550 mg Tableta Recubierta x 100 unid.",
                "laboratorio": "MEDROCK CORPORATION SOCIEDAD ANONIMA CERRADA",
                "farmacia_botica": "INKAFARMA",
                "precio_unitario": 0.23,
                "nombre_comercial": "FARMACIA CRUZYPHARMA",
                "direccion": "CAL. PORTUGAL 1205",
                "telefono": "958012014",
                "departamento_farmacia": "LA LIBERTAD",
                "provincia_farmacia": "TRUJILLO"
            }
        }


class MedicineSearchResponse(BaseModel):
    """Response model para búsqueda de medicamentos"""
    success: bool = Field(..., description="Indica si la búsqueda fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    total_encontrados: int = Field(..., description="Total de resultados encontrados")
    resultados: List[MedicineResult] = Field(default=[], description="Lista de medicamentos encontrados")
    error: Optional[str] = Field(default=None, description="Mensaje de error si ocurrió alguno")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Búsqueda completada exitosamente",
                "total_encontrados": 10,
                "resultados": [
                    {
                        "tipo_establecimiento": "Privado",
                        "fecha_actualizacion": "23/10/2025 07:44:00 PM",
                        "producto": "NAPROXENO SODICO 550 mg Tableta Recubierta x 100 unid.",
                        "laboratorio": "MEDROCK CORPORATION SOCIEDAD ANONIMA CERRADA",
                        "farmacia_botica": "INKAFARMA",
                        "precio_unitario": 0.23
                    }
                ],
                "error": None
            }
        }


class UberRideRequest(BaseModel):
    """Request model para cotización de viaje en Uber"""
    pickup_location: str = Field(..., description="Lugar de recogida", min_length=1)
    destination: str = Field(..., description="Destino del viaje", min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "pickup_location": "Plaza de Armas, Lima",
                "destination": "Aeropuerto Jorge Chávez, Lima"
            }
        }


class RideOption(BaseModel):
    """Modelo para una opción de viaje"""
    tipo_viaje: str = Field(..., description="Tipo de viaje (UberX, Uber Pet, etc.)")
    precio: str = Field(..., description="Precio del viaje")
    tiempo_espera: str = Field(default="", description="Tiempo estimado de espera")

    class Config:
        json_schema_extra = {
            "example": {
                "tipo_viaje": "UberX",
                "precio": "27,90 PEN",
                "tiempo_espera": "3 min"
            }
        }


class UberRideResponse(BaseModel):
    """Response model para cotización de viaje en Uber"""
    success: bool = Field(..., description="Indica si la cotización fue exitosa")
    pickup: Optional[str] = Field(default=None, description="Lugar de recogida")
    destination: Optional[str] = Field(default=None, description="Destino")
    total_opciones: int = Field(default=0, description="Total de opciones de viaje encontradas")
    resultados: List[RideOption] = Field(default=[], description="Lista de opciones de viaje disponibles")
    error: Optional[str] = Field(default=None, description="Mensaje de error si ocurrió alguno")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "pickup": "Plaza de Armas, Lima",
                "destination": "Aeropuerto Jorge Chávez, Lima",
                "total_opciones": 4,
                "resultados": [
                    {
                        "tipo_viaje": "UberX",
                        "precio": "27,90 PEN",
                        "tiempo_espera": "3 min"
                    },
                    {
                        "tipo_viaje": "Uber Pet",
                        "precio": "32,50 PEN",
                        "tiempo_espera": "5 min"
                    }
                ],
                "error": None
            }
        }

"""
Main API Module

This module contains the FastAPI application and all the API route definitions.
The data reading logic is handled by the services.sav_reader module.
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
import os
from sqlalchemy.orm import Session

from services.sav_reader import SAVReader, SAVReaderError, QuestionNotFoundError
from services.database import get_db, init_db
from services.profile_service import (
    ProfileService,
    ProfileNotFoundError,
    ProfileAlreadyExistsError
)

app = FastAPI()

# Initialize the database on startup
@app.on_event("startup")
def startup_event():
    """Initialize the database when the application starts."""
    init_db()


class RangoEdad(BaseModel):
    """Model for age range filter with min and max values."""
    min: Optional[int] = None
    max: Optional[int] = None


class FiltrosRequest(BaseModel):
    """
    Model for filter request body.
    
    Attributes:
        calidad_vida: Quality of life level (1="1-2", 2="3", 3="4-5")
        municipio: Municipality (1="El Salto", 2="Guadalajara", 3="San Pedro Tlaquepaque",
                                4="Tlajomulco de Zúñiga", 5="Tonalá", 6="Zapopan")
        sexo: Gender (1="Hombre", 2="Mujer")
        edad: Age filter - can be a range with min/max
        escolaridad: Education level (1="Sec<", 2="Prep", 3="Univ+")
        nse: Socioeconomic level (1="D+/D/E", 2="C/C-", 3="A/B/C+", 4="SIN DATOS SUFICIENTES")
    """
    calidad_vida: Optional[int] = None
    municipio: Optional[int] = None
    sexo: Optional[int] = None
    edad: Optional[RangoEdad] = None
    escolaridad: Optional[int] = None
    nse: Optional[int] = None

# Path to the data file
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "datos.sav")

# Initialize the SAV reader service
sav_reader = SAVReader(DATA_FILE_PATH)


class TipoRespuesta(str, Enum):
    cantidad = "cantidad"
    porcentaje = "porcentaje"


@app.get("/")
def welcome():
    return {"message": "Bienvenido a la API"}


@app.get("/preguntas")
def get_preguntas():
    """
    Endpoint that opens datos.sav and returns all questions in JSON format.
    
    Returns for each question:
    - identificador: The variable identifier (e.g., Q_1, T_Q_12_1)
    - pregunta: The question text
    - opciones: List of possible answer options
    """
    try:
        preguntas = sav_reader.load_preguntas()
        return {"preguntas": preguntas}
    except SAVReaderError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/respuestas/{question_id}")
def get_respuestas(
    question_id: str,
    tipo: TipoRespuesta = Query(
        default=TipoRespuesta.cantidad,
        description="Tipo de respuesta: 'cantidad' para conteo o 'porcentaje' para porcentaje"
    )
):
    """
    Endpoint that returns the responses for a specific question.
    
    Parameters:
    - question_id: The question identifier (e.g., Q_1, T_Q_12_1)
    - tipo: Type of response - 'cantidad' (count) or 'porcentaje' (percentage)
    
    Returns:
    - identificador: The question identifier
    - pregunta: The question text
    - tipo_respuesta: The type of response (cantidad or porcentaje)
    - respuestas: List of responses with value, label, and count/percentage
    - total_respuestas: Total number of valid responses (excludes NaN values)
    """
    try:
        return sav_reader.get_question_responses(question_id, tipo.value)
    except QuestionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SAVReaderError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/respuestas/{question_id}/filtros")
def get_respuestas_con_filtros(
    question_id: str,
    filtros: FiltrosRequest,
    tipo: TipoRespuesta = Query(
        default=TipoRespuesta.cantidad,
        description="Tipo de respuesta: 'cantidad' para conteo o 'porcentaje' para porcentaje"
    )
):
    """
    Endpoint that returns the responses for a specific question with filters applied.
    
    Parameters:
    - question_id: The question identifier (e.g., Q_1, T_Q_12_1)
    - tipo: Type of response - 'cantidad' (count) or 'porcentaje' (percentage)
    - filtros: JSON body with filter criteria
    
    Filter options (all optional):
    - calidad_vida: 1 (1-2 baja), 2 (3 media), 3 (4-5 alta)
    - municipio: 1 (El Salto), 2 (Guadalajara), 3 (San Pedro Tlaquepaque),
                 4 (Tlajomulco de Zúñiga), 5 (Tonalá), 6 (Zapopan)
    - sexo: 1 (Hombre), 2 (Mujer)
    - edad: {"min": 18, "max": 35} - Filter by actual age range
    - escolaridad: 1 (Sec<), 2 (Prep), 3 (Univ+)
    - nse: 1 (D+/D/E), 2 (C/C-), 3 (A/B/C+), 4 (SIN DATOS SUFICIENTES)
    
    Returns:
    - identificador: The question identifier
    - pregunta: The question text
    - tipo_respuesta: The type of response (cantidad or porcentaje)
    - respuestas: List of responses with value, label, and count/percentage
    - total_respuestas: Total number of valid responses after filtering
    - filtros_aplicados: Dictionary of filters that were applied
    """
    try:
        # Convert Pydantic model to dict, excluding None values
        filtros_dict = filtros.model_dump(exclude_none=True)
        
        # Handle nested edad model
        if "edad" in filtros_dict and isinstance(filtros_dict["edad"], dict):
            # Remove empty edad dict if both min and max are None
            if not filtros_dict["edad"]:
                del filtros_dict["edad"]
        
        return sav_reader.get_question_responses_with_filters(
            question_id, tipo.value, filtros_dict
        )
    except QuestionNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SAVReaderError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Profile Models
class PerfilBase(BaseModel):
    """Base model for profile data."""
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None


class PerfilCreate(PerfilBase):
    """Model for creating a new profile."""
    pass


class PerfilUpdate(BaseModel):
    """Model for updating a profile. All fields are optional."""
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None


class PerfilResponse(PerfilBase):
    """Model for profile response with ID."""
    id: int

    class Config:
        from_attributes = True


# Profile Endpoints
@app.post("/perfil", response_model=PerfilResponse, status_code=201)
def crear_perfil(perfil: PerfilCreate, db: Session = Depends(get_db)):
    """
    Create a new user profile.
    
    Parameters:
    - nombre: User's name (required)
    - email: User's email address (required, must be unique)
    - telefono: User's phone number (optional)
    
    Returns:
    - The created profile with its ID
    """
    try:
        user = ProfileService.create_profile(
            db=db,
            nombre=perfil.nombre,
            email=perfil.email,
            telefono=perfil.telefono
        )
        return user
    except ProfileAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/perfil/{user_id}", response_model=PerfilResponse)
def obtener_perfil(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user profile by ID.
    
    Parameters:
    - user_id: The ID of the user
    
    Returns:
    - The user profile data
    """
    try:
        user = ProfileService.get_profile(db=db, user_id=user_id)
        return user
    except ProfileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/perfiles", response_model=list[PerfilResponse])
def listar_perfiles(
    skip: int = Query(default=0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(default=100, ge=1, le=100, description="Número máximo de registros"),
    db: Session = Depends(get_db)
):
    """
    List all user profiles with pagination.
    
    Parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum number of records to return (default: 100, max: 100)
    
    Returns:
    - List of user profiles
    """
    users = ProfileService.get_all_profiles(db=db, skip=skip, limit=limit)
    return users


@app.put("/perfil/{user_id}", response_model=PerfilResponse)
def actualizar_perfil(
    user_id: int,
    perfil: PerfilUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing user profile.
    
    Parameters:
    - user_id: The ID of the user to update
    - nombre: New name (optional)
    - email: New email address (optional, must be unique)
    - telefono: New phone number (optional)
    
    Returns:
    - The updated profile data
    """
    try:
        user = ProfileService.update_profile(
            db=db,
            user_id=user_id,
            nombre=perfil.nombre,
            email=perfil.email,
            telefono=perfil.telefono
        )
        return user
    except ProfileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ProfileAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/perfil/{user_id}")
def eliminar_perfil(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user profile.
    
    Parameters:
    - user_id: The ID of the user to delete
    
    Returns:
    - Confirmation message
    """
    try:
        ProfileService.delete_profile(db=db, user_id=user_id)
        return {"message": f"Usuario con ID {user_id} eliminado correctamente"}
    except ProfileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

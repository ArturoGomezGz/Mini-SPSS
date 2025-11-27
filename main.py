"""
Main API Module

This module contains the FastAPI application and all the API route definitions.
The data reading logic is handled by the services.sav_reader module.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from enum import Enum
import os

from services.sav_reader import SAVReader, SAVReaderError, QuestionNotFoundError
from services.categories import get_all_categories, get_category_by_id

app = FastAPI()


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
    - categoria: The category the question belongs to (id, nombre, descripcion)
    - opciones: List of possible answer options
    """
    try:
        preguntas = sav_reader.load_preguntas()
        return {"preguntas": preguntas}
    except SAVReaderError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/categorias")
def get_categorias():
    """
    Endpoint that returns all available question categories.
    
    Returns:
    - categorias: List of categories with:
        - id: Unique category identifier
        - nombre: Category name
        - descripcion: Brief description of the category
    """
    categorias = get_all_categories()
    return {"categorias": categorias}


@app.get("/preguntas/categoria/{categoria_id}")
def get_preguntas_por_categoria(categoria_id: int):
    """
    Endpoint that returns questions filtered by category.
    
    Parameters:
    - categoria_id: The category identifier (1-17)
    
    Returns for each question:
    - identificador: The variable identifier (e.g., Q_1, T_Q_12_1)
    - pregunta: The question text
    - categoria: The category the question belongs to (id, nombre, descripcion)
    - opciones: List of possible answer options
    
    Raises:
    - 404: If category_id does not exist
    """
    # Validate that the category exists
    categoria = get_category_by_id(categoria_id)
    if categoria is None:
        raise HTTPException(
            status_code=404,
            detail=f"Categoría con id {categoria_id} no encontrada"
        )
    
    try:
        preguntas = sav_reader.load_preguntas(categoria_id=categoria_id)
        return {
            "categoria": categoria,
            "preguntas": preguntas
        }
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

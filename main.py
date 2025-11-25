"""
Main API Module

This module contains the FastAPI application and all the API route definitions.
The data reading logic is handled by the services.sav_reader module.
"""

from fastapi import FastAPI, HTTPException, Query
from enum import Enum
import os

from services.sav_reader import SAVReader, SAVReaderError, QuestionNotFoundError

app = FastAPI()

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

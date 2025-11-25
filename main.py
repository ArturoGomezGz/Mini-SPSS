from fastapi import FastAPI, HTTPException, Query
from enum import Enum
import pyreadstat
import os

app = FastAPI()

# Path to the data file
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "datos.sav")

# Cache for the loaded data
_cached_preguntas = None
_cached_data = None


class TipoRespuesta(str, Enum):
    cantidad = "cantidad"
    porcentaje = "porcentaje"


def _load_data():
    """Load and cache the dataframe and metadata from the SAV file."""
    global _cached_data
    
    if _cached_data is not None:
        return _cached_data
    
    if not os.path.exists(DATA_FILE_PATH):
        raise HTTPException(status_code=404, detail=f"Data file not found: {DATA_FILE_PATH}")
    
    try:
        df, meta = pyreadstat.read_sav(DATA_FILE_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading data file: {str(e)}")
    
    _cached_data = (df, meta)
    return _cached_data


def _load_preguntas():
    """Load and parse questions from the SAV file."""
    global _cached_preguntas
    
    if _cached_preguntas is not None:
        return _cached_preguntas
    
    df, meta = _load_data()
    
    # Get column labels (questions) and value labels (answer options)
    column_labels = meta.column_names_to_labels if meta.column_names_to_labels else {}
    value_labels = meta.variable_value_labels if meta.variable_value_labels else {}
    
    preguntas = []
    
    for column in df.columns:
        # Only include columns that have a label (question text)
        if column in column_labels and column_labels[column]:
            pregunta_info = {
                "identificador": column,
                "pregunta": column_labels[column],
                "opciones": []
            }
            
            # Add answer options if available
            if column in value_labels:
                for valor, etiqueta in value_labels[column].items():
                    pregunta_info["opciones"].append({
                        "valor": valor,
                        "etiqueta": etiqueta
                    })
            
            preguntas.append(pregunta_info)
    
    _cached_preguntas = preguntas
    return preguntas


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
    preguntas = _load_preguntas()
    return {"preguntas": preguntas}


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
    df, meta = _load_data()
    
    # Check if the question exists
    if question_id not in df.columns:
        raise HTTPException(
            status_code=404, 
            detail=f"Pregunta '{question_id}' no encontrada"
        )
    
    # Get question label
    column_labels = meta.column_names_to_labels if meta.column_names_to_labels else {}
    pregunta_texto = column_labels.get(question_id, question_id)
    
    # Get value labels for the question
    value_labels = meta.variable_value_labels if meta.variable_value_labels else {}
    question_value_labels = value_labels.get(question_id, {})
    
    # Count responses (excluding NaN values)
    value_counts = df[question_id].dropna().value_counts()
    total_respuestas = int(value_counts.sum())
    
    # Build response list
    respuestas = []
    for valor, cantidad in value_counts.items():
        etiqueta = question_value_labels.get(valor, str(valor))
        
        if tipo == TipoRespuesta.porcentaje:
            valor_respuesta = round((cantidad / total_respuestas) * 100, 2) if total_respuestas > 0 else 0
        else:
            valor_respuesta = int(cantidad)
        
        respuestas.append({
            "valor": valor,
            "etiqueta": etiqueta,
            tipo.value: valor_respuesta
        })
    
    # Sort by value for consistent ordering
    respuestas.sort(key=lambda x: x["valor"])
    
    return {
        "identificador": question_id,
        "pregunta": pregunta_texto,
        "tipo_respuesta": tipo.value,
        "respuestas": respuestas,
        "total_respuestas": total_respuestas
    }

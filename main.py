from fastapi import FastAPI, HTTPException
import pyreadstat
import os

app = FastAPI()

# Path to the data file
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "datos.sav")

# Cache for the loaded data
_cached_preguntas = None


def _load_preguntas():
    """Load and parse questions from the SAV file."""
    global _cached_preguntas
    
    if _cached_preguntas is not None:
        return _cached_preguntas
    
    if not os.path.exists(DATA_FILE_PATH):
        raise HTTPException(status_code=404, detail=f"Data file not found: {DATA_FILE_PATH}")
    
    try:
        df, meta = pyreadstat.read_sav(DATA_FILE_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading data file: {str(e)}")
    
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

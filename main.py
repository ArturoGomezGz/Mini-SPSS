from fastapi import FastAPI
import pyreadstat
import pandas as pd
import os

app = FastAPI()

# Path to the data file
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "datos.sav")


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
    # Read the SAV file with metadata
    df, meta = pyreadstat.read_sav(DATA_FILE_PATH)
    
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
                opciones = []
                for valor, etiqueta in value_labels[column].items():
                    opciones.append({
                        "valor": valor,
                        "etiqueta": etiqueta
                    })
                pregunta_info["opciones"] = opciones
            
            preguntas.append(pregunta_info)
    
    return {"preguntas": preguntas}

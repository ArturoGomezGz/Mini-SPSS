"""
SAV Reader Service Module

This module handles all the logic for reading and extracting data from SPSS .sav files.
It provides functions for loading data, caching, and parsing questions and responses.
"""

import os
import re
from typing import Any, Optional, Tuple
import pyreadstat


# Category mapping based on question identifier patterns
# Categories as defined in the survey structure documentation
CATEGORY_MAPPING = [
    # Metadata variables
    (["SbjNum", "Date", "Duration"], "Metadatos"),
    # Quality of Life and Satisfaction (Q_1 - Q_11)
    (r"^Q_([1-9]|1[01])(_S)?$", "Calidad de Vida y Satisfacción"),
    # Public Services (T_Q_12_1 - T_Q_13_6)
    (r"^T_Q_1[23]_\d+$", "Servicios Públicos"),
    # Government and Public Administration (Q_14 - Q_22)
    (r"^Q_(1[4-9]|2[0-2])(_S)?$", "Gobierno y Administración Pública"),
    # Mobility and Transportation (Q_23 - Q_32, T_Q_25 - T_Q_30)
    (r"^Q_(2[3-9]|3[0-2])(_O\d+)?(_S)?(_C)?$", "Movilidad y Transporte"),
    (r"^T_Q_(2[5-9]|30)_\d+$", "Movilidad y Transporte"),
    # Urban Infrastructure (Q_33 - Q_43, T_Q_36 - T_Q_43)
    (r"^Q_(3[3-9]|4[0-3])(_O\d+)?(_C)?$", "Infraestructura Urbana"),
    (r"^T_Q_(3[6-9]|4[0-3])_\d+$", "Infraestructura Urbana"),
    # Road Safety (Q_44 - Q_48)
    (r"^Q_4[4-8](_O\d+)?$", "Seguridad Vial"),
    # Public Safety and Crime (Q_49 - Q_55)
    (r"^Q_(49|5[0-5])$", "Seguridad Pública y Delincuencia"),
    # Violence and Coexistence (Q_56 - Q_66, T_Q_58 - T_Q_66)
    (r"^Q_(5[6-9]|6[0-6])$", "Violencia y Convivencia"),
    (r"^T_Q_(5[89]|6[0-6])_\d+$", "Violencia y Convivencia"),
    # Citizen Participation (Q_67 - Q_68, T_Q_68)
    (r"^Q_6[78](_O\d+)?$", "Participación Ciudadana"),
    (r"^T_Q_68_\d+$", "Participación Ciudadana"),
    # Media and Democracy (Q_69 - Q_73, T_Q_72 - T_Q_73)
    (r"^Q_(69|7[0-3])$", "Medios de Comunicación y Democracia"),
    (r"^T_Q_7[23]_\d+$", "Medios de Comunicación y Democracia"),
    # Sociodemographic Data (Q_74 - Q_98, T_Q_80 - T_Q_98)
    (r"^Q_(7[4-9]|8\d|9[0-8])(_S)?$", "Datos Sociodemográficos"),
    (r"^T_Q_(8[0-9]|9[0-8])_\d+$", "Datos Sociodemográficos"),
    # Derived and Classification Variables
    (["SEXO", "CALIDAD_VIDA", "EDAD", "ESC", "IND_SE2024", "NSE2024", "NSE2024_C", "FACTOR"], 
     "Variables Derivadas y de Clasificación"),
]


def get_category_for_question(identifier: str) -> Optional[str]:
    """
    Get the category for a given question identifier.
    
    Args:
        identifier: The question identifier (e.g., Q_1, T_Q_12_1)
        
    Returns:
        The category name or None if not found
    """
    for pattern, category in CATEGORY_MAPPING:
        if isinstance(pattern, list):
            # Direct match for list of identifiers
            if identifier in pattern:
                return category
        else:
            # Regex match for patterns
            if re.match(pattern, identifier):
                return category
    return None


class SAVReaderError(Exception):
    """Custom exception for SAV reader errors."""
    pass


class QuestionNotFoundError(SAVReaderError):
    """Exception raised when a question is not found in the data."""
    pass


class SAVReader:
    """Class to handle reading and caching of SAV file data."""
    
    def __init__(self, file_path: str):
        """
        Initialize the SAV reader with a file path.
        
        Args:
            file_path: Path to the SAV file
        """
        self._file_path = file_path
        self._cached_data = None
        self._cached_preguntas = None
    
    @property
    def file_path(self) -> str:
        """Return the file path."""
        return self._file_path
    
    def load_data(self) -> Tuple[Any, Any]:
        """
        Load and cache the dataframe and metadata from the SAV file.
        
        Returns:
            Tuple of (DataFrame, metadata)
            
        Raises:
            SAVReaderError: If file not found or error reading the file
        """
        if self._cached_data is not None:
            return self._cached_data
        
        if not os.path.exists(self._file_path):
            raise SAVReaderError(f"Data file not found: {self._file_path}")
        
        try:
            df, meta = pyreadstat.read_sav(self._file_path)
        except Exception as e:
            raise SAVReaderError(f"Error reading data file: {str(e)}")
        
        self._cached_data = (df, meta)
        return self._cached_data
    
    def load_preguntas(self) -> list:
        """
        Load and parse questions from the SAV file.
        
        Returns:
            List of question dictionaries with identificador, pregunta, and opciones
            
        Raises:
            SAVReaderError: If there's an error loading the data
        """
        if self._cached_preguntas is not None:
            return self._cached_preguntas
        
        df, meta = self.load_data()
        
        # Get column labels (questions) and value labels (answer options)
        column_labels = meta.column_names_to_labels if meta.column_names_to_labels else {}
        value_labels = meta.variable_value_labels if meta.variable_value_labels else {}
        
        preguntas = []
        
        for column in df.columns:
            # Only include columns that have a label (question text)
            if column in column_labels and column_labels[column]:
                # Get the category for this question
                categoria = get_category_for_question(column)
                
                pregunta_info = {
                    "identificador": column,
                    "pregunta": column_labels[column],
                    "categoria": categoria,
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
        
        self._cached_preguntas = preguntas
        return preguntas
    
    def get_question_responses(self, question_id: str, tipo: str = "cantidad") -> dict:
        """
        Get the responses for a specific question.
        
        Args:
            question_id: The question identifier (e.g., Q_1, T_Q_12_1)
            tipo: Type of response - 'cantidad' (count) or 'porcentaje' (percentage)
            
        Returns:
            Dictionary with question info and responses
            
        Raises:
            SAVReaderError: If question not found or error loading data
        """
        df, meta = self.load_data()
        
        # Check if the question exists
        if question_id not in df.columns:
            raise QuestionNotFoundError(f"Pregunta '{question_id}' no encontrada")
        
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
            
            if tipo == "porcentaje":
                valor_respuesta = round((cantidad / total_respuestas) * 100, 2) if total_respuestas > 0 else 0
            else:
                valor_respuesta = int(cantidad)
            
            respuestas.append({
                "valor": valor,
                "etiqueta": etiqueta,
                tipo: valor_respuesta
            })
        
        # Sort by value for consistent ordering
        # Use a key function that handles mixed types safely
        respuestas.sort(key=lambda x: (isinstance(x["valor"], str), x["valor"]))
        
        return {
            "identificador": question_id,
            "pregunta": pregunta_texto,
            "tipo_respuesta": tipo,
            "respuestas": respuestas,
            "total_respuestas": total_respuestas
        }
    
    def clear_cache(self):
        """Clear the cached data."""
        self._cached_data = None
        self._cached_preguntas = None

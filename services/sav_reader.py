"""
SAV Reader Service Module

This module handles all the logic for reading and extracting data from SPSS .sav files.
It provides functions for loading data, caching, and parsing questions and responses.
"""

import os
from typing import Any, Tuple
import pyreadstat


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

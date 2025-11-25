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
    
    def _apply_simple_filter(
        self, df, column: str, value, filtros_aplicados: dict, filter_key: str
    ):
        """
        Apply a simple equality filter to the dataframe.
        
        Args:
            df: DataFrame to filter
            column: Column name to filter on
            value: Value to filter for
            filtros_aplicados: Dictionary to record applied filters
            filter_key: Key name for the filter in filtros_aplicados
            
        Returns:
            Filtered DataFrame
        """
        if column in df.columns:
            df = df[df[column] == value]
            filtros_aplicados[filter_key] = value
        return df
    
    def get_question_responses_with_filters(
        self, question_id: str, tipo: str = "cantidad", filtros: dict = None
    ) -> dict:
        """
        Get the responses for a specific question with filters applied.
        
        Args:
            question_id: The question identifier (e.g., Q_1, T_Q_12_1)
            tipo: Type of response - 'cantidad' (count) or 'porcentaje' (percentage)
            filtros: Dictionary with filter criteria:
                - calidad_vida: int (1-3)
                - municipio: int (1-6)
                - sexo: int (1-2)
                - edad: dict with 'min' and/or 'max' keys for age range
                - escolaridad: int (1-3)
                - nse: int (1-4)
            
        Returns:
            Dictionary with question info, filtered responses, and applied filters
            
        Raises:
            SAVReaderError: If question not found or error loading data
        """
        df, meta = self.load_data()
        
        # Check if the question exists
        if question_id not in df.columns:
            raise QuestionNotFoundError(f"Pregunta '{question_id}' no encontrada")
        
        # Apply filters
        filtered_df = df.copy()
        filtros_aplicados = {}
        
        if filtros:
            # Define simple filter mappings: filter_key -> column_name
            simple_filters = {
                "calidad_vida": "CALIDAD_VIDA",
                "municipio": "Q_94",
                "sexo": "SEXO",
                "escolaridad": "ESC",
                "nse": "NSE2024_C"
            }
            
            # Apply simple equality filters
            for filter_key, column_name in simple_filters.items():
                if filter_key in filtros and filtros[filter_key] is not None:
                    filtered_df = self._apply_simple_filter(
                        filtered_df, column_name, filtros[filter_key],
                        filtros_aplicados, filter_key
                    )
            
            # Filter by edad (Q_75 column - actual age in years)
            if "edad" in filtros and filtros["edad"] is not None:
                edad_filter = filtros["edad"]
                if "Q_75" in filtered_df.columns:
                    min_age = edad_filter.get("min")
                    max_age = edad_filter.get("max")
                    
                    # Build condition for age range filter
                    if min_age is not None and max_age is not None:
                        filtered_df = filtered_df[
                            (filtered_df["Q_75"] >= min_age) & 
                            (filtered_df["Q_75"] <= max_age)
                        ]
                    elif min_age is not None:
                        filtered_df = filtered_df[filtered_df["Q_75"] >= min_age]
                    elif max_age is not None:
                        filtered_df = filtered_df[filtered_df["Q_75"] <= max_age]
                    
                    filtros_aplicados["edad"] = edad_filter
        
        # Get question label
        column_labels = meta.column_names_to_labels if meta.column_names_to_labels else {}
        pregunta_texto = column_labels.get(question_id, question_id)
        
        # Get value labels for the question
        value_labels = meta.variable_value_labels if meta.variable_value_labels else {}
        question_value_labels = value_labels.get(question_id, {})
        
        # Count responses (excluding NaN values) from filtered data
        value_counts = filtered_df[question_id].dropna().value_counts()
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
            "total_respuestas": total_respuestas,
            "filtros_aplicados": filtros_aplicados
        }
    
    def clear_cache(self):
        """Clear the cached data."""
        self._cached_data = None
        self._cached_preguntas = None

"""
SAV Reader Service Module

This module handles all the logic for reading and extracting data from SPSS .sav files.
It provides functions for loading data, caching, and parsing questions and responses.
"""

import os
import re
from typing import Any, Tuple, Optional, List
import pyreadstat


# Category definitions with id, name, and description
CATEGORIAS = [
    {
        "id": 1,
        "nombre": "Bienestar subjetivo",
        "descripcion": "Preguntas relacionadas con satisfacción con la vida, calidad de vida y felicidad"
    },
    {
        "id": 2,
        "nombre": "Relaciones interpersonales / Hogar",
        "descripcion": "Preguntas sobre relaciones familiares, con vecinos, amigos y compañeros"
    },
    {
        "id": 3,
        "nombre": "Economía",
        "descripcion": "Preguntas sobre situación económica, ingresos y empleo"
    },
    {
        "id": 4,
        "nombre": "Salud",
        "descripcion": "Preguntas sobre salud física, mental, acceso a servicios de salud y enfermedades"
    },
    {
        "id": 5,
        "nombre": "Educación",
        "descripcion": "Preguntas sobre satisfacción con la educación escolar"
    },
    {
        "id": 6,
        "nombre": "Cultura y recreación",
        "descripcion": "Preguntas sobre uso del tiempo libre y actividades recreativas"
    },
    {
        "id": 7,
        "nombre": "Vivienda",
        "descripcion": "Preguntas sobre satisfacción con la vivienda"
    },
    {
        "id": 8,
        "nombre": "Espacio público y servicios públicos",
        "descripcion": "Preguntas sobre calidad de servicios públicos y espacios públicos en la colonia"
    },
    {
        "id": 9,
        "nombre": "Movilidad",
        "descripcion": "Preguntas sobre transporte, tiempo de traslado y vialidad"
    },
    {
        "id": 10,
        "nombre": "Seguridad",
        "descripcion": "Preguntas sobre percepción de seguridad, delitos y agresiones"
    },
    {
        "id": 11,
        "nombre": "Medio Ambiente",
        "descripcion": "Preguntas sobre calidad del aire, agua, ruido y áreas verdes"
    },
    {
        "id": 12,
        "nombre": "Ciudadanía y Participación",
        "descripcion": "Preguntas sobre participación ciudadana, organizaciones, igualdad y discriminación"
    },
    {
        "id": 13,
        "nombre": "Gobierno y Corrupción",
        "descripcion": "Preguntas sobre confianza en instituciones, gobierno y corrupción"
    },
]


def get_categoria_for_question(identificador: str) -> Optional[dict]:
    """
    Determine the category for a question based on its identifier.
    
    The category mapping is based on question number ranges from the quality of life survey:
    - Bienestar subjetivo: Q1-Q5
    - Relaciones interpersonales / Hogar: Q6-Q13
    - Economía: Q14-Q21
    - Salud: Q22-Q31
    - Educación: Q32
    - Cultura y recreación: Q33-Q34
    - Vivienda: Q35
    - Espacio público y servicios públicos: Q36-Q37
    - Movilidad: Q38-Q43
    - Seguridad: Q44-Q53
    - Medio Ambiente: Q54-Q56, Q60
    - Ciudadanía y Participación: Q57-Q66
    - Gobierno y Corrupción: Q67-Q73
    
    Args:
        identificador: The question identifier (e.g., Q_1, T_Q_12_1)
        
    Returns:
        Category dictionary with id and nombre, or None if no category matches
    """
    # Extract the base question number from the identifier
    # Patterns: Q_1, Q_23_O1, T_Q_12_1, T_Q_25_1, Q_40_C, etc.
    match = re.match(r'^(?:T_)?Q_(\d+)(?:_.*)?$', identificador)
    if not match:
        return None
    
    q_num = int(match.group(1))
    
    # Bienestar subjetivo: Q1-Q5
    if 1 <= q_num <= 5:
        return {"id": 1, "nombre": "Bienestar subjetivo"}
    
    # Relaciones interpersonales / Hogar: Q6-Q13
    if 6 <= q_num <= 13:
        return {"id": 2, "nombre": "Relaciones interpersonales / Hogar"}
    
    # Economía: Q14-Q21
    if 14 <= q_num <= 21:
        return {"id": 3, "nombre": "Economía"}
    
    # Salud: Q22-Q31
    if 22 <= q_num <= 31:
        return {"id": 4, "nombre": "Salud"}
    
    # Educación: Q32
    if q_num == 32:
        return {"id": 5, "nombre": "Educación"}
    
    # Cultura y recreación: Q33-Q34
    if 33 <= q_num <= 34:
        return {"id": 6, "nombre": "Cultura y recreación"}
    
    # Vivienda: Q35
    if q_num == 35:
        return {"id": 7, "nombre": "Vivienda"}
    
    # Espacio público y servicios públicos: Q36-Q37
    if 36 <= q_num <= 37:
        return {"id": 8, "nombre": "Espacio público y servicios públicos"}
    
    # Movilidad: Q38-Q43
    if 38 <= q_num <= 43:
        return {"id": 9, "nombre": "Movilidad"}
    
    # Seguridad: Q44-Q53
    if 44 <= q_num <= 53:
        return {"id": 10, "nombre": "Seguridad"}
    
    # Medio Ambiente: Q54-Q56 and Q60
    if 54 <= q_num <= 56 or q_num == 60:
        return {"id": 11, "nombre": "Medio Ambiente"}
    
    # Ciudadanía y Participación: Q57-Q66
    if 57 <= q_num <= 66:
        return {"id": 12, "nombre": "Ciudadanía y Participación"}
    
    # Gobierno y Corrupción: Q67-Q73
    if 67 <= q_num <= 73:
        return {"id": 13, "nombre": "Gobierno y Corrupción"}
    
    return None


class SAVReaderError(Exception):
    """Custom exception for SAV reader errors."""
    pass


class QuestionNotFoundError(SAVReaderError):
    """Exception raised when a question is not found in the data."""
    pass


class CategoryNotFoundError(SAVReaderError):
    """Exception raised when a category is not found."""
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
            List of question dictionaries with identificador, pregunta, categoria, and opciones
            
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
                # Get category for this question
                categoria = get_categoria_for_question(column)
                
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
    
    def get_categorias(self) -> List[dict]:
        """
        Get all available categories.
        
        Returns:
            List of category dictionaries with id, nombre, and descripcion
        """
        return CATEGORIAS.copy()
    
    def get_categoria_by_id(self, categoria_id: int) -> dict:
        """
        Get a specific category by its ID.
        
        Args:
            categoria_id: The category ID
            
        Returns:
            Category dictionary with id, nombre, and descripcion
            
        Raises:
            CategoryNotFoundError: If category is not found
        """
        for categoria in CATEGORIAS:
            if categoria["id"] == categoria_id:
                return categoria
        raise CategoryNotFoundError(f"Categoría con id '{categoria_id}' no encontrada")
    
    def get_preguntas_by_categoria(self, categoria_id: int) -> list:
        """
        Get all questions for a specific category.
        
        Args:
            categoria_id: The category ID to filter by
            
        Returns:
            List of question dictionaries belonging to the specified category
            
        Raises:
            CategoryNotFoundError: If category is not found
        """
        # Verify category exists
        self.get_categoria_by_id(categoria_id)
        
        preguntas = self.load_preguntas()
        return [
            p for p in preguntas 
            if p["categoria"] is not None and p["categoria"]["id"] == categoria_id
        ]
    
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

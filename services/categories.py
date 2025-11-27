"""
Categories Module

This module defines the question categories and provides utilities for mapping
questions to their respective categories.
"""

from typing import Dict, List, Optional


# Category definitions with id, name, and description
CATEGORIES = {
    1: {
        "id": 1,
        "nombre": "Calidad de Vida y Satisfacción",
        "descripcion": "Preguntas sobre satisfacción con la vida, felicidad y relaciones personales"
    },
    2: {
        "id": 2,
        "nombre": "Relaciones Familiares y del Hogar",
        "descripcion": "Preguntas sobre la dinámica familiar y distribución de tareas en el hogar"
    },
    3: {
        "id": 3,
        "nombre": "Situación Económica",
        "descripcion": "Preguntas sobre satisfacción económica, ingresos y empleo"
    },
    4: {
        "id": 4,
        "nombre": "Salud",
        "descripcion": "Preguntas sobre acceso a servicios de salud, bienestar físico y mental"
    },
    5: {
        "id": 5,
        "nombre": "Educación y Tiempo Libre",
        "descripcion": "Preguntas sobre satisfacción educativa y uso del tiempo libre"
    },
    6: {
        "id": 6,
        "nombre": "Vivienda y Servicios Públicos",
        "descripcion": "Preguntas sobre vivienda, servicios públicos y espacios en la colonia"
    },
    7: {
        "id": 7,
        "nombre": "Movilidad y Transporte",
        "descripcion": "Preguntas sobre medios de transporte, tiempos de traslado y transporte público"
    },
    8: {
        "id": 8,
        "nombre": "Seguridad Vial",
        "descripcion": "Preguntas sobre conductas de manejo, accidentes y seguridad vial"
    },
    9: {
        "id": 9,
        "nombre": "Seguridad Pública",
        "descripcion": "Preguntas sobre percepción de seguridad, victimización y delincuencia"
    },
    10: {
        "id": 10,
        "nombre": "Violencia y Agresiones",
        "descripcion": "Preguntas sobre experiencias de violencia, agresiones y acoso"
    },
    11: {
        "id": 11,
        "nombre": "Medio Ambiente",
        "descripcion": "Preguntas sobre calidad del aire, agua y entorno urbano"
    },
    12: {
        "id": 12,
        "nombre": "Participación Ciudadana",
        "descripcion": "Preguntas sobre membresía en organizaciones y formas de participación"
    },
    13: {
        "id": 13,
        "nombre": "Igualdad y Discriminación",
        "descripcion": "Preguntas sobre percepción de igualdad y experiencias de discriminación"
    },
    14: {
        "id": 14,
        "nombre": "Política y Confianza Institucional",
        "descripcion": "Preguntas sobre interés político, medios de información y confianza en instituciones"
    },
    15: {
        "id": 15,
        "nombre": "Datos Sociodemográficos",
        "descripcion": "Información personal del encuestado: género, edad, escolaridad, ocupación"
    },
    16: {
        "id": 16,
        "nombre": "Características del Hogar",
        "descripcion": "Información sobre la vivienda, equipamiento y composición del hogar"
    },
    17: {
        "id": 17,
        "nombre": "Información de Control",
        "descripcion": "Datos de identificación, ubicación y control de la encuesta"
    }
}


# Question to category mapping
# Maps question identifiers to their category id
QUESTION_CATEGORY_MAP: Dict[str, int] = {
    # Category 1: Calidad de Vida y Satisfacción (Q_1 - Q_11)
    "Q_1": 1, "Q_2": 1, "Q_3": 1, "Q_4": 1, "Q_4_S": 1, "Q_5": 1,
    "Q_6": 1, "Q_7": 1, "Q_8": 1, "Q_9": 1, "Q_10": 1, "Q_11": 1,
    
    # Category 2: Relaciones Familiares y del Hogar (T_Q_12, T_Q_13)
    "T_Q_12_1": 2, "T_Q_12_2": 2, "T_Q_12_3": 2, "T_Q_12_4": 2, "T_Q_12_5": 2,
    "T_Q_13_1": 2, "T_Q_13_2": 2, "T_Q_13_3": 2, "T_Q_13_4": 2, "T_Q_13_5": 2, "T_Q_13_6": 2,
    
    # Category 3: Situación Económica (Q_14 - Q_21)
    "Q_14": 3, "Q_15": 3, "Q_16": 3, "Q_17": 3, "Q_18": 3, "Q_19": 3, "Q_20": 3, "Q_21": 3,
    
    # Category 4: Salud (Q_22 - T_Q_30, Q_31)
    "Q_22": 4,
    "Q_23_O1": 4, "Q_23_O2": 4, "Q_23_O3": 4, "Q_23_O4": 4, "Q_23_O5": 4,
    "Q_23_O6": 4, "Q_23_O7": 4, "Q_23_O8": 4, "Q_23_O9": 4,
    "Q_24": 4, "Q_24_S": 4,
    "T_Q_25_1": 4, "T_Q_25_2": 4, "T_Q_25_3": 4, "T_Q_25_4": 4, "T_Q_25_5": 4, "T_Q_25_6": 4,
    "T_Q_26_1": 4, "T_Q_26_2": 4, "T_Q_26_3": 4, "T_Q_26_4": 4, "T_Q_26_5": 4, "T_Q_26_6": 4,
    "T_Q_27_1": 4, "T_Q_27_2": 4, "T_Q_27_3": 4, "T_Q_27_4": 4, "T_Q_27_5": 4, "T_Q_27_6": 4,
    "T_Q_28_1": 4, "T_Q_28_2": 4, "T_Q_28_3": 4, "T_Q_28_4": 4, "T_Q_28_5": 4,
    "T_Q_28_6": 4, "T_Q_28_7": 4, "T_Q_28_8": 4, "T_Q_28_9": 4,
    "T_Q_29_1": 4, "T_Q_29_2": 4,
    "T_Q_30_1": 4, "T_Q_30_2": 4, "T_Q_30_3": 4, "T_Q_30_4": 4, "T_Q_30_5": 4, "T_Q_30_6": 4,
    "Q_31": 4,
    
    # Category 5: Educación y Tiempo Libre (Q_32 - Q_34)
    "Q_32": 5, "Q_33": 5,
    "Q_34_O1": 5, "Q_34_O2": 5, "Q_34_O3": 5, "Q_34_O4": 5, "Q_34_O5": 5,
    "Q_34_O6": 5, "Q_34_O7": 5, "Q_34_O8": 5, "Q_34_O9": 5, "Q_34_O10": 5,
    "Q_34_O11": 5, "Q_34_O12": 5, "Q_34_O13": 5, "Q_34_O14": 5,
    
    # Category 6: Vivienda y Servicios Públicos (Q_35 - T_Q_37)
    "Q_35": 6,
    "T_Q_36_1": 6, "T_Q_36_2": 6, "T_Q_36_3": 6, "T_Q_36_4": 6, "T_Q_36_5": 6, "T_Q_36_6": 6,
    "T_Q_37_1": 6, "T_Q_37_2": 6, "T_Q_37_3": 6, "T_Q_37_4": 6, "T_Q_37_5": 6, "T_Q_37_6": 6, "T_Q_37_7": 6,
    
    # Category 7: Movilidad y Transporte (Q_38 - T_Q_43)
    "Q_38": 7,
    "T_Q_39_1": 7, "T_Q_39_2": 7, "T_Q_39_3": 7, "T_Q_39_4": 7, "T_Q_39_5": 7, "T_Q_39_6": 7,
    "Q_40": 7, "Q_40_C": 7, "Q_41": 7, "Q_42": 7, "Q_42_C": 7,
    "T_Q_43_1": 7, "T_Q_43_2": 7, "T_Q_43_3": 7, "T_Q_43_4": 7, "T_Q_43_5": 7, "T_Q_43_6": 7, "T_Q_43_7": 7,
    
    # Category 8: Seguridad Vial (Q_44 - Q_48)
    "Q_44": 8, "Q_45": 8,
    "Q_46_O1": 8, "Q_46_O2": 8, "Q_46_O3": 8, "Q_46_O4": 8, "Q_46_O5": 8, "Q_46_O6": 8,
    "Q_47": 8, "Q_48": 8,
    
    # Category 9: Seguridad Pública (Q_49 - Q_57)
    "Q_49": 9, "Q_50": 9, "Q_51": 9, "Q_52": 9, "Q_53": 9, "Q_54": 9, "Q_55": 9, "Q_56": 9, "Q_57": 9,
    
    # Category 10: Violencia y Agresiones (T_Q_58, T_Q_59)
    "T_Q_58_1": 10, "T_Q_58_2": 10, "T_Q_58_3": 10, "T_Q_58_4": 10,
    "T_Q_59_1": 10, "T_Q_59_2": 10, "T_Q_59_3": 10,
    
    # Category 11: Medio Ambiente (T_Q_60)
    "T_Q_60_1": 11, "T_Q_60_2": 11, "T_Q_60_3": 11, "T_Q_60_4": 11, "T_Q_60_5": 11,
    
    # Category 12: Participación Ciudadana (T_Q_61, T_Q_66, Q_67)
    "T_Q_61_1": 12, "T_Q_61_2": 12, "T_Q_61_3": 12, "T_Q_61_4": 12, "T_Q_61_5": 12,
    "T_Q_66_1": 12, "T_Q_66_2": 12, "T_Q_66_3": 12, "T_Q_66_4": 12, "T_Q_66_5": 12, "T_Q_66_6": 12, "T_Q_66_7": 12,
    "Q_67_O1": 12, "Q_67_O2": 12, "Q_67_O3": 12, "Q_67_O4": 12, "Q_67_O5": 12, "Q_67_O6": 12, "Q_67_O7": 12, "Q_67_O8": 12,
    
    # Category 13: Igualdad y Discriminación (Q_62, T_Q_63, T_Q_68)
    "Q_62": 13,
    "T_Q_63_1": 13, "T_Q_63_2": 13, "T_Q_63_3": 13, "T_Q_63_4": 13, "T_Q_63_5": 13,
    "T_Q_63_6": 13, "T_Q_63_7": 13, "T_Q_63_8": 13, "T_Q_63_9": 13, "T_Q_63_10": 13, "T_Q_63_11": 13,
    "T_Q_68_1": 13, "T_Q_68_2": 13, "T_Q_68_3": 13, "T_Q_68_4": 13,
    
    # Category 14: Política y Confianza Institucional (T_Q_64, T_Q_65, Q_69-Q_71, T_Q_72, T_Q_73)
    "T_Q_64_1": 14, "T_Q_64_2": 14, "T_Q_64_3": 14,
    "T_Q_65_1": 14, "T_Q_65_2": 14, "T_Q_65_3": 14, "T_Q_65_4": 14,
    "Q_69": 14, "Q_70": 14, "Q_71": 14,
    "T_Q_72_1": 14, "T_Q_72_2": 14, "T_Q_72_3": 14, "T_Q_72_4": 14, "T_Q_72_5": 14, "T_Q_72_6": 14,
    "T_Q_72_7": 14, "T_Q_72_8": 14, "T_Q_72_9": 14, "T_Q_72_10": 14, "T_Q_72_11": 14, "T_Q_72_12": 14,
    "T_Q_73_1": 14, "T_Q_73_2": 14,
    
    # Category 15: Datos Sociodemográficos (Q_74 - Q_79)
    "Q_74": 15, "Q_74_S": 15, "Q_75": 15, "Q_76": 15, "Q_77": 15, "Q_78": 15, "Q_79": 15,
    
    # Category 16: Características del Hogar (T_Q_80 - Q_90)
    "T_Q_80_1": 16, "T_Q_80_2": 16, "T_Q_80_3": 16,
    "Q_81": 16, "Q_82": 16,
    "T_Q_83_1": 16, "T_Q_83_2": 16,
    "T_Q_84_1": 16, "T_Q_84_2": 16,
    "Q_85": 16, "Q_86": 16, "Q_87": 16, "Q_88": 16, "Q_89": 16, "Q_90": 16,
    
    # Category 17: Información de Control (SbjNum, Date, Duration, Q_91 - T_Q_98, derived variables)
    "SbjNum": 17, "Date": 17, "Duration": 17,
    "Q_91": 17,
    "T_Q_92_1": 17, "T_Q_92_2": 17, "T_Q_92_3": 17,
    "Q_94": 17, "Q_95": 17, "Q_96": 17,
    "T_Q_98_1": 17, "T_Q_98_2": 17, "T_Q_98_3": 17, "T_Q_98_4": 17, "T_Q_98_5": 17, "T_Q_98_6": 17,
    "SEXO": 17, "CALIDAD_VIDA": 17, "EDAD": 17, "ESC": 17,
    "IND_SE2024": 17, "NSE2024": 17, "NSE2024_C": 17, "FACTOR": 17,
}


def get_all_categories() -> List[Dict]:
    """
    Get all available categories.
    
    Returns:
        List of category dictionaries with id, nombre, and descripcion
    """
    return list(CATEGORIES.values())


def get_category_by_id(category_id: int) -> Optional[Dict]:
    """
    Get a category by its id.
    
    Args:
        category_id: The category id to look up
        
    Returns:
        Category dictionary or None if not found
    """
    return CATEGORIES.get(category_id)


def get_category_for_question(question_id: str) -> Optional[Dict]:
    """
    Get the category for a given question identifier.
    
    Args:
        question_id: The question identifier (e.g., Q_1, T_Q_12_1)
        
    Returns:
        Category dictionary or None if question not mapped to a category
    """
    category_id = QUESTION_CATEGORY_MAP.get(question_id)
    if category_id is not None:
        return CATEGORIES.get(category_id)
    return None


def get_category_id_for_question(question_id: str) -> Optional[int]:
    """
    Get the category id for a given question identifier.
    
    Args:
        question_id: The question identifier (e.g., Q_1, T_Q_12_1)
        
    Returns:
        Category id or None if question not mapped to a category
    """
    return QUESTION_CATEGORY_MAP.get(question_id)


def get_questions_by_category(category_id: int) -> List[str]:
    """
    Get all question identifiers that belong to a category.
    
    Args:
        category_id: The category id to filter by
        
    Returns:
        List of question identifiers
    """
    return [q_id for q_id, cat_id in QUESTION_CATEGORY_MAP.items() if cat_id == category_id]

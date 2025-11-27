"""
User Profile Model

This module defines the User model for storing user profile data.
"""

from sqlalchemy import Column, Integer, String
from services.database import Base


class User(Base):
    """
    User profile model for storing user information.
    
    Attributes:
        id: Unique identifier for the user
        nombre: User's name
        email: User's email address
        telefono: User's phone number (optional)
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    telefono = Column(String(20), nullable=True)

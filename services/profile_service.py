"""
Profile Service Module

This module handles all database operations related to user profiles.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from services.models import User


class ProfileError(Exception):
    """Custom exception for profile service errors."""
    pass


class ProfileNotFoundError(ProfileError):
    """Exception raised when a profile is not found."""
    pass


class ProfileAlreadyExistsError(ProfileError):
    """Exception raised when trying to create a profile with an existing email."""
    pass


class ProfileService:
    """Service class for handling user profile operations."""

    @staticmethod
    def create_profile(
        db: Session,
        nombre: str,
        email: str,
        telefono: Optional[str] = None
    ) -> User:
        """
        Create a new user profile.
        
        Args:
            db: Database session
            nombre: User's name
            email: User's email address
            telefono: User's phone number (optional)
            
        Returns:
            The created User object
            
        Raises:
            ProfileAlreadyExistsError: If a user with the email already exists
        """
        db_user = User(nombre=nombre, email=email, telefono=telefono)
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            raise ProfileAlreadyExistsError(
                f"Un usuario con el email '{email}' ya existe"
            )

    @staticmethod
    def get_profile(db: Session, user_id: int) -> User:
        """
        Get a user profile by ID.
        
        Args:
            db: Database session
            user_id: The user's ID
            
        Returns:
            The User object
            
        Raises:
            ProfileNotFoundError: If the user is not found
        """
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise ProfileNotFoundError(f"Usuario con ID {user_id} no encontrado")
        return user

    @staticmethod
    def get_profile_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get a user profile by email.
        
        Args:
            db: Database session
            email: The user's email
            
        Returns:
            The User object or None if not found
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_all_profiles(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Get all user profiles with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of User objects
        """
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_profile(
        db: Session,
        user_id: int,
        nombre: Optional[str] = None,
        email: Optional[str] = None,
        telefono: Optional[str] = None
    ) -> User:
        """
        Update an existing user profile.
        
        Args:
            db: Database session
            user_id: The user's ID
            nombre: New name (optional)
            email: New email (optional)
            telefono: New phone number (optional)
            
        Returns:
            The updated User object
            
        Raises:
            ProfileNotFoundError: If the user is not found
            ProfileAlreadyExistsError: If the new email already exists
        """
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise ProfileNotFoundError(f"Usuario con ID {user_id} no encontrado")
        
        if nombre is not None:
            user.nombre = nombre
        if email is not None and email != user.email:
            # Check if email already exists
            existing = db.query(User).filter(User.email == email).first()
            if existing:
                raise ProfileAlreadyExistsError(
                    f"Un usuario con el email '{email}' ya existe"
                )
            user.email = email
        if telefono is not None:
            user.telefono = telefono
        
        try:
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            raise ProfileAlreadyExistsError(
                f"Un usuario con el email '{email}' ya existe"
            )

    @staticmethod
    def delete_profile(db: Session, user_id: int) -> bool:
        """
        Delete a user profile.
        
        Args:
            db: Database session
            user_id: The user's ID
            
        Returns:
            True if deleted successfully
            
        Raises:
            ProfileNotFoundError: If the user is not found
        """
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise ProfileNotFoundError(f"Usuario con ID {user_id} no encontrado")
        
        db.delete(user)
        db.commit()
        return True

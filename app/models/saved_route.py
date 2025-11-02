"""
SavedRoute model for user route management.

This module defines the SavedRoute table for storing user's saved transit routes.
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class SavedRoute(Base):
    """
    SavedRoute model for storing user's saved transit routes.

    Attributes:
        id: Primary key, auto-incrementing integer
        user_id: Foreign key to users table
        name: Name of the saved route
        origin: Origin stop/location
        destination: Destination stop/location
        route_types: Preferred route types (comma-separated)
        notes: Optional notes about the route
        is_favorite: Whether this is a favorite route
        is_active: Whether the route is active/enabled
        created_at: Timestamp when the route was created
        updated_at: Timestamp when the route was last updated

    Example:
        >>> route = SavedRoute(
        ...     user_id=1,
        ...     name="Home to Work",
        ...     origin="Times Sq-42 St",
        ...     destination="Grand Central-42 St",
        ...     route_types="subway,bus"
        ... )
        >>> db.add(route)
        >>> db.commit()
    """

    # Table name
    __tablename__ = "saved_routes"

    # Primary key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Unique route identifier",
    )

    # Foreign key to users
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Owner of this saved route",
    )

    # Route Details
    name = Column(
        String(255),
        nullable=False,
        comment="Name for this saved route",
    )

    origin = Column(
        String(255),
        nullable=False,
        comment="Origin stop or location",
    )

    destination = Column(
        String(255),
        nullable=False,
        comment="Destination stop or location",
    )

    route_types = Column(
        String(100),
        nullable=True,
        comment="Preferred route types (comma-separated: subway,bus)",
    )

    notes = Column(
        Text,
        nullable=True,
        comment="Optional notes about the route",
    )

    # Status Fields
    is_favorite = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether this is a favorite route",
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether the route is active/enabled",
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Timestamp when the route was created",
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Timestamp when the route was last updated",
    )

    # Relationship
    user = relationship("User", backref="saved_routes")

    def __repr__(self) -> str:
        """
        String representation of the SavedRoute object.

        Returns:
            String representation
        """
        return (
            f"<SavedRoute(id={self.id}, name='{self.name}', "
            f"origin='{self.origin}', destination='{self.destination}')>"
        )

    def to_dict(self) -> dict:
        """
        Convert SavedRoute object to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "origin": self.origin,
            "destination": self.destination,
            "route_types": self.route_types,
            "notes": self.notes,
            "is_favorite": self.is_favorite,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

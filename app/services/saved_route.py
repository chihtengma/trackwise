"""
Saved route service - Business logic for saved route operations.

This module contains all business logic related to saved route management,
including CRUD operations and user preferences.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ResourceNotFoundError, AuthorizationError
from app.models.saved_route import SavedRoute
from app.schemas.saved_route import SavedRouteCreate, SavedRouteUpdate


class SavedRouteService:
    """
    Service class for saved route operations.

    Handles all business logic for route management including
    creating, reading, updating, and deleting saved routes.
    """

    @staticmethod
    async def get_route_by_id(
        db: AsyncSession, route_id: int, user_id: int
    ) -> Optional[SavedRoute]:
        """
        Get a saved route by ID for a specific user.

        Args:
            db: Async database session
            route_id: The route's unique identifier
            user_id: The user's ID

        Returns:
            SavedRoute object if found and owned by user, None otherwise

        Example:
            >>> route = await SavedRouteService.get_route_by_id(db, 1, user_id=1)
            >>> if route:
            ...     print(route.name)
        """
        result = await db.execute(
            select(SavedRoute).where(
                SavedRoute.id == route_id, SavedRoute.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_routes_by_user(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        favorites_only: bool = False,
    ) -> List[SavedRoute]:
        """
        Get all saved routes for a user.

        Args:
            db: Async database session
            user_id: The user's ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            favorites_only: If True, only return favorite routes

        Returns:
            List of SavedRoute objects

        Example:
            >>> routes = await SavedRouteService.get_routes_by_user(db, user_id=1)
            >>> print(f"User has {len(routes)} saved routes")
        """
        query = select(SavedRoute).where(SavedRoute.user_id == user_id)
        if favorites_only:
            query = query.where(SavedRoute.is_favorite == True)

        query = query.order_by(
            SavedRoute.is_favorite.desc(), SavedRoute.created_at.desc()
        )
        query = query.offset(skip).limit(limit)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def create_route(
        db: AsyncSession, route_data: SavedRouteCreate, user_id: int
    ) -> SavedRoute:
        """
        Create a new saved route.

        Args:
            db: Async database session
            route_data: SavedRouteCreate schema with route information
            user_id: The user's ID who owns this route

        Returns:
            Newly created SavedRoute object

        Example:
            >>> route_data = SavedRouteCreate(
            ...     name="Home to Work",
            ...     origin="Times Sq-42 St",
            ...     destination="Grand Central-42 St",
            ...     is_favorite=True
            ... )
            >>> route = await SavedRouteService.create_route(db, route_data, user_id=1)
        """
        db_route = SavedRoute(
            user_id=user_id,
            name=route_data.name,
            origin=route_data.origin,
            destination=route_data.destination,
            route_types=route_data.route_types,
            notes=route_data.notes,
            is_favorite=route_data.is_favorite,
        )

        db.add(db_route)
        await db.commit()
        await db.refresh(db_route)

        return db_route

    @staticmethod
    async def update_route(
        db: AsyncSession,
        route_id: int,
        route_data: SavedRouteUpdate,
        user_id: int,
    ) -> SavedRoute:
        """
        Update a saved route.

        Args:
            db: Async database session
            route_id: The route's unique identifier
            route_data: SavedRouteUpdate schema with updated fields
            user_id: The user's ID who owns this route

        Returns:
            Updated SavedRoute object

        Raises:
            ResourceNotFoundError: If route not found
            AuthorizationError: If user doesn't own this route

        Example:
            >>> route_data = SavedRouteUpdate(name="Updated Route Name")
            >>> route = await SavedRouteService.update_route(db, 1, route_data, user_id=1)
        """
        # Get existing route
        route = await SavedRouteService.get_route_by_id(db, route_id, user_id)
        if not route:
            raise ResourceNotFoundError("Saved route not found", {"route_id": route_id})

        # Update fields
        update_data = route_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(route, field, value)

        await db.commit()
        await db.refresh(route)

        return route

    @staticmethod
    async def delete_route(db: AsyncSession, route_id: int, user_id: int) -> bool:
        """
        Delete a saved route.

        Args:
            db: Async database session
            route_id: The route's unique identifier
            user_id: The user's ID who owns this route

        Returns:
            True if deleted successfully

        Raises:
            ResourceNotFoundError: If route not found

        Example:
            >>> deleted = await SavedRouteService.delete_route(db, 1, user_id=1)
            >>> print(f"Route deleted: {deleted}")
        """
        route = await SavedRouteService.get_route_by_id(db, route_id, user_id)
        if not route:
            raise ResourceNotFoundError("Saved route not found", {"route_id": route_id})

        await db.delete(route)
        await db.commit()

        return True

    @staticmethod
    async def get_favorites_count(db: AsyncSession, user_id: int) -> int:
        """
        Get count of favorite routes for a user.

        Args:
            db: Async database session
            user_id: The user's ID

        Returns:
            Count of favorite routes

        Example:
            >>> count = await SavedRouteService.get_favorites_count(db, user_id=1)
            >>> print(f"User has {count} favorite routes")
        """
        result = await db.execute(
            select(SavedRoute)
            .where(SavedRoute.user_id == user_id)
            .where(SavedRoute.is_favorite == True)
        )
        return len(list(result.scalars().all()))

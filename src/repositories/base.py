from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ('DatabaseRepository',)


class DatabaseRepository:
    """Base class for all repositories that work with the database."""

    def __init__(self, session: AsyncSession):
        """
        Args:
            session: SQLAlchemy's async session object.
        """
        self._session = session

from collections.abc import AsyncGenerator

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from litestar.plugins.sqlalchemy import (
    SQLAlchemyAsyncConfig,
)

from litestar.exceptions import ClientException
from litestar.status_codes import HTTP_409_CONFLICT

from BaseObject import Base

def get_db_config():
    return SQLAlchemyAsyncConfig(
        connection_string="sqlite+aiosqlite:///todo.sqlite", 
        metadata=Base.metadata,
        create_all=True
    )
    
# provide_transaction is an asynchronous generator function that yields a database session for use in transactions.
async def provide_transaction(db_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
        try:
            async with db_session.begin():
                yield db_session
        except IntegrityError as exc:
            raise ClientException(
                status_code=HTTP_409_CONFLICT,
                detail=str(exc),
            ) from exc
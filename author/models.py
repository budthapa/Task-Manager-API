from litestar.plugins.sqlalchemy import base, repository

from datetime import date

from sqlalchemy.orm import Mapped, relationship

# base.UUIDBase is a base class that includes an id field of type UUID and a created_at field of type datetime,
# which are common fields for all models in the application
class Author(base.UUIDBase):
    __tablename__ = "author"
    name: Mapped[str]
    dob: Mapped[date]
    dod: Mapped[date | None]
    books: Mapped[list["Book"]] = relationship(back_populates="author", lazy="selectin")
    
    
class AuthorRepository(repository.SQLAlchemyAsyncRepository[Author]):
    model_type = Author
    
    
# base.UUIDAuditBase is a base class that includes an id field of type UUID, 
# a created_at field of type datetime, and an updated_at field of type datetime,
class Book(base.UUIDAuditBase):
    __tablename__ = "book"
    title: Mapped[str]
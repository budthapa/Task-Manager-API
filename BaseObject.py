from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Define the base class for SQLAlchemy models
class Base(DeclarativeBase): ...

# @dataclass
# Define the TodoObject model with SQLAlchemy ORM mapping
# __tablename__ specifies the name of the database table that this model corresponds to, which is "todo_items".
# The TodoObject class represents a to-do item with a title, completion status, and an ID.
# Mapped is used to define the type of each field, and mapped_column is used to specify the database column properties for the id field.
# mapped_column is used to define the id field as a primary key that auto-increments, ensuring each to-do item has a unique identifier.
class TodoObject(Base):
    __tablename__ = "todo_items"
    
    title: Mapped[str]
    completed: Mapped[bool] 
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
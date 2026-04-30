# allows for forward references in type hints, so we can reference Person within the Person class definition for the children field
# eg. children: list[Person]
# without this, we would get a NameError because Person is not defined at the time we reference it in the children field
from __future__ import annotations
from dataclasses import dataclass

from typing import Optional

from address.models import Address


@dataclass
class Person:
    id: int
    name: str
    age: int
    email: str
    gender: str
    address: Optional[Address]
    # allows for recursive nesting of Person objects, so a Person can have a list of children who are also Person instances
    children: Optional[list[Person]]



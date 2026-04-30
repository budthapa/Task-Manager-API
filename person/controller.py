from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from litestar import Controller, get, post, put
from litestar.dto import DTOData

from address.models import Address
from person.models import Person
from person.schemas import ReadPersonDTO, WritePersonDTO


class PersonController(Controller):
    path = "/person"

    @get("/{person_id:int}", return_dto=ReadPersonDTO, sync_to_thread=False)
    async def get_person(self, person_id: int) -> Person:
        address = Address(
            id=1,
            street="123 Main St",
            city="Anytown",
            state="Anystate",
            zip_code="12345",
            country="USA",
        )

        child1 = Person(
            id=2,
            name="Jane Doe",
            age=5,
            gender="Female",
            email="child1@example.com",
            address=address,
            children=[],
        )

        child2 = Person(
            id=3,
            name="Bob Doe",
            age=10,
            gender="Male",
            email="child2@example.com",
            address=address,
            children=[],
        )

        return Person(
            id=person_id,
            name="John Doe",
            email="john.doe@example.com",
            age=30,
            gender="Male",
            address=address,
            children=[child1, child2],
        )

    @post("/", dto=WritePersonDTO, return_dto=ReadPersonDTO, sync_to_thread=False)
    async def create_person(self, data: DTOData[Person]) -> Person:
        print(f"Creating person: {data}")

        # In a real application, you would save the person to the database here
        return data.create_instance(id=1, address=None, children=None)
    
    @put("/{person_id:int}", dto=WritePersonDTO, return_dto=ReadPersonDTO, sync_to_thread=False)
    async def update_person(self, person_id: int, data: DTOData[Person]) -> Person:
        print(f"Updating person: {data}")
        
        person = data.create_instance(id=person_id, address=None, children=None)

        return data.update_instance(person)

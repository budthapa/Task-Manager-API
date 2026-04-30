from address.models import Address
from litestar.dto import DataclassDTO, DTOConfig


class ReadAddressDTO(DataclassDTO[Address]):
    # rename zip_code to postal_code in the output but not for the nested address field
    config = DTOConfig(rename_fields={"zip_code": "postal_code"})
    
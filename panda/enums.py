from enum import Enum, unique


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

@unique
class Sex(ExtendedEnum):
    MALE = "Male"
    FEMALE = "Female"
    INTERSEX = "Intersex"
    NON_BINARY = "Non-Binary"
    OTHER = "Other"


@unique
class AddressOwnerType(ExtendedEnum):
    PATIENT = "patient"
    #LOCATION = "location"

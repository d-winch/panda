import datetime
import random

import pytest
from faker import Faker

from panda.enums import AddressOwnerType, Sex
from panda.schemas import AddressCreate, PatientCreate
from panda.util.nhs_validator import is_valid_nhs_number

Faker.seed(0)
fake: Faker = Faker("en-GB")


@pytest.fixture(name="valid_nhs_numbers")
def fixture_valid_nhs_numbers():
    """ Returns a list of valid nhs numbers """
    return [
        '4609571471',
        '4524408592',
        '4959181745',
        '1565022955',
        '6607313191',
        '2469139341',
        '1451773986',
        '0849244285',
        '8663598831',
        '7133568055',
    ]


@pytest.fixture(name="invalid_nhs_numbers")
def fixture_invalid_nhs_numbers():
    """ Returns a list of invalid nhs numbers """
    return [
        '4609571472',
        '4524408593',
        '4959181746',
        '1565022956',
        '6607313192',
        '2469139342',
        '1451773987',
        '0849244286',
        '8663598832',
        '7133568056',
    ]


@pytest.fixture(name="invalid_format_nhs_numbers")
def fixture_invalid_format_nhs_numbers():
    """ Returns a list of badly formatted nhs numbers """
    return [
        ' 4609571471',
        '452 440 8592',
        '495-918-1745',
    ]


def test_patient(valid_nhs_numbers):
    """
    Test patient is valid and instances are as expected
    """
    nhs_number = random.choice(valid_nhs_numbers)
    patient = PatientCreate(
        nhs_number=nhs_number,
        name=fake.name(),
        dob=fake.date_of_birth(),
        sex=fake.enum(Sex),
    )
    assert is_valid_nhs_number(patient.nhs_number)
    assert isinstance(patient.nhs_number, str)
    assert isinstance(patient.name, str)
    assert isinstance(patient.dob, datetime.date)
    assert isinstance(patient.sex, str)
    assert patient.sex in Sex.list()


def test_patient_invalid_nhs_number(invalid_nhs_numbers):
    """
    Test ValueError thrown with an invalid nhs number
    """
    nhs_number = random.choice(invalid_nhs_numbers)
    with pytest.raises(ValueError):
        PatientCreate(
            nhs_number=nhs_number,
            name=fake.name(),
            dob=fake.date_of_birth(),
            sex=fake.enum(Sex),
        )
    assert is_valid_nhs_number(nhs_number) is False


def test_patient_invalid_format_nhs_number(invalid_format_nhs_numbers):
    """
    Test patient with an invalid format nhs number doesn't throw an error
    """
    nhs_number = random.choice(invalid_format_nhs_numbers)
    PatientCreate(
        nhs_number=nhs_number,
        name=fake.name(),
        dob=fake.date_of_birth(),
        sex=fake.enum(Sex),
    )


def test_patient_blank_name(valid_nhs_numbers):
    """
    Test ValueError thrown with a blank name
    """
    nhs_number = random.choice(valid_nhs_numbers)
    with pytest.raises(ValueError):
        PatientCreate(
            nhs_number=nhs_number,
            name="",
            dob=fake.date_of_birth(),
            sex=fake.enum(Sex),
        )


def test_patient_dob_value_when_not_date(valid_nhs_numbers):
    """
    Test ValueError thrown when dob is not a date object
    """
    nhs_number = random.choice(valid_nhs_numbers)
    with pytest.raises(ValueError):
        PatientCreate(
            nhs_number=nhs_number,
            name=fake.name(),
            dob="abc",  # type: ignore
            sex=fake.enum(Sex),
        )


def test_address():
    """
    Test address is valid and instances are as expected
    """
    address = AddressCreate(
        owner_type=fake.enum(AddressOwnerType).value,
        line1=fake.secondary_address(),
        line2=fake.street_address(),
        town=fake.city(),
        county=fake.county(),
        country=fake.current_country_code(),
        postcode=fake.postcode(),
    )
    assert isinstance(address.owner_type, str)
    assert address.owner_type in AddressOwnerType.list()
    assert isinstance(address.line1, str)
    assert isinstance(address.line2, str)
    assert isinstance(address.town, str)
    assert isinstance(address.county, str)
    assert isinstance(address.country, str)
    assert isinstance(address.postcode, str)


def test_address_invalid_postcodes():
    """
    Test address is valid and instances are as expected
    """
    with pytest.raises(ValueError):
        AddressCreate(
            owner_type=fake.enum(AddressOwnerType).value,
            line1=fake.secondary_address(),
            line2=fake.street_address(),
            town=fake.city(),
            county=fake.county(),
            country=fake.current_country_code(),
            postcode="111111",
        )
    with pytest.raises(ValueError):
        AddressCreate(
            owner_type=fake.enum(AddressOwnerType).value,
            line1=fake.secondary_address(),
            line2=fake.street_address(),
            town=fake.city(),
            county=fake.county(),
            country=fake.current_country_code(),
            postcode="TR72SSS",
        )
    with pytest.raises(ValueError):
        AddressCreate(
            owner_type=fake.enum(AddressOwnerType).value,
            line1=fake.secondary_address(),
            line2=fake.street_address(),
            town=fake.city(),
            county=fake.county(),
            country=fake.current_country_code(),
            postcode="TR77S2SS",
        )


def test_address_invalid_postcodes_get_formatted():
    """
    Test valid postcodes with improper fomatting and non-alphanum chars gets parsed
    """
    AddressCreate(
        owner_type=fake.enum(AddressOwnerType).value,
        line1=fake.secondary_address(),
        line2=fake.street_address(),
        town=fake.city(),
        county=fake.county(),
        country=fake.current_country_code(),
        postcode=" TR7 2SS",
    )
    AddressCreate(
        owner_type=fake.enum(AddressOwnerType).value,
        line1=fake.secondary_address(),
        line2=fake.street_address(),
        town=fake.city(),
        county=fake.county(),
        country=fake.current_country_code(),
        postcode=" TR72SS ",
    )
    AddressCreate(
        owner_type=fake.enum(AddressOwnerType).value,
        line1=fake.secondary_address(),
        line2=fake.street_address(),
        town=fake.city(),
        county=fake.county(),
        country=fake.current_country_code(),
        postcode="TR7-2SS",
    )

import pytest

from panda.util.nhs_validator import is_valid_nhs_number


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


def test_valid_nhs_numbers(valid_nhs_numbers):
    """
    Test valid NHS numbers using the validator
    """

    for value in valid_nhs_numbers:
        assert is_valid_nhs_number(value)


def test_invalid_nhs_numbers(invalid_nhs_numbers):
    """
    Test invalid NHS numbers using the validator, checksum digit is +1
    """

    for value in invalid_nhs_numbers:
        assert is_valid_nhs_number(value) is False


def test_invalid_formatted_numbers(invalid_format_nhs_numbers):
    """
    Test that badly formatted numbers return ValueError
    """
    for value in invalid_format_nhs_numbers:
        with pytest.raises(ValueError):
            is_valid_nhs_number(value)


def test_validation_too_short():
    """
    Test that a ValueError is raised with a number too short
    """
    value = '0123456'
    with pytest.raises(ValueError):
        is_valid_nhs_number(value)


def test_validation_too_long():
    """
    Test that a ValueError is raised with a number too long
    """
    value = '12345678900'
    with pytest.raises(ValueError):
        is_valid_nhs_number(value)


def test_validation_alpha():
    """
    Test to ensure validation fails non-numeric values
    """
    value = 'abc4567890'
    with pytest.raises(ValueError):
        is_valid_nhs_number(value)

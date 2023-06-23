"""The current system uses a ten-digit number in '3 3 4' format with the final digit being an error-detecting checksum. Examples given include 987 654 4321.[5]

Currently issued numbers for England, Wales and the Isle of Man are from 400 000 000 to 499 999 999 and 600 000 000 upwards.[4][6] Current numbers in England also include 3xx xxx xxxx.[citation needed] Unavailable number ranges include 320 000 001 to 399 999 999 (allocated to the Northern Irish system[7]) and 010 100 0000 to 311 299 9999 (used for CHI numbers in Scotland[8]). NHS Digital reserves the numbers 999 000 0000 to 999 999 9999 for test purposes; these numbers are valid but are never going to be issued.[9]

The checksum is calculated by multiplying each of the first nine digits by 11 minus its position. Using the number 943 476 5919 as an example:

The first digit is 9. This is multiplied by 10.
The second digit is 4. This is multiplied by 9.
And so on until the ninth digit (1) is multiplied by 2.
The result of this calculation is summed. In this example: 9×10+4×9+3×8+4×7+7*6+6*5+5*4+9*3+1×2 = 299.
The remainder when dividing this number by 11 is calculated, yielding a number in the range 0–10, which would be 2 in this case.
Finally, this number is subtracted from 11 to give the checksum in the range 1–11, in this case 9, which becomes the last digit of the NHS number.
A checksum of 11 is represented by 0 in the final NHS number. If the checksum is 10 then the number is not valid.
"""

from typing import List


def is_valid_nhs_number(nhs_number: str) -> bool:
    if len(nhs_number) != 10 or not nhs_number.isnumeric():
        # [ ] TODO Handle this scenario better
        raise ValueError(
            "The NHS number should be 10 digits with no alpha characters."
        )

    def digits_of(num: str) -> List[int]:
        return [int(d) for d in num]

    digits = digits_of(nhs_number)
    total = 0

    for i, n in zip(digits, range(10, 1, -1)):
        total += i * n

    checksum = 11 - (total % 11)
    return checksum == digits[-1]

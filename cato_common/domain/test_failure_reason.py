from enum import Enum


class TestFailureReason(Enum):
    EXIT_CODE_NON_ZERO = "EXIT_CODE_NON_ZERO"
    REFERENCE_IMAGE_MISSING = "REFERENCE_IMAGE_MISSING"
    OUTPUT_IMAGE_MISSING = "OUTPUT_IMAGE_MISSING"
    REFERENCE_AND_OUTPUT_IMAGE_MISSING = "REFERENCE_AND_OUTPUT_IMAGE_MISSING"
    IMAGES_ARE_NOT_EQUAL = "IMAGES_ARE_NOT_EQUAL"
    TIMED_OUT = "TIMED_OUT"

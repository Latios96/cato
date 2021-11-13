import { TestFailureReasonDto } from "../catoapimodels";

export function getNiceName(failureReason: TestFailureReasonDto): string {
  switch (failureReason) {
    case TestFailureReasonDto.EXIT_CODE_NON_ZERO:
      return "Exit code was non zero";
    case TestFailureReasonDto.IMAGES_ARE_NOT_EQUAL:
      return "Images are not equal";
    case TestFailureReasonDto.OUTPUT_IMAGE_MISSING:
      return "Output image is missing";
    case TestFailureReasonDto.REFERENCE_IMAGE_MISSING:
      return "Reference image is missing";
    case TestFailureReasonDto.REFERENCE_AND_OUTPUT_IMAGE_MISSING:
      return "Reference and output image is missing";
    case TestFailureReasonDto.TIMED_OUT:
      return "Test timed out";
  }
}

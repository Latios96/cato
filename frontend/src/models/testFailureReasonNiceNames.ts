import { TestFailureReason } from "../catoapimodels/catoapimodels";

export function getNiceName(failureReason: TestFailureReason): string {
  switch (failureReason) {
    case TestFailureReason.EXIT_CODE_NON_ZERO:
      return "Exit code was non zero";
    case TestFailureReason.IMAGES_ARE_NOT_EQUAL:
      return "Images are not equal";
    case TestFailureReason.OUTPUT_IMAGE_MISSING:
      return "Output image is missing";
    case TestFailureReason.REFERENCE_IMAGE_MISSING:
      return "Reference image is missing";
    case TestFailureReason.REFERENCE_AND_OUTPUT_IMAGE_MISSING:
      return "Reference and output image is missing";
    case TestFailureReason.TIMED_OUT:
      return "Test timed out";
  }
}

export default interface TestResult {
  id: number;
  suite_result_id: number;
  test_name: string;
  test_identifier: string;
  test_command: string;
  test_variables: object;
  machine_info: object;
  unified_test_status: string;
  seconds: number | null;
  message: string | null;
  image_output: number | null;
  reference_image: number | null;
  started_at: string | null;
  finished_at: string | null;
}

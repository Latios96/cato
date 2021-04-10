Feature: Updating a reference image
  Updating a reference image to a new one (e.g. add a new baseline)

  Scenario: Updating reference image which did not exist before
    Given a cato.json file with tests
    And an output image for a test
    And reference images for other tests
    When I run the update reference image command
    Then the output image should be stored as reference image
    And other reference images should be untouched

  Scenario: Updating reference image which did exist before
    Given a cato.json file with tests
    And an output image for a test
    And reference images for other tests
    And a reference image exists for the test
    When I run the update reference image command
    Then the output image should be stored as reference image
    And other reference images should be untouched

  Scenario: Updating reference to a not existing output file fails
    Given a cato.json file with tests
    And reference images for other tests
    When I run the update reference image command for a not existing test
    Then all reference images should be untouched
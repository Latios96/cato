Feature: Running tests described in a config file
# all tests success
# all tests images not matching
# all tests one test no image output fails


  Scenario: Run all tests the first time should fail because of missing reference images
    Given a cato.json file with tests
    And no reference images for the tests
    When I run the run command
    Then All tests should have been executed
    And A failure message should be printed
    And Failure Messages for missing reference image should be printed
    And the result should be available at the server
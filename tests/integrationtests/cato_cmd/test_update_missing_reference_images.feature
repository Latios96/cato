# Created by Jan at 21.03.2021
Feature: Updating missing reference images
  Updates the reference images for tests without one to the last test output.
  Useful for adding a baseline

  Scenario: Updating missing reference image
    Given a cato.json file with tests
    And no reference image for a test
    And an output image for a test
    And reference images for other tests
    When I run the update missing reference images command
    Then the output image should be stored as reference image
    And other reference images should be untouched
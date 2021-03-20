# Created by Jan at 17.03.2021
Feature: List tests described in a config file

  Scenario: In Folder with cato.json
    Given A folder with a valid cato.json
    And I changed to this folder
    And I run the list-tests command
    Then I should see the test identifiers of the config on the terminal

  Scenario: Path to config
    Given A folder with a valid cato.json
    When I run the list-tests command with the path to the config
    Then I should see the test identifiers of the config on the terminal
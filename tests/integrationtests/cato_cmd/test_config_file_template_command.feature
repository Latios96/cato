Feature: Create a config file template
  As a user I want to easily create a config file template to start writing tests fast

  Scenario: Create a new cato.json in an empty folder
    Given An empty folder
    When I run the config-template command with the folder
    Then a new cato.json should be created based on template

  Scenario: Create a cato.json in a folder with an existing cato.json
    Given a folder with non default cato.json
    When I run the config-template command with the folder
    Then the cato.json should be overriden with template
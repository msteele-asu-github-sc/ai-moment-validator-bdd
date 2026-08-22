Feature: AI Video Moment Validation Pipeline

  Scenario: A valid AI moment payload passes data contract checks
    Given an AI moment payload with ID "m-201" and confidence 0.92
    And a valid video window from 34.5 to 40.0 seconds
    When the QA validation harness parses the payload
    Then the validation check must pass successfully
    And an informational metric is routed to the CloudWatch log stack

  Scenario: An invalid AI moment payload fails due to an out-of-bounds confidence score
    Given an AI moment payload with ID "m-202" and confidence 1.45
    And a valid video window from 10.0 to 15.0 seconds
    When the QA validation harness parses the payload
    Then the validation check must fail
    And a schema validation defect notification is recorded

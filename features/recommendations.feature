Feature: Recommendations Service

Background:
    Given the following recommendations
        | recommendation_id | name      | recommendation_name | recommendation_type |
        | 1                 | cake      | cookie              | CROSS_SELL          |
        | 2                 | Lemon     | Orange              | CROSS_SELL          |
        | 3                 | pineapple | Mango               | CROSS_SELL          |
        | 4                 | Water     | Sparkling Water     | UP_SELL             |
        | 5                 | sprite    | Coke                | CROSS_SELL          |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Recommendation Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Recommendation
    When I visit the "Home Page"
    And I set the "name" to "cake"
    And I set the "recommendation_type" to "CROSS_SELL"
    And I set the "recommendation_name" to "cookie"
    And I set the "recommendation_id" to "2"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "name" field should be empty
    And the "recommendation_type" field should be empty
    And the "recommendation_name" field should be empty
    And the "recommendation_id" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "cake" in the "name" field
    And I should see "CROSS_SELL" in the "recommendation_type" field
    And I should see "cookie" in the "recommendation_name" field
    And I should see "2" in the "recommendation_id" field

Scenario: List all recommendations
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "cake" in the results
    And I should see "Lemon" in the results
    And I should see "pineapple" in the results
    And I should see "Water" in the results
    And I should see "sprite" in the results

Scenario: Search for a recommendation by name
    When I visit the "Home Page"
    And I set the "name" to "cake"
    And I press the "Search" button
    Then I should see "cake" in the results
    And I should not see "Lemon" in the results
    And I should not see "pineapple" in the results
    And I should not see "Water" in the results
    And I should not see "sprite" in the results

Scenario: Search for a recommendation by recommendation type
    When I visit the "Home Page"
    And I set the "recommendation_type" to "CROSS_SELL"
    And I press the "Search" button
    Then I should see "cake" in the results
    And I should see "Lemon" in the results
    And I should see "pineapple" in the results
    And I should not see "Water" in the results
    And I should see "sprite" in the results

Scenario: Search for a recommendation by recommendation name
    When I visit the "Home Page"
    And I set the "recommendation_name" to "cookie"
    And I press the "Search" button
    Then I should see "cake" in the results
    And I should not see "Lemon" in the results
    And I should not see "pineapple" in the results
    And I should not see "Water" in the results
    And I should not see "sprite" in the results

Scenario: Search for a recommendation by recommendation ID
    When I visit the "Home Page"
    And I set the "recommendation_id" to "1"
    And I press the "Search" button
    Then I should see "cake" in the results
    And I should not see "Lemon" in the results
    And I should not see "pineapple" in the results
    And I should not see "Water" in the results
    And I should not see "sprite" in the results
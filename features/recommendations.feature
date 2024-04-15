Feature: Recommendations Service

Background:
    Given the following recommendations
        | product_id | product_name | recommendation_name | recommendation_id  | recommendation_type |
        | 1          | cake         | cookie              | 123                | CROSS_SELL          |
        | 2          | Lemon        | Orange              | 321                | CROSS_SELL          |
        | 3          | pineapple    | Mango               | 456                | CROSS_SELL          |
        | 4          | Water        | Sparkling Water     | 654                | UP_SELL             |
        | 5          | sprite       | Coke                | 111                | CROSS_SELL          | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Recommendation Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Recommendation
    When I visit the "Home Page"
    And I set the "product_name" to "cake"
    And I select "CROSS_SELL" in the "recommendation_type" dropdown
    And I set the "recommendation_name" to "cookie"
    And I set the "recommendation_id" to "123"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "product_id" field
    And I press the "Clear" button
    Then the "product_id" field should be empty
    And the "product_name" field should be empty
    And the "recommendation_type" field should be empty
    And the "recommendation_name" field should be empty
    And the "recommendation_id" field should be empty
    When I paste the "product_id" field
    And I press the "Retrieve" button
    Then I should see "cake" in the "product_name" field
    And I should see "CROSS_SELL" in the "recommendation_type" field
    And I should see "cookie" in the "recommendation_name" field
    And I should see "2" in the "recommendation_id" field

Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "cake" in the results
    And I should see "Lemon" in the results
    And I should see "pineapple" in the results
    And I should see "Water" in the results
    And I should see "sprite" in the results

Scenario: Search for a recommendation by name
    When I visit the "Home Page"
    And I set the "product_name" to "cake"
    And I press the "Search" button
    Then I should see "cake" in the results
    And I should not see "Lemon" in the results
    And I should not see "pineapple" in the results
    And I should not see "Water" in the results
    And I should not see "sprite" in the results

Scenario: Search for a recommendation by recommendation type
    When I visit the "Home Page"
    And I select "CROSS_SELL" in the "recommendation_type" dropdown
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
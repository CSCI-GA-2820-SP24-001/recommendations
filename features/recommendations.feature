Feature: The recommendation service back-end
    As a E-Commerce owner
    I need a RESTful recommendation service
    So that I can keep track of all the recommendation made to the customer

# Background:
#     Given the following recommendations
#         | id | name       | product_id | recommendation_name | recommendation_id  | recommendation_type |
#         | 1  | cake       | 15         | cookie              | 123                | CROSS_SELL          |
#         | 2  | Lemon      | 10         | Orange              | 321                | CROSS_SELL          |
#         | 3  | pineapple  | 28         | Mango               | 456                | CROSS_SELL          |
#         | 4  | Water      | 31         | Sparkling Water     | 654                | UPSELL              |
#         | 5  | sprite     | 16         | Coke                | 111                | CROSS_SELL          | 

Background:
    Given the server is started

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Recommendation Demo REST API Service" in the title
    And  I should not see "404 Not Found"

Scenario: Create a Recommendation
    When I visit the "Home Page"
    And I set the "name" to "Feeder"
    And I select the "recommendationType" drop-down to "cross-sell"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "name" field should be empty
    And the "recommendationType" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Feeder" in the "name" field
    And I should see "cross-sell" in the "recommendationType" drop-down
    And I should see "recommendationID" in the "Id" field
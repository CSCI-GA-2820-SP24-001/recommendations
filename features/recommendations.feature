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
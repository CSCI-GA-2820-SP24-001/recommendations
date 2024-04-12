Feature: The recommendation service back-end
    As a E-Commerce owner
    I need a RESTful recommendation service
    So that I can keep track of all the recommendation made to the customer

# Background:
#     Given the following recommendations
#         | id | user_id | product_id | bought_in_last_30_days | rating | recommendation_type |
#         | 1  | 11      | 15         | True                   | 2      | UPSELL              |
#         | 2  | 21      | 10         | True                   | 3      | CROSS_SELL          |
#         | 3  | 1       | 28         | False                  | 4      | TRENDING            |
#         | 4  | 5       | 31         | False                  | 0      | UPSELL              |
#         | 5  | 9       | 16         | False                  | 1      | TRENDING            |

Background:
    Given the server is started

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Recommendation Demo REST API Service" in the title
    And  I should not see "404 Not Found"
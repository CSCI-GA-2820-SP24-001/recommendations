"""
Recommendation API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Recommendation
from tests.factories import RecommendationFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)

BASE_URL = "/recommendations"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestRecommendationService(TestCase):
    """REST API Server Tests"""

    # pylint: disable=duplicate-code
    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Recommendation).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_recommendations(self, count):
        """Factory method to create recommendations in bulk"""
        recommendations = []
        for _ in range(count):
            test_recommendation = RecommendationFactory()
            response = self.client.post(BASE_URL, json=test_recommendation.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test recommendation",
            )
            new_recommendation = response.get_json()
            test_recommendation.id = new_recommendation["id"]
            recommendations.append(test_recommendation)
        return recommendations

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################
    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_recommendation(self):
        """It should Create a new Recommendation"""
        test_recommendation = RecommendationFactory()
        logging.debug("Test Recommendation: %s", test_recommendation.serialize())
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_recommendation = response.get_json()
        self.assertEqual(new_recommendation["name"], test_recommendation.name)
        self.assertEqual(new_recommendation["recommendation_in_stock"], test_recommendation.recommendation_in_stock)
        self.assertEqual(
            new_recommendation["recommendation_name"],
            test_recommendation.recommendation_name,
        )
        self.assertEqual(
            new_recommendation["recommendation_id"],
            test_recommendation.recommendation_id,
        )
        self.assertEqual(
            new_recommendation["recommendation_type"],
            test_recommendation.recommendation_type.name,
        )

    def test_get_recommendation(self):
        """It should Get a single Recommendation"""
        # get the id of a recommendation
        test_recommendation = self._create_recommendations(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_recommendation.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_recommendation.name)

    def test_get_recommendation_not_found(self):
        """It should not Get a Recommendation thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_update_recommendation(self):
        """It should Update an existing Recommendation"""
        # create a recommendation to update
        test_recommendation = RecommendationFactory()
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the recommendation
        new_recommendation = response.get_json()
        logging.debug(new_recommendation)

        new_recommendation["recommendation_name"] = "unknown"
        new_recommendation["recommendation_id"] = 0

        response = self.client.put(
            f"{BASE_URL}/{new_recommendation['id']}", json=new_recommendation
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_recommendation = response.get_json()

        self.assertEqual(updated_recommendation["recommendation_name"], "unknown")
        self.assertEqual(updated_recommendation["recommendation_id"], 0)

    def test_update_recommendation_id(self):
        """It should update the recommendation id for an existing product"""
        # Create a recommendation to update
        test_recommendation = RecommendationFactory()
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Fetch the newly created recommendation
        new_recommendation = response.get_json()
        logging.debug(new_recommendation)

        # Define a new recommendation ID to update
        new_recommendation_id = 123  # Example new ID

        # Update the recommendation ID
        response = self.client.put(
            f"{BASE_URL}/{new_recommendation['id']}/{new_recommendation_id}",
            json=new_recommendation,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_recommendation = response.get_json()

        # Check that the recommendation ID has been updated
        self.assertEqual(
            updated_recommendation["recommendation_id"], new_recommendation_id
        )

    def test_update_recommendation_name(self):
        """It should update the recommendation name for an existing product"""
        # Create a recommendation to update
        test_recommendation = RecommendationFactory()
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Fetch the newly created recommendation
        new_recommendation = response.get_json()
        logging.debug(new_recommendation)

        # Define a new name for the recommendation
        new_name = "Updated Recommendation Name"

        # Update the recommendation name
        response = self.client.put(
            f"{BASE_URL}/{new_recommendation['id']}/{new_name}",
            json=new_recommendation,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_recommendation = response.get_json()

        # Check that the recommendation name has been updated
        self.assertEqual(updated_recommendation["recommendation_name"], new_name)

    def test_delete_recommendation(self):
        """It should Delete a Recommendation"""
        test_recommendation = self._create_recommendations(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_recommendation.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_recommendation.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_recommendation_list(self):
        """It should Get a list of Recommendations"""
        self._create_recommendations(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    # ----------------------------------------------------------
    # TEST QUERY
    # ----------------------------------------------------------
    def test_get_recommendations_by_name(self):
        """It should filter recommendations by name"""
        # Create recommendations to filter
        recommendation_1 = RecommendationFactory(name="Product A")
        recommendation_2 = RecommendationFactory(name="Product B")
        self.client.post(BASE_URL, json=recommendation_1.serialize())
        self.client.post(BASE_URL, json=recommendation_2.serialize())

        # Filter recommendations by name
        response = self.client.get(f"{BASE_URL}?name=Product A")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Product A")

    def test_get_recommendations_by_recommendation_name(self):
        """It should filter recommendations by recommendation name"""
        # Create recommendations to filter
        recommendation_1 = RecommendationFactory(recommendation_name="RecA")
        recommendation_2 = RecommendationFactory(recommendation_name="RecB")
        self.client.post(BASE_URL, json=recommendation_1.serialize())
        self.client.post(BASE_URL, json=recommendation_2.serialize())

        # Filter recommendations by recommendation name
        response = self.client.get(f"{BASE_URL}?recommendation_name=RecA")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["recommendation_name"], "RecA")

    def test_get_recommendations_by_id(self):
        """It should filter recommendations by recommendation ID"""
        # Create recommendations to filter
        recommendation_1 = RecommendationFactory(recommendation_id=1)
        recommendation_2 = RecommendationFactory(recommendation_id=2)
        self.client.post(BASE_URL, json=recommendation_1.serialize())
        self.client.post(BASE_URL, json=recommendation_2.serialize())

        # Filter recommendations by recommendation ID
        response = self.client.get(f"{BASE_URL}?recommendation_id=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["recommendation_id"], 1)

    def test_query_by_in_stock(self):
        """It should Query Recommendations by in_sock"""
        recommendations = self._create_recommendations(10)
        available_recommendations = [
            recommendation
            for recommendation in recommendations
            if recommendation.recommendation_in_stock is True
        ]
        unavailable_recommendations = [
            recommendation
            for recommendation in recommendations
            if recommendation.recommendation_in_stock is False
        ]
        available_count = len(available_recommendations)
        unavailable_count = len(unavailable_recommendations)
        logging.debug(
            "In stock Recs [%d] %s", available_count, available_recommendations
        )
        logging.debug(
            "No stock Recs [%d] %s", unavailable_count, unavailable_recommendations
        )

        # test for recommendation_in_stock
        response = self.client.get(BASE_URL, query_string="recommendation_in_stock=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), available_count)
        # check the data just to be sure
        for recommendation in data:
            self.assertEqual(recommendation["recommendation_in_stock"], True)

        # test for unavailable
        response = self.client.get(BASE_URL, query_string="recommendation_in_stock=false")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), unavailable_count)
        # check the data just to be sure
        for recommendation in data:
            self.assertEqual(recommendation["recommendation_in_stock"], False)

    # ----------------------------------------------------------
    # TEST ACTIONS
    # ----------------------------------------------------------
    def test_restock_a_recommendation(self):
        """It should restock a Recommendation"""
        recommendations = self._create_recommendations(15)
        nostock_recommendations = [
            recommendation
            for recommendation in recommendations
            if recommendation.recommendation_in_stock is False
        ]
        recommendation = nostock_recommendations[0]
        response = self.client.put(f"{BASE_URL}/{recommendation.id}/restock")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"{BASE_URL}/{recommendation.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        logging.debug("Response data: %s", data)
        self.assertEqual(data["recommendation_in_stock"], True)

    def test_restock_not_available(self):
        """It should not restock a Recommendation that is not available"""
        recommendations = self._create_recommendations(15)
        instock_recommendations = [
            recommendation
            for recommendation in recommendations
            if recommendation.recommendation_in_stock is True
        ]
        recommendation = instock_recommendations[0]
        response = self.client.put(f"{BASE_URL}/{recommendation.id}/restock")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    # def test_restock_not_available(self):
    #     """It should not restock a Recommendation that is not available"""
    #     recommendations = self._create_recommendations(10)
    #     unavailable_recommendations = [
    #         recommendation
    #         for recommendation in recommendations
    #         if recommendation.recommendation_in_stock is True
    #     ]
    #     recommendation = unavailable_recommendations[0]
    #     response = self.client.put(f"{BASE_URL}/{recommendation.id}/restock")
    #     self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    # ----------------------------------------------------------
    # TEST HEALTHY
    # ----------------------------------------------------------
    def test_health(self):
        """It should be healthy"""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["status"], "OK")


######################################################################
#  T E S T   S A D   P A T H S
######################################################################
class TestSadPaths(TestCase):
    """Test REST Exception Handling"""

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()

    def test_method_not_allowed(self):
        """It should not allow update without a recommendation id"""
        response = self.client.put(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_recommendation_no_data(self):
        """It should not Create a Recommendation with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recommendation_no_content_type(self):
        """It should not Create a Recommendation with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_recommendation_wrong_content_type(self):
        """It should not Create a Recommendation with the wrong content type"""
        response = self.client.post(BASE_URL, data="hello", content_type="text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_recommendation_bad_in_stock(self):
        """It should not Create a Recommendation with bad recommendation_in_stock data"""
        test_recommendation = RecommendationFactory()
        logging.debug(test_recommendation)
        # change available to a string
        test_recommendation.recommendation_in_stock = "true"
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

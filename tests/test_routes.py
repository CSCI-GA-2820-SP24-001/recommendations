"""
Recommendation API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Recommendation
from .factories import RecommendationFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)

BASE_URL = "/recommendations"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestYourResourceService(TestCase):
    """REST API Server Tests"""

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

    def _create_recommendation(self, count):
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

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # Todo: Add your test cases here...
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
        self.assertEqual(
            new_recommendation["recommendationName"],
            test_recommendation.recommendationName,
        )
        self.assertEqual(
            new_recommendation["recommendationID"], test_recommendation.recommendationID
        )
        self.assertEqual(
            new_recommendation["recommendationType"],
            test_recommendation.recommendationType.name,
        )
        # Check that location is correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_recommendation = response.get_json()
        self.assertEqual(new_recommendation["name"], test_recommendation.name)
        self.assertEqual(
            new_recommendation["recommendationName"],
            test_recommendation.recommendationName,
        )
        self.assertEqual(
            new_recommendation["recommendationID"], test_recommendation.recommendationID
        )
        self.assertEqual(
            new_recommendation["recommendationType"],
            test_recommendation.recommendationType.name,
        )

    # Test route for get Function (Read)
    # def test_get_recommendation(self):

    def test_get_recommendation(self):
        """It should Get a single Recommendation"""
        # get the id of a recommendation
        test_recommendation = self._create_recommendation(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_recommendation.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_recommendation.name)


##############
# def test_get_recommendation_not_found(self):
#     """It should not Get a Pet thats not found"""
#     response = self.client.get(f"{BASE_URL}/0")
#     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#     data = response.get_json()
#     logging.debug("Response data = %s", data)
#     self.assertIn("was not found", data["message"])
#############
# def test_update_recommendation(self):
# def test_list_recommendation(self):
# def test_delete_recommendation(self):

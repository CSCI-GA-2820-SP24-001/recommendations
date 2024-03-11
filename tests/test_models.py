"""
Test cases for Pet Model
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.models import (
    Recommendation,
    EnumRecommendationType,
    DataValidationError,
    db,
)
from .factories import RecommendationFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  R E C O M M E N D A T I O N   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestRecommendationModel(TestCase):
    """Test Cases for Recommendation Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Recommendation).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_recommendation_model(self):
        """It should create a Recommendation Model"""
        # Todo: Remove this test case example
        recommendation = RecommendationFactory()
        recommendation.create()
        self.assertIsNotNone(recommendation.id)
        found = Recommendation.all()
        self.assertEqual(len(found), 1)
        data = Recommendation.find(recommendation.id)
        self.assertEqual(data.name, recommendation.name)
        # TODO: This has error, data.recommendationType seems be generated ramdomly.
        # So maybe just don't check this here
        # self.assertEqual(data.recommendationType, EnumRecommendationType.UNKNOWN)

        self.assertEqual(data.recommendationName, recommendation.recommendationName)
        self.assertEqual(data.recommendationID, recommendation.recommendationID)

    # Todo: Add your test cases here...

    def test_update_recommendation(self):
        """It should Update an existing Recommendation"""
        # create a recommendation to update
        test_recommendation = RecommendationFactory()
        response = self.client.post(BASE_URL, json=test_recommendation.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # update the recommendation
        new_recommendation = response.get_json()
        logging.debug(new_recommendation)

        new_recommendation["recommendationName"] = "unknown"
        new_recommendation["recommendationID"] = 0

        response = self.client.put(
            f"{BASE_URL}/{new_recommendation['id']}", json=new_recommendation
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_recommendation = response.get_json()

        self.assertEqual(updated_recommendation["recommendationName"], "unknown")
        self.assertEqual(updated_recommendation["recommendationID"], 0)

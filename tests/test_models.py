"""
Test cases for Recommendation Model
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
        self.assertEqual(data.recommendationType, EnumRecommendationType.UNKNOWN)
        self.assertEqual(data.recommendationName, recommendation.recommendationName)
        self.assertEqual(data.recommendationID, recommendation.recommendationID)

    # TODO 
    # def test_create_a_recommendation(self):
    #     """It should Create a recommendation and assert that it exists"""
    #     recommendation = Recommendation(name="Fido", category="dog", available=True, gender=Gender.MALE)
    #     self.assertEqual(str(recommendation), "<Recommendation Fido id=[None]>")
    #     self.assertTrue(recommendation is not None)
    #     self.assertEqual(recommendation.id, None)
    #     self.assertEqual(recommendation.name, "Fido")
    #     self.assertEqual(recommendation.category, "dog")
    #     self.assertEqual(recommendation.available, True)
    #     self.assertEqual(recommendation.gender, Gender.MALE)
    #     recommendation = Recommendation(name="Fido", category="dog", available=False, gender=Gender.FEMALE)
    #     self.assertEqual(recommendation.available, False)
    #     self.assertEqual(recommendation.gender, Gender.FEMALE)

    def test_read_a_recommendation(self):
        """It should Read a Recommendation"""
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.id = None
        recommendation.create()
        self.assertIsNotNone(recommendation.id)
        # Fetch it back
        found_recommendation = Recommendation.find(recommendation.id)
        self.assertEqual(found_recommendation.id, recommendation.id)
        self.assertEqual(found_recommendation.name, recommendation.name)
        self.assertEqual(
            found_recommendation.recommendationType, EnumRecommendationType.UNKNOWN
        )

        self.assertEqual(
            found_recommendation.recommendationName, recommendation.recommendationName
        )
        self.assertEqual(
            found_recommendation.recommendationID, recommendation.recommendationID
        )

    # Todo: Add your test cases here...
    def test_update_a_recommendation(self):
        """It should Update a Recommendation"""
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.id = None
        recommendation.create()
        logging.debug(recommendation)
        self.assertIsNotNone(recommendation.id)
        # Change it an save it
        recommendation.category = "k9"
        original_id = recommendation.id
        recommendation.update()
        self.assertEqual(recommendation.id, original_id)
        self.assertEqual(recommendation.category, "k9")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0].id, original_id)
        self.assertEqual(recommendations[0].category, "k9")

    def test_update_no_id(self):
        """It should not Update a Recommendation with no id"""
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.id = None
        self.assertRaises(DataValidationError, recommendation.update)

    def test_delete_a_recommendation(self):
        """It should Delete a Recommendation"""
        recommendation = RecommendationFactory()
        recommendation.create()
        self.assertEqual(len(Recommendation.all()), 1)
        # delete the recommendation and make sure it isn't in the database
        recommendation.delete()
        self.assertEqual(len(Recommendation.all()), 0)

    def test_list_all_recommendations(self):
        """It should List all Recommendations in the database"""
        recommendations = Recommendation.all()
        self.assertEqual(recommendations, [])
        # Create 5 Recommendations
        for _ in range(5):
            recommendation = RecommendationFactory()
            recommendation.create()
        # See if we get back 5 recommendations
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 5)

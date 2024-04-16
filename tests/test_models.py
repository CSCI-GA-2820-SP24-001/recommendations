"""
Test cases for Recommendation Model
"""

import os
import logging
from unittest import TestCase
from unittest.mock import patch
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
class TestCaseBase(TestCase):
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
#  P E T   M O D E L   T E S T   C A S E S
######################################################################
class TestRecommendationModel(TestCaseBase):
    """Recommendation Model CRUD Tests"""

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_create_a_recommendation(self):
        """It should Create a recommendation and assert that it exists"""
        recommendation = Recommendation(
            name="Test_product_name",
            recommendation_in_stock=True,
            recommendation_type=EnumRecommendationType.UNKNOWN,
            recommendation_name="Test_recommendation_name",
            recommendation_id=0,
        )

        self.assertEqual(
            str(recommendation), "<Recommendation Test_product_name id=[None]>"
        )
        self.assertTrue(recommendation is not None)
        self.assertEqual(recommendation.id, None)
        self.assertEqual(recommendation.name, "Test_product_name")
        self.assertEqual(recommendation.recommendation_in_stock, True)
        self.assertEqual(
            recommendation.recommendation_type, EnumRecommendationType.UNKNOWN
        )
        self.assertEqual(recommendation.recommendation_name, "Test_recommendation_name")
        self.assertEqual(recommendation.recommendation_id, 0)

    def test_add_recommendation_model(self):
        """It should create a Recommendation and add to the database"""
        recommendation = RecommendationFactory()
        recommendation.create()
        self.assertIsNotNone(recommendation.id)
        found = Recommendation.all()
        self.assertEqual(len(found), 1)
        data = Recommendation.find(recommendation.id)
        self.assertEqual(data.name, recommendation.name)
        self.assertEqual(data.recommendation_type, EnumRecommendationType.UNKNOWN)
        self.assertEqual(data.recommendation_name, recommendation.recommendation_name)
        self.assertEqual(data.recommendation_id, recommendation.recommendation_id)

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
            found_recommendation.recommendation_type, EnumRecommendationType.UNKNOWN
        )

        self.assertEqual(
            found_recommendation.recommendation_name, recommendation.recommendation_name
        )
        self.assertEqual(
            found_recommendation.recommendation_id, recommendation.recommendation_id
        )

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

    def test_repr_recommendation(self):
        """test_repr_recommendation"""
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.id = None
        recommendation.create()
        self.assertEqual(
            repr(recommendation),
            f"<Recommendation {recommendation.name} id=[{recommendation.id}]>",
        )

    def test_serialize_a_recommendation(self):
        """It should serialize a Recommendation"""
        recommendation = RecommendationFactory()
        data = recommendation.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], recommendation.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], recommendation.name)
        self.assertIn("recommendation_in_stock", data)
        self.assertEqual(
            data["recommendation_in_stock"], recommendation.recommendation_in_stock
        )
        self.assertIn("recommendation_type", data)
        self.assertEqual(
            data["recommendation_type"], recommendation.recommendation_type.name
        )
        self.assertIn("recommendation_name", data)
        self.assertEqual(
            data["recommendation_name"], recommendation.recommendation_name
        )
        self.assertIn("recommendation_id", data)
        self.assertEqual(data["recommendation_id"], recommendation.recommendation_id)

    def test_deserialize_a_recommendation(self):
        """It should de-serialize a Recommendation"""
        data = RecommendationFactory().serialize()
        recommendation = Recommendation()
        recommendation.deserialize(data)
        self.assertNotEqual(recommendation, None)
        self.assertEqual(recommendation.id, None)
        self.assertEqual(recommendation.name, data["name"])
        self.assertEqual(
            recommendation.recommendation_in_stock, data["recommendation_in_stock"]
        )
        self.assertEqual(
            data["recommendation_type"], recommendation.recommendation_type.name
        )
        self.assertEqual(
            data["recommendation_name"], recommendation.recommendation_name
        )
        self.assertEqual(data["recommendation_id"], recommendation.recommendation_id)

    def test_deserialize_missing_data(self):
        """It should not deserialize a Recommendation with missing data"""
        data = {
            "id": 1,
            "name": "test_deserialize_name",
            "recommendation_name": "test_deserialize_recommendation_name",
        }
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)

    def test_deserialize_bad_in_stock(self):
        """It should not deserialize a bad recommendation_in_stock attribute"""
        test_recommendation = RecommendationFactory()
        data = test_recommendation.serialize()
        data["recommendation_in_stock"] = "true"
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)

    # def test_deserialize_bad_EnumRecommendationType(self):
    #     """It should not deserialize a bad EnumRecommendationType attribute"""
    #     test_recommendation = RecommendationFactory()
    #     data = test_recommendation.serialize()
    #     data["recommendation_type"] = EnumRecommendationType.ACCESSORY  # wrong case
    #     recommendation = Recommendation()
    #     self.assertRaises(DataValidationError, recommendation.deserialize, data)


######################################################################
#  T E S T   E X C E P T I O N   H A N D L E R S
######################################################################
class TestExceptionHandlers(TestCaseBase):
    """Recommendation Model Exception Handlers"""

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        recommendation = RecommendationFactory()
        self.assertRaises(DataValidationError, recommendation.create)

    @patch("service.models.db.session.commit")
    def test_update_exception(self, exception_mock):
        """It should catch a update exception"""
        exception_mock.side_effect = Exception()
        recommendation = RecommendationFactory()
        self.assertRaises(DataValidationError, recommendation.update)

    @patch("service.models.db.session.commit")
    def test_delete_exception(self, exception_mock):
        """It should catch a delete exception"""
        exception_mock.side_effect = Exception()
        recommendation = RecommendationFactory()
        self.assertRaises(DataValidationError, recommendation.delete)

    # @patch("service.models.db.session.commit")
    # def test_deserialize_exception(self, exception_mock):
    #     """It should catch deserialize exception"""
    #     exception_mock.side_effect = AttributeError("Invalid attribute")
    #     data = RecommendationFactory()
    #     recommendation = RecommendationFactory()
    #     self.assertRaises(DataValidationError, recommendation.deserialize, data)

    # def test_deserialize_bad_EnumRecommendationType(self):
    #     """It should not deserialize a bad EnumRecommendationType attribute"""
    #     test_recommendation = RecommendationFactory()
    #     data = test_recommendation.serialize()
    #     data["recommendation_type"] = EnumRecommendationType.ACCESSORY  # wrong case
    #     recommendation = Recommendation()
    #     self.assertRaises(DataValidationError, recommendation.deserialize, data)

    ######################################################################
    #  Q U E R Y   T E S T   C A S E S
    ######################################################################

    def test_find_by_in_stock(self):
        """It should Find Recommendations by recommendation_in_stock"""
        recommendations = RecommendationFactory.create_batch(10)
        for recommendation in recommendations:
            recommendation.create()
        recommendation_in_stock = recommendations[0].recommendation_in_stock
        count = len(
            [
                recommendation
                for recommendation in recommendations
                if recommendation.recommendation_in_stock == recommendation_in_stock
            ]
        )
        found = Recommendation.find_by_in_stock(recommendation_in_stock)
        self.assertEqual(found.count(), count)
        for recommendation in found:
            self.assertEqual(
                recommendation.recommendation_in_stock, recommendation_in_stock
            )


# class TestModelQueries(TestCaseBase):
#     """Recommendation Model Query Tests"""

#     def test_find_recommendation(self):
#         """It should Find a Recommendation by ID"""
#         recommendations = RecommendationFactory.create_batch(5)
#         for recommendation in recommendations:
#             recommendation.create()
#         logging.debug(recommendations)
#         # make sure they got saved
#         self.assertEqual(len(Recommendation.all()), 5)
#         # find the 2nd recommendation in the list
#         recommendation = Recommendation.find(recommendations[1].id)
#         self.assertIsNot(recommendation, None)
#         self.assertEqual(recommendation.id, recommendations[1].id)
#         self.assertEqual(recommendation.name, recommendations[1].name)
#         self.assertEqual(recommendation.recommendation_in_stock, recommendations[1].recommendation_in_stock)
#         self.assertEqual(recommendation.gender, recommendations[1].gender)
#         self.assertEqual(recommendation.birthday, recommendations[1].birthday)

#     def test_find_by_category(self):
#         """It should Find Recommendations by Category"""
#         recommendations = RecommendationFactory.create_batch(10)
#         for recommendation in recommendations:
#             recommendation.create()
#         category = recommendations[0].category
#         count = len([recommendation for recommendation in recommendations if recommendation.category == category])
#         found = Recommendation.find_by_category(category)
#         self.assertEqual(found.count(), count)
#         for recommendation in found:
#             self.assertEqual(recommendation.category, category)

#     def test_find_by_name(self):
#         """It should Find a Recommendation by Name"""
#         recommendations = RecommendationFactory.create_batch(10)
#         for recommendation in recommendations:
#             recommendation.create()
#         name = recommendations[0].name
#         count = len([recommendation for recommendation in recommendations if recommendation.name == name])
#         found = Recommendation.find_by_name(name)
#         self.assertEqual(found.count(), count)
#         for recommendation in found:
#             self.assertEqual(recommendation.name, name)

#     def test_find_by_availability(self):
#         """It should Find Recommendations by Availability"""
#         recommendations = RecommendationFactory.create_batch(10)
#         for recommendation in recommendations:
#             recommendation.create()
#         recommendation_in_stock = recommendations[0].recommendation_in_stock
#         count = len([recommendation for recommendation in recommendations
#                       if recommendation.recommendation_in_stock == recommendation_in_stock])
#         found = Recommendation.find_by_availability(recommendation_in_stock)
#         self.assertEqual(found.count(), count)
#         for recommendation in found:
#             self.assertEqual(recommendation.recommendation_in_stock, recommendation_in_stock)

#     def test_find_by_gender(self):
#         """It should Find Recommendations by Gender"""
#         recommendations = RecommendationFactory.create_batch(10)
#         for recommendation in recommendations:
#             recommendation.create()
#         gender = recommendations[0].gender
#         count = len([recommendation for recommendation in recommendations if recommendation.gender == gender])
#         found = Recommendation.find_by_gender(gender)
#         self.assertEqual(found.count(), count)
#         for recommendation in found:
#             self.assertEqual(recommendation.gender, gender)

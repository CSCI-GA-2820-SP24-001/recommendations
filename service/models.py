"""
Models for recommendation service

Models
------
Recommendation - A Recommendation used in the Recommendation

Attributes:
-----------
name (string) - the name of the product
recommendation_type (enum) - the recommendation type (cross-sell, up-sell...etc)
recommendation (string) - recommendation product

recommendation_name (string) - recommendation name
recommendation_id (int) - recommendation id
"""

import logging
from enum import Enum
from flask_sqlalchemy import SQLAlchemy


logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class EnumRecommendationType(Enum):
    """Enumeration of valid Recommendation Type"""

    CROSS_SELL = 0
    UP_SELL = 1
    ACCESSORY = 2
    UNKNOWN = 3


class Recommendation(db.Model):
    """
    Class that represents a Recommendation
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    recommendation_type = db.Column(
        db.Enum(EnumRecommendationType),
        nullable=False,
        server_default=(EnumRecommendationType.UNKNOWN.name),
    )
    recommendation_name = db.Column(db.String(63))
    recommendation_id = db.Column(db.Integer, primary_key=False)

    def __repr__(self):
        return f"<Recommendation {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Recommendation to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(e) from e

    def update(self):
        """
        Updates a Recommendation to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Recommendation from the data store"""

        logger.info("Deleting %s", self.name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self):
        """Serializes a Recommendation into a dictionary"""

        return {
            "id": self.id,
            "name": self.name,
            "recommendation_type": self.recommendation_type.name,
            "recommendation_name": self.recommendation_name,
            "recommendation_id": self.recommendation_id,
        }

    def deserialize(self, data):
        """
        Deserializes a Recommendation from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.recommendation_type = getattr(
                EnumRecommendationType, data["recommendation_type"]
            )  # create enum from string
            self.recommendation_name = data["recommendation_name"]
            self.recommendation_id = data["recommendation_id"]
        except AttributeError as error:
            raise DataValidationError("Invalid attribute: " + error.args[0]) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Recommendation: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Recommendation: body of request contained bad or no data "
                + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Recommendations in the database"""
        logger.info("Processing all Recommendations")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Recommendation by its ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Recommendations with the given name

        Args:
            name (string): the name of the Recommendations you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_type(cls, recommendation_type):
        """Returns all Recommendations with the given recommendation type

        Args:
            recommendation_type (string): the recommendation type of the Recommendations you want to match
        """
        logger.info(
            "Processing recommendation type query for %s ...", recommendation_type
        )
        return cls.query.filter(
            cls.recommendation_type == EnumRecommendationType[recommendation_type]
        )

    @classmethod
    def find_by_recommendation_name(cls, recommendation_name):
        """Returns all Recommendations with the given recommendation name

        Args:
            recommendation_name (string): the recommendation name of the Recommendations you want to match
        """
        logger.info(
            "Processing recommendation name query for %s ...", recommendation_name
        )
        return cls.query.filter(cls.recommendation_name == recommendation_name)

    @classmethod
    def find_by_recommendation_id(cls, recommendation_id):
        """Returns all Recommendations with the given recommendation ID

        Args:
            recommendation_id (int): the recommendation ID of the Recommendations you want to match
        """
        logger.info("Processing recommendation ID query for %s ...", recommendation_id)

        return cls.query.filter(cls.recommendation_id == recommendation_id)

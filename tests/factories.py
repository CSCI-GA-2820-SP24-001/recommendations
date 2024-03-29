"""
Test Factory to make fake objects for testing
"""

# from datetime import date

import factory
from factory.fuzzy import FuzzyChoice
from service.models import Recommendation, EnumRecommendationType


class RecommendationFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Recommendation

    # Add your other attributes here...
    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    recommendationType = EnumRecommendationType.UNKNOWN
    recommendationName = FuzzyChoice(choices=["apple", "banana", "steak", "fish"])
    recommendationID = factory.Sequence(lambda n: n)

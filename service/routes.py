######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Recommendation Store Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Recommendations from the inventory of Recommendations in the RecommendationShop
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Recommendation
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################
# TODO: Place your REST API code here ...
######################################################################
# READ A Recommendation
######################################################################
# @app.route("/recommendations/<int:recommendation_id>", methods=["GET"])
# def get_recommendations(recommendation_id):
#     """
#     Retrieve a single Recommendation

#     This endpoint will return a Recommendation based on it's id
#     """
#     app.logger.info("Request for Recommendation with id: %s", recommendation_id)

#     recommendation = Recommendation.find(recommendation_id)
#     if not recommendation:
#         error(
#             status.HTTP_404_NOT_FOUND,
#             f"Recommendation with id '{recommendation_id}' was not found.",
#         )

#     app.logger.info("Returning Recommendation: %s", Recommendation.name)
#     return jsonify(Recommendation.serialize()), status.HTTP_200_OK


######################################################################
# CREATE A NEW Recommendation
######################################################################
@app.route("/recommendations", methods=["POST"])
def create_recommendations():
    """
    Creates a Recommendation

    This endpoint will create a Recommendation based the data in the body that is posted
    """
    app.logger.info("Request to create a Recommendation")
    check_content_type("application/json")

    recommendation = Recommendation()
    recommendation.deserialize(request.get_json())
    recommendation.create()
    message = recommendation.serialize()
    # TODO: Uncomment this code get_recommendations is implemented
    # location_url = url_for(
    #     "get_recommendations", recommendation_id=recommendation.id, _external=True
    # )
    location_url = "unknown"

    app.logger.info("Recommendation with ID: %d created.", recommendation.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


# ######################################################################
# # UPDATE AN EXISTING Recommendation
# ######################################################################
# @app.route("/recommendations/<int:recommendation_id>", methods=["PUT"])
# def update_recommendations(recommendation_id):
#     """
#     Update a Recommendation

#     This endpoint will update a Recommendation based the body that is posted
#     """
#     app.logger.info("Request to update Recommendation with id: %d", recommendation_id)
#     check_content_type("application/json")

#     recommendation = Recommendation.find(recommendation_id)
#     if not Recommendation:
#         error(
#             status.HTTP_404_NOT_FOUND,
#             f"Recommendation with id: '{recommendation_id}' was not found.",
#         )

#     recommendation.deserialize(request.get_json())
#     recommendation.id = recommendation_id
#     recommendation.update()

#     app.logger.info("Recommendation with ID: %d updated.", recommendation.id)
#     return jsonify(recommendation.serialize()), status.HTTP_200_OK


# ######################################################################
# # DELETE A Recommendation
# ######################################################################
# @app.route("/recommendations/<int:recommendation_id>", methods=["DELETE"])
# def delete_Recommendations(recommendation_id):
#     """
#     Delete a Recommendation

#     This endpoint will delete a Recommendation based the id specified in the path
#     """
#     app.logger.info("Request to delete Recommendation with id: %d", recommendation_id)

#     recommendation = Recommendation.find(recommendation_id)
#     if recommendation:
#         recommendation.delete()

#     app.logger.info("Recommendation with ID: %d delete complete.", recommendation_id)
#     return "", status.HTTP_204_NO_CONTENT


######################################################################
# (TODO) LIST ALL Recommendations
# Required extra function (classmethod) to develop
######################################################################
# @app.route("/recommendations", methods=["GET"])
# def list_pets():
#     """Returns all of the recommendations"""
#     app.logger.info("Request for pet list")

#     recommendations = []

#     # See if any query filters were passed in
#     category = request.args.get("category")
#     name = request.args.get("name")
#     if category:
#         recommendations = Recommendation.find_by_category(category)
#     elif name:
#         recommendations = Recommendation.find_by_name(name)
#     else:
#         recommendations = Recommendation.all()

#     results = [recommendation.serialize() for pet in recommendations]
#     app.logger.info("Returning %d recommendations", len(results))
#     return jsonify(results), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        error(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    error(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# Logs error messages before aborting
######################################################################
def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    abort(status_code, reason)

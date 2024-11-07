# # routes/firebase.py
#
# from flask import Blueprint, jsonify
# from apis.firebase_storage import list_photos_in_about_folder
#
# firebase_routes = Blueprint('firebase_routes', __name__)
#
#
# @firebase_routes.route('/firebase/photos/about', methods=['GET'])
# def get_about_photos():
#     photos = list_photos_in_about_folder()
#     return jsonify({'photos': photos})

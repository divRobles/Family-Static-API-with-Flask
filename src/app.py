"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
import json


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def consult_all_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    if len(members) > 0:
        response_body = {
            "family": members
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"msg": "Error en el servidor"}), 500

@app.route('/member/<int:member_id>', methods=['GET','DELETE'])
def handle_member(member_id):
    if request.method == 'GET':
        members = jackson_family.get_member(member_id)
        if len(members) == 0:
            return jsonify({"msg": "No existe ningun miembro de la familia con ese Id"}), 400
        elif len(members) == 1:
            return jsonify({"Miembro": members[0]}), 200
        else:
            return jsonify({"Msg": "Error del servidor"}), 500
    
    if request.method == 'DELETE':
        num_members = len(jackson_family._members)
        members = jackson_family.delete_member(member_id)

        if num_members > len(members):
            return jsonify({"Eliminado": members}), 200
        else:
            return jsonify({"Message" : "Error en el servidor"}), 500


@app.route('/member', methods=['POST'])
def add_member():
    body = json.loads(request.data)
    res = not body
            
    if res is True:
        return jsonify({"Msg": "Body vacio"}), 500
    else:
        member = jackson_family.add_member(body)
        return jsonify({'msg': "Miembro añadido correctamente"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

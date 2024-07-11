import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({"first_name": "Tommy", "age": 23, "lucky_numbers": [7, 13, 22]})
jackson_family.add_member({"first_name": "Jane", "age": 35, "lucky_numbers": [3, 8, 12]})
jackson_family.add_member({"first_name": "Jimmy", "age": 7, "lucky_numbers": [1, 9, 14]})

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def add_member():
    member_data = request.get_json()
    if not member_data or "first_name" not in member_data:
        raise APIException("You must specify the member's first name", status_code=400)
    jackson_family.add_member(member_data)
    return jsonify({"message": "Member added successfully"}), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.get_member(id)
    if not member:
        raise APIException("Member not found", status_code=404)
    
    jackson_family.delete_member(id)
    return jsonify({"message": "Member deleted successfully", "done": True}), 200

@app.route('/member/<int:id>', methods=['PUT'])
def update_member(id):
    member_data = request.get_json()
    member = jackson_family.get_member(id)
    if not member:
        raise APIException("Member not found", status_code=404)
    
    jackson_family.update_member(id, member_data)
    return jsonify({"message": "Member updated successfully"}), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if not member:
        raise APIException("Member not found", status_code=404)
    
    return jsonify(member), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)


"""AI23 - Rendu 4 - API"""

import os
from datetime import timedelta


from flasgger import Swagger
from dotenv import load_dotenv

from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

from database import LibraryDatabase as db

# Configure the Swagger documentation
swagger_config = Swagger.DEFAULT_CONFIG
swagger_config['title'] = 'AI23 - Rendu 4 - API'
swagger_config['description'] = 'API for the AI23 - Rendu 4 project'
swagger_config['version'] = '1.0.0'
swagger_config['host'] = 'localhost:5000'
swagger_config['basePath'] = '/'
swagger_config['schemes'] = ['http', 'https']
swagger_config['produces'] = ['application/json']
swagger_config['consumes'] = ['application/json']

# Load the environment variables
load_dotenv()

#  Get the environment variables
host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")
db_name = os.getenv("PG_DB")
user = os.getenv("PG_USER")
db_password = os.getenv("PG_PASS")
jwt_secret = os.getenv("JWT_SECRET")

# Configure the Flask app
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = jwt_secret
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=4)
jwt = JWTManager(app)
swagger = Swagger(app, config=swagger_config)
CORS(app)

# Configure the database
database = db(host, port, db_name, user, db_password)



@app.route('/login', methods=['POST'])
def login():
    """
    Login route
    ---
    parameters:
        - name: login
          in: body
          required: true
          schema:
            id: user_login
            required:
                - login
                - password
            properties:
                login:
                    type: string
                    description: The user's login
                password:
                    type: string
                    description: The user's password
    responses:
        200:
            description: Access token
            schema:
                type: object
                properties:
                    access_token:
                        type: string
                        description: Access token
        400:
            description: Missing login or password
        401:
            description: Invalid login or password
    """

    data = request.get_json()
    user_login = data.get('login')
    password = data.get('password')

    if not user_login or not password:
        return jsonify({"error": "Missing login or password"}), 400

    if database.login(user_login, password):
        access_token = create_access_token(identity=user_login)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid login or password"}), 401

@app.route('/get-account-type', methods=['GET'])
@jwt_required()
def get_account_type():
    """
    Get account type route
    ---
    parameters:
        - name: login
          in: query
          type: string
          required: true
          description: The user's login
    responses:
        200:
            description: Account type
            schema:
                type: string
                description: The account type
        400:
            description: Missing login
        401:
            description: Invalid login
    """

    user_login = request.args.get('login')

    if not user_login:
        return jsonify({"error": "Missing login"}), 400

    account_type = database.get_account_type(user_login)

    if account_type:
        return str(account_type), 200

    else:
        return jsonify({"error": "Invalid login"}), 401


@app.route("/get-ressources", methods=['GET'])
@jwt_required()
def get_ressources():
    """
    Get resources route
    ---
    parameters:
        - name: resource_name
          in: query
          type: string
          required: false
          description: Name of the resource
        - name: resource_type
          in: query
          type: string
          required: false
          description: Type of the resource
        - name: only_available
          in: query
          type: boolean
          required: false
          description: Retrieve only available   resources
    responses:
        200:
            description: List of resources
        404:
            description: No resources found
    """

    # Parse the request parameters
    resource_name = request.args.get('resource_name', '')
    resource_type = request.args.get('resource_type', '')
    only_available = request.args.get('only_available', '').lower() == 'true'

    # Get the ressources from the database
    ressources = database.get_ressources(resource_name, resource_type, only_available)

    if ressources:
        return jsonify(ressources), 200
    else:
        return jsonify({"error": "No ressources found"}), 404
    

@app.route("/get-user-infos", methods=['GET'])
@jwt_required()
def get_user_infos():
    """
    Get user infos route
    ---
    parameters:
        - name: login
          in: query
          type: string
          required: true
          description: The user's login
    responses:
        200:
            description: User infos
            schema:
                type: object
                properties:
                    login:
                        type: string
                        description: The user's login
                    account_type:
                        type: string
                        description: The user's account type
        400:
            description: Missing login
        401:
            description: Invalid login
    """

    user_login = request.args.get('login')

    if not user_login:
        return jsonify({"error": "Missing login"}), 400

    user_infos = database.get_user_infos(user_login)

    if user_infos:
        return jsonify(user_infos), 200

    else:
        return jsonify({"error": "Invalid login"}), 401


@app.route("/get-ressource-infos", methods=['GET'])
@jwt_required()
def get_ressource_infos():
    """
    Get resource infos route
    ---
    parameters:
        - name: resource_id
          in: query
          type: integer
          required: true
          description: The resource's id
    responses:
        200:
            description: Resource infos
        400:
            description: Missing resource id
        401:
            description: Invalid resource id
    """

    resource_id = request.args.get('resource_id')

    if not resource_id:
        return jsonify({"error": "Missing resource id"}), 400

    resource_infos = database.get_ressource_infos(resource_id)

    if resource_infos:
        return jsonify(resource_infos), 200

    else:
        return jsonify({"error": "Invalid resource id"}), 401
    

@app.route("/get-resource-contributors", methods=['GET'])
@jwt_required()
def get_resource_contributors():
    """
    Get resource contributors route
    ---
    parameters:
        - name: resource_id
          in: query
          type: integer
          required: true
          description: The resource's id
    responses:
        200:
            description: Resource contributors
        400:
            description: Missing resource id
        401:
            description: Invalid resource id
    """

    resource_id = request.args.get('resource_id')

    if not resource_id:
        return jsonify({"error": "Missing resource id"}), 400

    resource_contributors = database.get_resource_contributors(resource_id)

    if resource_contributors:
        return jsonify(resource_contributors), 200

    else:
        return jsonify({"error": "Invalid resource id"}), 401
    

@app.route("/get-resource-copies", methods=['GET'])
@jwt_required()
def get_resource_copies():
    """
    Get resource copies route
    ---
    parameters:
        - name: resource_id
          in: query
          type: integer
          required: true
          description: The resource's id
    responses:
        200:
            description: Resource copies
        400:
            description: Missing resource id
        401:
            description: Invalid resource id
    """

    resource_id = request.args.get('resource_id')

    if not resource_id:
        return jsonify({"error": "Missing resource id"}), 400

    resource_copies = database.get_resource_copies(resource_id)

    if resource_copies:
        return jsonify(resource_copies), 200

    else:
        return jsonify({"error": "Invalid resource id"}), 401
    

@app.route("/get-users", methods=['GET'])
@jwt_required()
def get_users():
    """
    Get users route
    ---
    parameters:
        - name: login
            in: query
            type: string
            required: true
            description: The user's login
    responses:
        200:
            description: List of users
        404:
            description: No users found
    """

    #Check if the user is a staff member
    user_login = request.args.get('login')
    account_type = database.get_account_type(user_login)

    if account_type == "Adherent" or account_type is None:
        return jsonify({"error": "Unauthorized"}), 401

    # Get the users from the database
    users = database.get_users()

    if users:
        return jsonify(users), 200
    else:
        return jsonify({"error": "No users found"}), 404


@app.route("/create-user", methods=['POST'])
@jwt_required()
def create_user():
    """ 
    Create user route
    """
    try:
        json_r = request.get_json()

        # Get the staff member account type
        staff_login = json_r.get('login')
        account_type = database.get_account_type(staff_login)

        if account_type.value == "Adherent" or account_type is None:
            return jsonify({"error": "Unauthorized"}), 401

        elif account_type.value == "Personnel" and (json_r.get('account_type') == "Administrateur" or json_r.get('account_type') == "Personnel"):
            return jsonify({"error": "Unauthorized"}), 401

        user_login = json_r.get('user_login')
        password = json_r.get('password')
        user_account_type = json_r.get('account_type')
        nom = json_r.get('nom')
        prenom = json_r.get('prenom')
        adresse = json_r.get('adresse')
        email = json_r.get('email')
        date_naissance = json_r.get('date_naissance')  # Assuming this field is provided
        telephone = json_r.get('telephone')  # Assuming this field is provided

        if not user_login or not password or not user_account_type or not nom or not prenom or not adresse or not email:
            return jsonify({"error": "Missing required parameters"}), 400

        # Create user in the database
        database.create_user(user_login, password, user_account_type, nom, prenom, adresse, email, date_naissance, telephone)

        # Return a success response
        return jsonify({"success": "User created successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "Error"}), 500


@app.route("/add-loan", methods=['POST'])
@jwt_required()
def add_loan():

    """ 
    Add loan route
    """

    json_r = request.get_json()
    print(json_r)

    # Check if the user is able to add a loan
    user_login = json_r.get('user_login')

    if not database.is_eligible_to_borrow(user_login):
        return jsonify({"error": "Unauthorized"}), 401

    # Check if the user borrowed too many resources
    if not database.is_eligible_to_borrow(user_login):
        return jsonify({"error": "Unauthorized"}), 401

    # Add loan in the database
    resource_id = json_r.get('copy_number')
    loan_duration = json_r.get('loan_duration')
    database.add_loan(user_login, resource_id, loan_duration)

    print(resource_id);

    return jsonify({"success": "Loan added"}), 200


if __name__ == '__main__':
    app.run(debug=True)

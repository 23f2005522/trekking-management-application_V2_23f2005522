from flask import blueprints , jsonify , request 


health_blueprint = blueprints.Blueprint("health" , __name__ , url_prefix="/api/health")

@health_blueprint.route("/", methods=["GET"])
def check_health():
    response = {
        "status": "success",
        "message": "Server is up and running"
    }
    return jsonify(response), 200

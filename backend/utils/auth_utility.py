
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt


def role_required(required_role):
    
    """
    role_required is a decorator that checks if the logged-in user has the required role to access a specific route.
    
    PARAMETERS:
        - required_role (str): The role required to access the route. This can be a string representing the role, or an enum value from UserRole.
    
    RETURN:
        - A decorator function that wraps the original route function and checks the user's role.
    
    useExample:
        @app.route('/admin')
        @role_required('admin' or UserRole.ADMIN (enums))
        def admin_dashboard():
            return render_template('admin_dashboard.html')
    
    """
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            
            token_data = get_jwt()
            role = token_data.get("role")


           # if userorle dont match dont allow access to the route and return a 403 forbidden error code\
               
            if role == None or role != required_role:
                response = {
                    "message": "You do not have permission to access this resource."
                }
                return jsonify(response), 403 # forbidden error code

            return f(*args, **kwargs)
        return decorated_function
    return decorator
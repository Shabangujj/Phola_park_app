from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from .access_control import ROLE_HIERARCHY, ROLE_PERMISSIONS

def jwt_role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return jsonify({
                    "error": "Access denied",
                    "message": f"Role '{user_role}' does not have permission to access this resource"
                }), 403

            return fn(*args, **kwargs)

        return wrapper
    return decorator

def jwt_access_required(min_role="user", permission=None):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            claims = get_jwt()
            user_role = claims.get("role")
            user_permissions = set(claims.get("permissions", []))

            if not user_role:
                return jsonify({
                    "error": "Access denied",
                    "message": "Role missing in token"
                }), 403

            if user_role not in ROLE_HIERARCHY:
                return jsonify({
                    "error": "Access denied",
                    "message": "Invalid role"
                }), 403

            if min_role not in ROLE_HIERARCHY:
                return jsonify({
                    "error": "Configuration error",
                    "message": f"Invalid minimum role: {min_role}"
                }), 500

            if ROLE_HIERARCHY[user_role] < ROLE_HIERARCHY[min_role]:
                return jsonify({
                    "error": "Access denied",
                    "required_role": min_role,
                    "your_role": user_role
                }), 403

            if permission:
                role_permissions = ROLE_PERMISSIONS.get(user_role, set())
                effective_permissions = role_permissions | user_permissions

                if permission not in effective_permissions:
                    return jsonify({
                        "error": "Access denied",
                        "required_permission": permission
                    }), 403

            return fn(*args, **kwargs)

        return wrapper
    return decorator


from phola_park_app.auth.access_control import jwt_access_required
from phola_park_app import create_app,app

def test_something(client):
    response = client.get("/api/v1/protected")
    assert response.status_code == 401

@app.route("/user", methods=["GET"])
@jwt_access_required(min_role="user")
def user_route():
    return {"message": "user"}, 200


@app.route("/admin", methods=["GET"])
@jwt_access_required(min_role="admin", permission="manage_users")
def admin_route():
    return {"message": "admin"}, 200

def test_user_can_access_user_route(client, user_token):
    res = client.get(
        "/user",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 200


def test_user_cannot_access_admin_route(client, user_token):
    res = client.get(
        "/admin",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert res.status_code == 403


def test_admin_can_access_admin_route(client, admin_token):
    res = client.get(
        "/admin",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == 200


def test_missing_token(client):
    res = client.get("/user")
    assert res.status_code == 401


def test_missing_permission(client, admin_token):
    # Admin without permission override
    token = admin_token.replace("manage_users", "")
    res = client.get(
        "/admin",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 403

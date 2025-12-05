from fastapi import Request, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse

from routes.auth_routes import auth_oauth2_scheme
from shared.models.env import EnvSettings

settings = EnvSettings()

async def authentication_middleware(request: Request, call_next):
    from routes.conf import routes_access
    from services.AuthServices import AuthServices

    if request.method == "OPTIONS":
        return await call_next(request)
    
    if any(request.url.path.startswith(path) for path in routes_access.no_auth_routes_list):
        return await call_next(request)

    exclude_paths = routes_access.no_auth_routes_list

    admin_routes = routes_access.admin_routes_list

    if request.url.path in exclude_paths:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Authorization header missing or invalid"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ")[1]
    token = token.strip()

    authServices = AuthServices()

    decoded_token = authServices.decode_jwt_token(token)

    for route in admin_routes:
        if route in request.url.path and decoded_token.user_role != "admin":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Access denied: insufficient privileges"},
                headers={"WWW-Authenticate": "Bearer"},
            )

    user_id = decoded_token.user_id

    if not user_id:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid token"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    request.state.user = user_id
    request.state.user_role = decoded_token.user_role
    request.state.user_email = decoded_token.user_email

    return await call_next(request)


async def get_user_id(token: str = Depends(auth_oauth2_scheme)):
    from services.AuthServices import AuthServices

    authServices = AuthServices()

    decoded_user = authServices.decode_jwt_token(token)

    if not decoded_user:
        return None

    return decoded_user.user_id


def validate_user_role(user_role: str) -> bool:
    permissions = ["admin"]

    if user_role not in permissions:
        return False
    
    return True

import logging

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from cato_server.authentication.create_user import CreateUser, CreateUserData
from cato_server.authentication.session_backend import SessionBackend
from cato_server.configuration.app_configuration import AppConfiguration
from cato_common.domain.auth.email import Email
from cato_common.domain.auth.username import Username
from cato_server.storage.abstract.auth_user_repository import AuthUserRepository

logger = logging.getLogger(__name__)


class AuthBlueprint(APIRouter):
    def __init__(
        self,
        session_backend: SessionBackend,
        auth_user_repository: AuthUserRepository,
        create_user: CreateUser,
        app_configuration: AppConfiguration,
    ):
        super(AuthBlueprint, self).__init__()
        self._session_backend = session_backend
        self._auth_user_repository = auth_user_repository
        self._create_user = create_user
        self._app_configuration = app_configuration

        self._oauth_config = Config(
            environ={
                "KEYCLOAK_CLIENT_ID": self._app_configuration.oidc_configuration.client_id,
                "KEYCLOAK_CLIENT_SECRET": self._app_configuration.oidc_configuration.client_secret.get_secret_value(),
            }
        )
        self._oauth = OAuth(self._oauth_config)

        self._oauth.register(
            name="keycloak",
            server_metadata_url=self._app_configuration.oidc_configuration.well_known_url,
            client_kwargs={"scope": "openid email profile"},
        )

        self.get("/login")(self.login)
        self.get("/auth")(self.auth)

    async def login(self, request: Request):
        redirect_uri = f"{self._app_configuration.public_hostname}:{self._app_configuration.port}/auth"
        return await self._oauth.keycloak.authorize_redirect(request, redirect_uri)

    async def auth(self, request: Request):
        try:
            token = await self._oauth.keycloak.authorize_access_token(request)
        except OAuthError as error:
            logging.error(error)
            return Response(status_code=401)
        user = await self._oauth.keycloak.userinfo(token=token)
        if not user:
            return Response(status_code=404)

        create_user_data = CreateUserData(
            username=Username(user["preferred_username"]),
            fullname=Username(f"{user['given_name']} {user['family_name']}"),
            email=Email(user["email"]),
        )
        auth_user = self._create_user.create_or_update_user(create_user_data)

        session = self._session_backend.create_session(auth_user)
        request.session["session_id"] = str(session.id)

        logger.info('User "%s" signed in', auth_user.username)

        return RedirectResponse(url="/")
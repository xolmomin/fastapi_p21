from starlette.authentication import AuthenticationError, AuthCredentials
from starlette.requests import HTTPConnection

from apps.models import User


class AuthenticationMiddleware:
    def __init__(
            self,
            app,
            backend,
            on_error=None,
    ) -> None:
        self.app = app
        self.backend = backend
        self.on_error = (
            on_error if on_error is not None else self.default_on_error
        )

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)
        try:
            auth_result = await self.backend.authenticate(conn)
        except AuthenticationError as exc:
            response = self.on_error(conn, exc)
            if scope["type"] == "websocket":
                await send({"type": "websocket.close", "code": 1000})
            else:
                await response(scope, receive, send)
            return

        if auth_result is None:
            auth_result = AuthCredentials(), User()  ####################### HERE
        scope["auth"], scope["user"] = auth_result
        await self.app(scope, receive, send)

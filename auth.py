import functools
from aiohttp import BasicAuth, web, hdrs
from aiohttp.web import middleware
import json


@middleware
class BasicAuthMiddleware(object):
    def __init__(self, force=True, realm=''):
        with open('passwords.json') as json_file:
            data = json.load(json_file)
        self.user_pass = data["passwords"]
        self.user = None
        self.force = force
        self.realm = realm

    def parse_auth_header(self, request):
        auth_header = request.headers.get(hdrs.AUTHORIZATION)
        if not auth_header:
            return None
        try:
            auth = BasicAuth.decode(auth_header=auth_header)
        except ValueError:
            auth = None
        return auth

    async def authenticate(self, request):
        auth = self.parse_auth_header(request)
        return (auth is not None
                and await self.check_credentials(auth.login, auth.password,
                                                 request))

    async def check_credentials(self, username, password, request):
        if username is None:
            raise ValueError('username is None')

        if password is None:
            raise ValueError('password is None')

        if [username, password] in self.user_pass:
            self.user = username

        return [username, password] in self.user_pass

    def challenge(self):
        return web.Response(
            body=b'', status=401, reason='UNAUTHORIZED',
            headers={
                hdrs.WWW_AUTHENTICATE: 'Basic realm="%s"' % self.realm,
                hdrs.CONTENT_TYPE: 'text/html; charset=utf-8',
                hdrs.CONNECTION: 'keep-alive'
            }
        )

    def required(self, handler):
        @functools.wraps(handler)
        async def wrapper(*args):
            request = args[-1]
            if await self.authenticate(request):
                return await handler(*args)
            else:
                return self.challenge()

        return wrapper

    async def __call__(self, request, handler):
        if not self.force:
            return await handler(request)
        else:
            if await self.authenticate(request):
                return await handler(request)
            else:
                return self.challenge()

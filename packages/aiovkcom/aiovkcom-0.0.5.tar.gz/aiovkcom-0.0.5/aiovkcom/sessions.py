import aiohttp
import asyncio
import logging
from yarl import URL

from .exceptions import (
    Error,
    OAuthError,
    VKOAuthError,
    InvalidGrantError,
    InvalidUserError,
    VKAPIError,
)
from .parsers import AuthPageParser, AccessPageParser


log = logging.getLogger(__name__)


class Session:
    """A wrapper around aiohttp.ClientSession."""

    CONTENT_TYPE = 'application/json; charset=utf-8'

    __slots__ = ('pass_error', 'session')

    def __init__(self, pass_error=False, session=None):
        self.pass_error = pass_error
        self.session = session or aiohttp.ClientSession()

    def __await__(self):
        return self.authorize().__await__()

    async def __aenter__(self):
        return await self.authorize()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def authorize(self):
        return self

    async def close(self):
        await self.session.close()


class TokenSession(Session):
    """Session for sending authorized requests."""

    URL = 'https://api.vk.com/method/'
    V = '5.101'

    __slots__ = ('access_token', 'v')

    def __init__(self, access_token, v='', pass_error=False, session=None):
        super().__init__(pass_error, session)
        self.access_token = access_token
        self.v = v or self.V

    @property
    def required_params(self):
        """Required parameters."""
        return {'v': self.v, 'access_token': self.access_token}

    async def request(self, method_name, params=()):
        """Sends a request.

        Args:
            method_name (str): method's name.
            params (dict): URL parameters.

        Returns:
            response (dict): JSON object response.

        """

        url = f'{self.URL}/{method_name}'
        params = {k: params[k] for k in params if params[k]}
        params.update(self.required_params)

        async with self.session.get(url, params=params) as resp:
            content = await resp.json(content_type=self.CONTENT_TYPE)

        if self.pass_error:
            response = content
        elif 'error' in content:
            log.error(content['error'])
            raise VKAPIError(content['error'])
        else:
            response = content['response']

        return response


class ImplicitSession(TokenSession):

    OAUTH_URL = 'https://oauth.vk.com/authorize'
    REDIRECT_URI = 'https://oauth.vk.com/blank.html'

    AUTHORIZE_NUM_ATTEMPTS = 1
    AUTHORIZE_RETRY_INTERVAL = 3

    GET_AUTH_DIALOG_ERROR_MSG = 'Failed to open authorization dialog.'
    POST_AUTH_DIALOG_ERROR_MSG = 'Form submission failed.'
    GET_ACCESS_TOKEN_ERROR_MSG = 'Failed to receive access token.'
    POST_ACCESS_DIALOG_ERROR_MSG = 'Failed to process access dialog.'

    __slots__ = ('app_id', 'login', 'passwd', 'scope', 'expires_in')

    def __init__(self, app_id, login, passwd, scope='', v='',
                 pass_error=False, session=None):
        super().__init__('', v, pass_error, session)
        self.app_id = app_id
        self.login = login
        self.passwd = passwd
        self.scope = scope

    @property
    def params(self):
        """Authorization parameters."""
        return {
            'display': 'page',
            'response_type': 'token',
            'redirect_uri': self.REDIRECT_URI,
            'client_id': self.app_id,
            'scope': self.scope,
            'v': self.v,
        }

    async def authorize(self, num_attempts=None, retry_interval=None):
        """OAuth Implicit flow."""

        num_attempts = num_attempts or self.AUTHORIZE_NUM_ATTEMPTS
        retry_interval = retry_interval or self.AUTHORIZE_RETRY_INTERVAL

        for attempt_num in range(num_attempts):
            log.debug(f'getting authorization dialog {self.OAUTH_URL}')
            url, html = await self._get_auth_dialog()

            if url.path == '/authorize':
                log.debug(f'authorizing at {url}')
                url, html = await self._post_auth_dialog(html)

            if url.path == '/authorize' and '__q_hash' in url.query:
                log.debug(f'giving rights at {url}')
                url, html = await self._post_access_dialog(html)
            elif url.path == '/authorize' and 'email' in url.query:
                log.error(f'Invalid login "{self.login}" or password.')
                raise InvalidGrantError()
            elif url.query.get('act') == 'blocked':
                raise InvalidUserError()

            if url.path == '/blank.html':
                log.debug('authorized successfully')
                await self._get_access_token()
                return self

            await asyncio.sleep(retry_interval)
        else:
            log.error(f'{num_attempts} login attempts exceeded.')
            raise OAuthError(f'{num_attempts} login attempts exceeded.')

    async def _get_auth_dialog(self):
        """Return URL and html code of authorization page."""

        async with self.session.get(self.OAUTH_URL, params=self.params) as resp:
            if resp.status == 401:
                error = await resp.json(content_type=self.CONTENT_TYPE)
                log.error(error)
                raise VKOAuthError(error)
            elif resp.status != 200:
                log.error(self.GET_AUTH_DIALOG_ERROR_MSG)
                raise OAuthError(self.GET_AUTH_DIALOG_ERROR_MSG)
            else:
                url, html = resp.url, await resp.text()

        return url, html

    async def _post_auth_dialog(self, html):
        """Submits a form with login and password to get access token.

        Args:
            html (str): authorization page's html code.

        Returns:
            url (URL): redirected page's URL.
            html (str): redirected page's html code.

        """

        parser = AuthPageParser()
        parser.feed(html)
        parser.close()

        form_url, form_data = parser.form
        form_data['email'] = self.login
        form_data['pass'] = self.passwd

        async with self.session.post(form_url, data=form_data) as resp:
            if resp.status != 200:
                log.error(self.POST_AUTH_DIALOG_ERROR_MSG)
                raise OAuthError(self.POST_AUTH_DIALOG_ERROR_MSG)
            else:
                url, html = resp.url, await resp.text()

        return url, html

    async def _post_access_dialog(self, html):
        """Clicks button 'allow' in a page with access dialog.

        Args:
            html (str): html code of the page with access form.

        Returns:
            url (URL): redirected page's URL.
            html (str): redirected page's html code.

        """

        parser = AccessPageParser()
        parser.feed(html)
        parser.close()

        form_url, form_data = parser.form

        async with self.session.post(form_url, data=form_data) as resp:
            if resp.status != 200:
                log.error(self.POST_ACCESS_DIALOG_ERROR_MSG)
                raise OAuthError(self.POST_ACCESS_DIALOG_ERROR_MSG)
            else:
                url, html = resp.url, await resp.text()

        return url, html

    async def _get_access_token(self):
        async with self.session.get(self.OAUTH_URL, params=self.params) as resp:
            if resp.status != 200:
                log.error(self.GET_ACCESS_TOKEN_ERROR_MSG)
                raise OAuthError(self.GET_ACCESS_TOKEN_ERROR_MSG)
            else:
                location = URL(resp.history[-1].headers['Location'])
                url = URL(f'?{location.fragment}')

        try:
            self.access_token = url.query['access_token']
            self.expires_in = url.query['expires_in']
        except KeyError as e:
            raise OAuthError(f'"{e.args[0]}" is missing in the auth response.')

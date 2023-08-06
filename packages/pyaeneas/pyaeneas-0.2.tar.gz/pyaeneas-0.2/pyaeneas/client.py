import asyncio
from aiohttp import client_exceptions, ClientSession, ClientTimeout
from . import exceptions

TIMEOUT = 10


class Aeneas(object):
    """ Aeneas fullnode API client """

    def __init__(self, uri: str = 'ws://localhost:9085/aeneas'):
        """
        Client initialization

        :param uri: WebSocket server uri
        """

        self._socket = None
        self._session = None
        self._uri = uri
        self._response = {}
        self._timeout = ClientTimeout(total=TIMEOUT)

        # create an event loop and WebSocket connection

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._create_socket())

    def __del__(self):
        self._loop.run_until_complete(self._close_socket())
        self._loop.close()

    async def _create_socket(self):
        """ Establish a WebSocket connection """

        self._session = ClientSession(timeout=self._timeout)

        try:
            self._socket = await self._session.ws_connect(self._uri)

        except client_exceptions.ClientConnectorError:
            raise exceptions.AeneasConnectionError('Connection to given uri failed, uri: {}'.format(self._uri))

        except client_exceptions.ServerConnectionError as e:
            raise exceptions.AeneasConnectionError('Server connection error: {}'.format(e))

    async def _close_socket(self):
        """ Close a WebSocket connection """

        if self._socket is not None:
            await self._socket.close()

        await self._session.close()

    async def _request(self, data: dict, reestablish: bool = False) -> None:
        """
        Send request via WebSocket connection

        :param data: request data dictionary
        :param reestablish: indicate attempt to reestablish connection
        """

        try:
            await self._socket.send_json(data)
            self._response = await self._socket.receive_json()

        except client_exceptions.ServerConnectionError as e:
            raise exceptions.AeneasConnectionError('Server connection error: {}'.format(e))

        except TypeError:
            if reestablish:
                msg = 'The server closed the connection. Attempt to re-establish connection failed.'
                raise exceptions.AeneasConnectionError(msg)

            await self._close_socket()
            await self._create_socket()
            await self._request(data, reestablish=True)

    def _parse_errors(self):
        """ Parse Aeneas fullnode API response errors """

        if not len(self._response):
            return

        if self._response['action'] == 'ErrorResponse':
            raise exceptions.AeneasActionError('Wrong action, message: {}'.format(self._response['msg']))

        if self._response.get('status') == 'error':
            data = self._response['exception']
            raise exceptions.AeneasResponseError(data['text'], data['sqlCode'])

    def execute(self, action: str, params: dict = None) -> dict:
        """
        Make request with event loop

        :param action: Aeneas fullnode API action name
        :param params: dictionary with request parameters
        :return: json response
        """

        data = {'msg': {'action': action}}

        if params is not None:
            data['msg'].update(params)

        self._loop.run_until_complete(self._request(data))
        self._parse_errors()
        return self._response

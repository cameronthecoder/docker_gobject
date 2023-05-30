"""
A single ``Session`` object is shared across all modules and inherits the methods and properties from the ``Soup.Session`` class.

"""
import logging
import gi
import json

gi.require_version("Soup", "3.0")

from gi.repository import GLib, Soup, Gio
from docker_gobject.authentication import AuthenticationMethod

class Session(Soup.Session):
    """
    docker_gobject session handler
    """

    instance: Soup.Session = None
    cancellable: Gio.Cancellable = Gio.Cancellable().new()
    socket: Gio.UnixSocketAddress = None
    authentication_method: AuthenticationMethod = AuthenticationMethod.SOCKET
    api_url: str

    def __init__(self):
        Soup.Session.__init__(self)
        self.set_timeout(0)
        self.set_idle_timeout(0)

    @staticmethod
    def new() -> 'Session':
        """Create a new instance of Session."""
        sock = Gio.UnixSocketAddress.new("/run/docker.sock")
        s_session = Soup.Session(remote_connectable=sock)
        s_session.__class__ = Session
        return s_session

    @staticmethod
    def get() -> 'Session':
        """Return an active instance of Session."""
        if Session.instance is None:
            Session.instance = Session.new()
        return Session.instance

    @classmethod
    def set_authentication_method(cls, auth: AuthenticationMethod):
        """Set authentication for the session."""
        cls.authentication_method = auth

    @classmethod
    def set_api_url(cls, api_url: str):
        """Set the API URL for the session."""
        cls.api_url = api_url

    @classmethod
    def set_socket(cls, socket: Gio.UnixSocketAddress):
        cls.socket = socket
        cls.remote_connectable = socket



    def make_api_call(self, url, callback):
        def on_response(session, result, msg):
            data = success = error = None
            try:
                resp = session.send_and_read_finish(result)
                data = resp.get_data()
                success = True
            except Exception as e:
                logging.warning(e)
                error = e
            callback(success, error, data)

        msg = Soup.Message.new("GET", url)
        self.send_and_read_async(
            msg, GLib.PRIORITY_DEFAULT, self.cancellable, on_response, msg
        )



class ResponseError(Exception):
    """Exception raised when response fails."""

    def __init__(self, cause, message='Response has failed'):
        self.cause = cause
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self.cause}'


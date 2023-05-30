import gi, logging, json

gi.require_version("Soup", "3.0")

from gi.repository import GObject, Gio, Soup, GLib
from docker_gobject.session import Session
from docker_gobject.containers import Containers
from docker_gobject.authentication import AuthenticationMethod
from docker_gobject.monitor import EventMonitor

class DockerClient(GObject.Object):
    __gtype_name__ = "DockerClient"

    authentication_method: AuthenticationMethod
    """
    Authentication method for connecting to the Docker Engine
    """
    url: str = "http://localhost:2375"
    """
    If you are using the (TCP)`docker_gobject.authentication.AuthenticationMethod.TCP` protocol to connect to the Docker Engine, this is the API URL that will be used.
    """
    containers: Containers
    """Containers"""
    session: Session
    "Session"
    event_monitor: EventMonitor
    "Event Monitor"

    def __init__(self, authentication_method = AuthenticationMethod.SOCKET, url = "http://localhost:2375", *args, **kwargs):
        super(DockerClient, self).__init__(*args, **kwargs)
        self.cancellable = Gio.Cancellable().new()
        self.session = Session.get()
        self.session.set_authentication_method(authentication_method)
        self.session.set_api_url(url)
        if authentication_method is AuthenticationMethod.SOCKET:
            sock = Gio.UnixSocketAddress.new("/run/docker.sock")
            self.session.set_socket(sock)
            self.session.set_timeout(0)  # docker engine monitoring endpoint
            self.session.set_idle_timeout(0)
            self.session.set_api_url("http://localhost")
        self.containers = Containers()
        self.event_monitor = EventMonitor()
        #self.monitor_events()

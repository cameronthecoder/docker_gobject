"""
# Containers
"""
import gi, json
from typing import Callable
gi.require_version("Soup", "3.0")
gi.require_version("Gtk", "4.0")
gi.require_version("Json", "1.0")
from docker_gobject.session import Session
from docker_gobject.container import Container
from gi.repository import Gio, Soup, GLib, Json, Gtk, GObject


class Containers(GObject.Object):
    """
    Class to control containers
    """

    session = Session.get()

    def __init__(self, *args, **kwargs):
        GObject.Object.__init__(self)

    def list(self, callback: Callable[[bool, bool, bytes]]):
        self.session.make_api_call(self.session.api_url + "/containers/json?all=true", callback)

    def from_json(self, data) -> Gtk.ListStore:
        """
        Converts the raw JSON container data into a Gtk.ListStore
        """
        containers = Gtk.ListStore.new((Container,))
        d = json.loads(data.decode())
        for container in d:
            containers.append([Container.from_json(container)])
        return containers

    def get(self, name_or_id, callback: Callable[[bool, bool, bytes]]):
        self.session.make_api_call(self.session.api_url + "/containers/" + name_or_id + "/json", callback)

    def tail_togs(self, id, callback):
        self.session.connect_to_websocket(f"ws://127.0.0.1:5555/containers/{id}/attach/ws?logs=true&stream=true", callback)

import dbus
from dbus.mainloop.glib import DBusGMainLoop
try:
    from docker_gobject.client import DockerClient
    from docker_gobject.authentication import AuthenticationMethod
except:
    print("DOCKER GOBJECT NOT INSTALLED")

from gi.repository import Gio, GLib
client = DockerClient(AuthenticationMethod.SOCKET)
def list_callback(success, error, data):
    containers = client.containers.from_json(data)

    for container in containers:
        print(container[0].id)


def pulled_image(source, image):
    print(source)
    print(image)

client.containers.list(list_callback)
client.event_monitor.monitor_events()
client.event_monitor.connect("image_pull", pulled_image)


if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()
    try:
        GLib.MainLoop().run()
    except KeyboardInterrupt:
        GLib.MainLoop().quit()



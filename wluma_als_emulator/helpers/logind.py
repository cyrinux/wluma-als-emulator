import dbus
import threading
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
from time import sleep


class DbusLogindThread(threading.Thread):
    """
    DBUS threads that detect if laptop back from suspend
    """

    def __init__(self, config, strategy, event):
        threading.Thread.__init__(self)
        self.config = config
        self.strategy = strategy
        self.event = event

    def handle_sleep_callback(self, sleeping):
        if sleeping:
            if self.config.verbose:
                print("System going to hibernate or sleep")
        else:
            print("System just resumed from hibernate or suspend, polling in 3s...")
            sleep(2)
            self.strategy.run()
            print("Quick polling done")

    def run(self):
        DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
        bus.add_signal_receiver(
            self.handle_sleep_callback,
            self.event,
            "org.freedesktop.login1.Manager",
            "org.freedesktop.login1",
        )

        self.loop = GLib.MainLoop()
        self.loop.run()


class SleepDetect:
    """
    Detect if the computer is back from suspend and trigger the polling
    """

    def __init__(self, strategy):
        self.config = strategy.config
        self.logind = DbusLogindThread(self.config, strategy, "PrepareForSleep")

    def run(self):
        self.logind.start()

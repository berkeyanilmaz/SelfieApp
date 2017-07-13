#!/usr/bin/env python

import sys
import qi
import os


class Selfie(object):
    subscriber_list = []
    loaded_topic = ""

    def __init__(self, application):
        # Get session
        self.application = application
        self.session = application.session
        self.service_name = self.__class__.__name__

        # Get logger -> stored in: /var/log/naoqi/servicemanager/{application id}.{service name}
        self.logger = qi.Logger(self.service_name)
        # Do initialization before the service is registered to NAOqi
        self.logger.info("Initializing...")

        # Autonomous Life
        self.life = self.session.service("ALAutonomousLife")

        # Memory
        self.memory = self.session.service("ALMemory")
        self.logger.info("Initializing - ALMemory")

        # Create Signals
        self.create_signals()

        self.logger.info("Initialized!")



    @qi.nobind
    def create_signals(self):
        # Create events and subscribe them here
        self.logger.info("Creating events...")
        # TODO: Create events

        self.logger.info("Subscribed to all events.")

    @qi.nobind
    def disconnect_signals(self):
        self.logger.info("Deleting events...")
        for sub, i in self.subscriber_list:
            try:
                sub.signal.disconnect(i)
            except Exception, e:
                self.logger.info("Error unsubscribing: {}".format(e))
        self.logger.info("Unsubscribe done!")

    # Signal related methods end

    # ---------------------------

    # Event CallBacks Start

    # Event CallBacks End

    # -------------------

    # Initiation methods for services start

    @qi.nobind
    def show_screen(self):
        folder = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
        self.logger.info("Loading tablet page for app: {}".format(folder))
        try:
            ts = self.session.service("ALTabletService")
            ts.loadApplication(folder)
            ts.showWebview()

            self.logger.info("Tablet loaded.")
        except Exception, e:
            self.logger.error("Error starting tablet page{}".format(e))

    @qi.nobind
    def hide_screen(self):
        self.logger.info("Stopping tablet")
        try:
            ts = self.session.service("ALTabletService")
            ts.hideWebview()
            self.logger.info("Tablet stopped.")
        except Exception, e:
            self.logger.error("Error hiding tablet page{}".format(e))

    @qi.nobind
    def start_dialog(self):
        self.logger.info("Loading dialog")
        dialog = self.session.service("ALDialog")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        topic_path = os.path.realpath(os.path.join(dir_path, "selfie", "selfie_enu.top"))
        self.logger.info("File is: {}".format(topic_path))
        try:
            self.loaded_topic = dialog.loadTopic(topic_path)
            dialog.activateTopic(self.loaded_topic)
            dialog.subscribe(self.service_name)
            self.logger.info("Dialog loaded!")
        except Exception, e:
            self.logger.info("Error while loading dialog: {}".format(e))
        dialog.gotoTag("start", "barcode_detected")

    @qi.nobind
    def stop_dialog(self):
        self.logger.info("Unloading dialog")
        try:
            dialog = self.session.service("ALDialog")
            dialog.unsubscribe(self.service_name)
            dialog.deactivateTopic(self.loaded_topic)
            dialog.unloadTopic(self.loaded_topic)
            self.logger.info("Dialog unloaded!")
        except Exception, e:
            self.logger.info("Error while unloading dialog: {}".format(e))

    # Initiation methods for services end

    # -----------------------------------

    # App Start/End Methods start

    @qi.nobind
    def start_app(self):
        # do something when the service starts
        self.logger.info("Starting app...")
        self.show_screen()
        self.start_dialog()
        self.preferences.update()
        self.connect_to_preferences()
        self.logger.info("Started!")

    @qi.nobind
    def stop_app(self):
        # To be used if internal methods need to stop the service from inside.
        # external NAOqi scripts should use ALServiceManager.stopService if they need to stop it.
        self.logger.info("Stopping service...")
        self.application.stop()
        self.logger.info("Stopped!")

    @qi.nobind
    def cleanup(self):
        # called when your module is stopped
        self.logger.info("Cleaning...")

        self.disconnect_signals()
        self.stop_dialog()
        self.hide_screen()

        self.logger.info("Cleaned!")
        try:
            self.audio.stopMicrophonesRecording()
        except Exception, e:
            self.logger.info("Microphone already closed")



if __name__ == "__main__":
    # with this you can run the script for tests on remote robots
    # run : python main.py --qi-url 123.123.123.123
    app = qi.Application(sys.argv)
    app.start()
    service_instance = Selfie(app)
    service_id = app.session.registerService(service_instance.service_name, service_instance)
    service_instance.start_app()
    app.run()
    service_instance.cleanup()
    app.session.unregisterService(service_id)
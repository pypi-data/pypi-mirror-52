# coding=utf-8
"""
Demo for the Speech API module
"""
# pylint: disable=c-extension-no-member, no-name-in-module, no-self-use
import sys
import logging
import PySide2.QtCore
from sksurgeryspeech.algorithms import voice_recognition_service as speech_api

LOGGER = logging.getLogger("voice_recognition_logger")


class VoiceListener(PySide2.QtCore.QObject):

    """
    Class which contains the slots for the demo application
    """

    @PySide2.QtCore.Slot()
    def on_start_listen(self):
        """
        Slot when the user says the keyword
        """
        LOGGER.info("Listening for command")

    @PySide2.QtCore.Slot()
    def on_next(self):
        """
        Slot for next signal
        """
        LOGGER.info("Next signal caught")

    @PySide2.QtCore.Slot()
    def on_previous(self):
        """
        Slot for the previous signal
        """
        LOGGER.info("Previous signal caught")

    @PySide2.QtCore.Slot()
    def on_undo(self):
        """
        Slot for the undo signal
        """
        LOGGER.info("Undo signal caught")

    @PySide2.QtCore.Slot()
    def on_quit(self):
        """
        Slot for the quit signal
        Quits application
        """
        LOGGER.info("Quit signal caught... Exit application")
        PySide2.QtCore.QCoreApplication.quit()

    @PySide2.QtCore.Slot()
    def on_voice_signal(self, input_string):
        """
        Slot for the voice signal,
        which just contains the microphone input as string
        """
        LOGGER.info("Generic voice signal caught with input: %s", input_string)

    @PySide2.QtCore.Slot()
    def on_google_api_not_understand(self):
        """
        Slot if the google api doesn't understand audio
        """
        LOGGER.info("Google Speech Recognition could not understand audio")

    @PySide2.QtCore.Slot()
    def on_google_api_request_failure(self, exception):
        """
        Slot if something with the google api went wrong
        """
        LOGGER.info("Could not request results from Google Speech "
                    "Recognition service; %s", exception)

    @PySide2.QtCore.Slot()
    def on_start_processing_request(self):
        """
        Slot when the request is sent to Google API
        """
        LOGGER.info("Processing...")

    @PySide2.QtCore.Slot()
    def on_end_processing_request(self):
        """
        Slot when the processing of the request is done
        """
        LOGGER.info("Processing done")


class SpeechRecognitionDemo(PySide2.QtCore.QObject):

    """
    Demo class for the Speech API module
    """
    def __init__(self):
        """
        Constructor.
        """
        super(SpeechRecognitionDemo, self).__init__()

        #  set up the logger
        voice_recognition_logger = logging.getLogger("voice_recognition_logger")
        voice_recognition_logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        file_handler = logging.FileHandler('voice_recognition_log.log')
        file_handler.setLevel(logging.INFO)
        voice_recognition_logger.addHandler(console_handler)
        voice_recognition_logger.addHandler(file_handler)

        #  create VoiceRecognitionService()
        self.voice_recognition = speech_api\
            .VoiceRecognitionService(timeout_for_command=3)
        #  create VoiceListener() which in this example has all the slots to
        #  react to the signals from the VoiceRecognitionService()
        self.listener = VoiceListener()

        #  Move the VoiceRecognitionService() to a separate thread so it doesn't
        #  block the main thread
        self.listener_thread = PySide2.QtCore.QThread()
        self.voice_recognition.timer.moveToThread(self.listener_thread)
        self.voice_recognition.moveToThread(self.listener_thread)
        self.listener_thread.started.connect(self.voice_recognition.run)

        #  connect the Signals emitted by the VoiceRecognitionService()
        #  with the Slots of the VoiceListener
        self.voice_recognition.start_listen\
            .connect(self.listener.on_start_listen)
        self.voice_recognition.next.connect(self.listener.on_next)
        self.voice_recognition.previous.connect(self.listener.on_previous)
        self.voice_recognition.undo.connect(self.listener.on_undo)
        self.voice_recognition.quit.connect(self.listener.on_quit)
        self.voice_recognition.voice_command\
            .connect(self.listener.on_voice_signal)
        self.voice_recognition.google_api_not_understand\
            .connect(self.listener.on_google_api_not_understand)
        self.voice_recognition.google_api_request_failure\
            .connect(self.listener.on_google_api_request_failure)
        self.voice_recognition.start_processing_request\
            .connect(self.listener.on_start_processing_request)
        self.voice_recognition.end_processing_request\
            .connect(self.listener.on_end_processing_request)

    def run_demo(self):
        """
        Entry point to run the demo
        """
        #  instantiate the QCoreApplication
        app = PySide2.QtCore.QCoreApplication()
        #  this is the main call to start the background thread listening
        self.listener_thread.start()
        #  start the application, meaning starting the infinite Event Loop which
        #  stops when the user says "start" followed by "quit"
        return sys.exit(app.exec_())

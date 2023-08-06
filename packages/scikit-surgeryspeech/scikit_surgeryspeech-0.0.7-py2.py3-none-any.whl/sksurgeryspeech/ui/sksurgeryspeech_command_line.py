# coding=utf-8

"""Command line processing"""


import argparse
from sksurgeryspeech import __version__
from sksurgeryspeech.ui import sksurgeryspeech_demo


def main(args=None):
    """Entry point for scikit-surgeryspeech application"""

    parser = argparse.ArgumentParser(description='scikit-surgeryspeech')

    version_string = __version__
    friendly_version_string = version_string if version_string else 'unknown'
    parser.add_argument(
        "--version",
        action='version',
        version='scikit-surgeryspeech version ' + friendly_version_string)

    args = parser.parse_args(args)

    demo = sksurgeryspeech_demo.SpeechRecognitionDemo()
    demo.run_demo()

#!/usr/bin/env python3
from setuptools import find_packages, setup

setup(
        name='idris',
        version='0.0.1',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
          'SpeechRecognition',
          'google-cloud-speech',
          'oauth2client',
          'simpleaudio',
          'pyaudio',
          'google-auth'
        ],
    )

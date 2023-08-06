import logging
import os
import pytest
from flask import Flask, request, redirect, url_for, send_from_directory


_moduleLogger = logging.getLogger(__name__)
_moduleLogger.addHandler(logging.NullHandler())

_base_dir = os.path.dirname(os.path.realpath(__file__))


def _get_cwd():
    path = os.getcwd()
    common_prefix = os.path.commonprefix([path, _base_dir])
    if not common_prefix:
        return '.'
    return os.path.relpath(path, _base_dir) or '.'


class DefaultFlaskApp(object):
    def __init__(self, root_folder=None):
        self._app = Flask(__name__)
        self._app.debug = True

        if not root_folder:
            root_folder = _get_cwd()
        self._app.static_folder = root_folder

        @self._app.route('/')
        def handle_index():
            return self.handle_path('/')

        @self._app.route('/<path:file>')
        def handle_file(file):
            return self.handle_path(file)

    @property
    def flask(self):
        return self._app


    def handle_path(self, path):
        '''Handle any path passed to the Flask app

        Args:
            path (str): The url short path to the desired file
        
        Returns:
            Flask.send_static_file: Response
        '''
        # send_static_file will guess the correct MIME type
        # _moduleLogger.debug('Path: %s', path)
        _moduleLogger.debug('File: %s', path)
        # dest = os.path.join(path, file.strip('/'))
        dest = path
        if dest.endswith('/'):
            segments = list(path.strip('/').split('/', False))
            segments.append('index.html')
            dest = '/'.join(segments).lstrip('/')
        _moduleLogger.debug('Joined: %s', dest)
        return self._app.send_static_file(dest)

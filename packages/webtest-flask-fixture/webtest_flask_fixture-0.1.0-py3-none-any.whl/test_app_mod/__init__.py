import logging
import os
import pytest

_moduleLogger = logging.getLogger(__name__)
_moduleLogger.addHandler(logging.NullHandler())

_base_dir = os.path.dirname(os.path.realpath(__file__))


def _get_cwd():
    path = os.getcwd()
    common_prefix = os.path.commonprefix([path, _base_dir])
    if not common_prefix:
        return '.'
    return os.path.relpath(path, _base_dir) or '.'


def _flask_app():
    from flask import Flask, request, redirect, url_for, send_from_directory
    app = Flask(__name__)
    app.debug = True
    app.static_folder = _get_cwd()

    # Routes
    @app.route('/')
    def root():
        _moduleLogger.debug('Serving Index')
        # _file = os.path.join(cwd, 'index.html')
        return app.send_static_file('index.html')

    @app.route('/<path:file>')
    def static_proxy(file):
        # send_static_file will guess the correct MIME type
        # _moduleLogger.debug('Path: %s', path)
        _moduleLogger.debug('File: %s', file)
        # dest = os.path.join(path, file.strip('/'))
        dest = file
        if dest.endswith('/'):
            segments = list(file.split('/', False))
            segments.append('index.html')
            dest = os.path.join(*segments)
        _moduleLogger.debug('Joined: %s', dest)
        return app.send_static_file(dest)

    return app


@pytest.fixture
def test_app():
    from webtest import TestApp
    flask_app = _flask_app()
    app = TestApp(flask_app)
    return app

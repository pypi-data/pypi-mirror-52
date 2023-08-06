from webtest_flask_fixture import fixture_template
import pytest

@pytest.fixture
def test_app():
    from webtest import TestApp

    wrapper = fixture_template.DefaultFlaskApp()

    flask_app = wrapper.flask
    app = TestApp(flask_app)
    return app

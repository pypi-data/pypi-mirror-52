import os.path
import pytest

_base_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def mock_site(mocker):
    import webtest_flask_fixture.test_app_mod
    mock = mocker.patch('webtest_flask_fixture.test_app_mod._get_cwd',
                        return_value=os.path.join(_base_dir, 'test_files'))
    return mock

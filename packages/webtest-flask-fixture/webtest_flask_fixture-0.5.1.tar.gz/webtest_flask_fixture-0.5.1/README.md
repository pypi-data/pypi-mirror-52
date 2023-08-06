# webtest-flask-fixture
Providing a fixture for static websites to use WebTest through Flask

## Why WebTest?
[WebTest](https://pypi.org/project/WebTest/) provides a great interface for testing websites including button/link and form interactions.

## Why Flask?
[Flask](https://pypi.org/project/Flask/) comes with an extremely light-weight dev server that can server up arbitrary pages (static or coded) relatively easily.

## Let's put the two together!!
And this package is born. The objective is to provide a `PyTest.fixture` that allows for quickly testing static web sites, or through customizing the template, a fixture that can be used to test more complex web sites.


# Installation

`pip install webtest-flask-fixture`

or, from source:

`pip install git+git://github.com/mshafer1/webtest-flask-fixture.git@0.5.1`


# Useage

Start writing a PyTest test, and use `webtest_flask_fixture.test_app` to load pages.

Example:

```python
from webtest_flask_fixture import test_app

def test_can_load_test_index(test_app):
    # Act
    resp = test_app.get('/')

    # Assert
    assert resp.status_int == 200
    assert resp.content_type == 'text/html'
    assert 'Hello, World!' in resp  # string must be present in body
```

<!-- use absolute URL as this is also used for the PyPi docs -->
More examples in [examples](https://github.com/mshafer1/webtest-flask-fixture/tree/master/webtest_flask_fixture/examples/test_files).

# Future
Currently WebTest does not execute JS in the page, we would like to also integrate selenium such that a user can apply our PyTest fixture and get a full experience.

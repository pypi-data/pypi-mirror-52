# webtest-flask-fixture
Providing a fixture for static websites to use WebTest through Flask

## Why WebTest?
[WebTest](https://pypi.org/project/WebTest/) provides a great interface for testing websites including button/link and form interactions.

## Why Flask?
[Flask](https://pypi.org/project/Flask/) comes with an extremely light-weight dev server that can server up arbitrary pages (static or coded) relatively easily.

## Let's put the two together!!
And this package is born. The objective is to provide a `PyTest.fixture` that allows for quickly testing static web sites, or through customizing the template, a fixture that can be used to test more complex web sites.


# Installation
coming . . .


# Future
Currently WebTest does not execute JS in place, we would like to also integrate selenium such that a user can apply our PyTest fixture and get a full experience.

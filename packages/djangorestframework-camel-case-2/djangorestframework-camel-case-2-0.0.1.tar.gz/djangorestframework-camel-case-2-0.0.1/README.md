# Django REST Framework JSON CamelCase

Camel case JSON support for Django REST framework.

## Installation

At the command line::

```
pip install djangorestframework-camel-case-2
```

Add the render and parser to your django settings file.


```python
# ...
REST_FRAMEWORK = {

    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
        # Any other renders
    ),

    'DEFAULT_PARSER_CLASSES': (
        # If you use MultiPartFormParser or FormParser, we also have a camel case version
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        # Any other parsers
    ),
}
# ...
```

## Swapping Renderer

By default the package uses `rest_framework.renderers.JSONRenderer`. If you want
to use another renderer (the only possible alternative is
`rest_framework.renderers.UnicodeJSONRenderer`, only available in DRF < 3.0), you must specify it in your django
settings file.

```
# ...
JSON_CAMEL_CASE = {
    'RENDERER_CLASS': 'rest_framework.renderers.UnicodeJSONRenderer'
}
# ...
```

## Underscoreize Options

As raised in https://github.com/krasa/StringManipulation/issues/8#issuecomment-121203018
there are two conventions of snake case.

```
# Case 1 (Package default)
v2Counter -> v_2_counter
fooBar2 -> foo_bar_2

# Case 2
v2Counter -> v2_counter
fooBar2 -> foo_bar2
```

By default, the package uses the first case. To use the second case, specify it in your django settings file.

```python
REST_FRAMEWORK = {
    # ...
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },
    # ...
}
```

## Running Tests

To run the current test suite, execute the following from the root of he project::

```
make test
```

## License

* Free software: BSD license

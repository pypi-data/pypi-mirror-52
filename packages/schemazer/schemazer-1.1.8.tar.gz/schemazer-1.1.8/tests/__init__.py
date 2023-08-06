from schemazer.commons.headers import AuthHeaders
from schemazer import RequestErrors
from schemazer.base import SchemazerMethod
from schemazer.commons.errors import AuthErrors
from schemazer.commons.limits import AllLimit
from schemazer.commons.parameters import AuthParameters


class TestMethodsGroup:
    _name = 'auth'
    test_method = SchemazerMethod(
        name='test_method',
        description='Test method',
        parameters=[
            AuthParameters.Email(),
        ],
        errors=[RequestErrors.BadRequest,
                AuthErrors.UserNotFound],
        limits=[AllLimit()]
    )
    test_headers_method = SchemazerMethod(
        name='test_method',
        description='Test method',
        parameters=[
            AuthParameters.Email(),
        ],
        errors=[RequestErrors.BadRequest,
                AuthErrors.UserNotFound],
        limits=[AllLimit()],
        headers=[AuthHeaders.Apikey()]
    )


class TestSchema:
    test = TestMethodsGroup

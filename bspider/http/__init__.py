from .request import Request
from .response import Response

ERROR_REQUEST = Request('bspider://error')

ERROR_RESPONSE = Response(
        url='bspider://error',
        status=599,
        request=ERROR_REQUEST
    )

__all__ = ['Request', 'Response', 'ERROR_RESPONSE']

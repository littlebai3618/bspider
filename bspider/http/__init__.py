from .request import Request
from .response import Response

ERROR_RESPONSE = Response(
        url='bspider://error',
        status=599,
        request=Request('bspider://error')
    )

__all__ = ['Request', 'Response', 'ERROR_RESPONSE']

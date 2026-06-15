from view_models import HTTPRequest
from services import HTTPParser
from core import BigLogger


logger = BigLogger(__name__)

class BigRagaHTTPRouter:

    @staticmethod
    @logger.error_decorator()
    def load_routing_table():
        pass

    @staticmethod
    @logger.error_decorator()
    def route_request(request: HTTPRequest):
        pass

    
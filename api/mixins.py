"""
Api mixins
"""
from django.conf import settings


class ResponseDataWrapperMixin(object):
    """
    Success or fail wrapper of response data
    """
    def finalize_response(self, request, response, *args, **kwargs):
        """
        Finalizing response before return
        """
        response = super(ResponseDataWrapperMixin, self).finalize_response(
            request, response, *args, **kwargs)
        if response.status_code in settings.SUCCESS_STATUS_CODES:
            response.data = {
                "status": "success",
                "data": response.data
            }
            return response
        if response.status_code in settings.FAIL_STATUS_CODES:
            response.data = {
                "status": "fail",
                "data": response.data
            }
            return response
        return response
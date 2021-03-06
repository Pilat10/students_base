"""
Api mixins module
"""
SUCCESS_STATUS_CODES = (
    200,
    201,
    204,
)

FAIL_STATUS_CODES = (
    480,
    400,
    401,
    403,
    404,
    405,
)
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
        if response.status_code in SUCCESS_STATUS_CODES:
            response.data = {
                "status": "success",
                "data": response.data
            }
            return response
        if response.status_code in FAIL_STATUS_CODES:
            response.data = {
                "status": "fail",
                "data": response.data
            }
            return response
        return response


class ResponseDataWrapperMixinSuccess(object):
    """
    Success or fail wrapper of response data
    """
    def finalize_response(self, request, response, *args, **kwargs):
        """
        Finalizing response before return
        """
        response = super(ResponseDataWrapperMixinSuccess, self).\
            finalize_response(request, response, *args, **kwargs)
        if response.status_code in SUCCESS_STATUS_CODES:
            response.data = {
                "success": True,
                "data": response.data
            }
            return response
        if response.status_code in FAIL_STATUS_CODES:
            response.data = {
                "success": False,
                "data": response.data
            }
            return response
        return response

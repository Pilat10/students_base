"""
Api mixins module
"""


class ResponseDataWrapperMixin(object):
    """
    Success or fail wrapper of response data
    """
    envelope_key = "status"
    success_value = "success"
    fail_value = "fail"

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Finalizing response before return
        """
        response = super().finalize_response(request, response, *args, **kwargs)
        if 200 <= response.status_code < 300:
            value = self.success_value
        elif 400 <= response.status_code < 500:
            value = self.fail_value
        else:
            return response
        response.data = {
            self.envelope_key: value,
            "data": response.data,
        }
        return response


class ResponseDataWrapperMixinSuccess(ResponseDataWrapperMixin):
    """
    Success or fail wrapper of response data
    """
    envelope_key = "success"
    success_value = True
    fail_value = False

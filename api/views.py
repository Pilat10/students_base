"""
Api views module
"""
# from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.views import APIView


class ApiRootView(APIView):
    """
    Root endpoint
    """
    def get(self, request, format=None):
        """
        Available endpoints
        """
        # response = OrderedDict([
        #     ('Upload image', reverse(
        #         'api:update_media',
        #         request=request,
        #         format=format,
        #         kwargs={"pk": media_id}
        #     )
        #     ),
        # ])
        return Response(None)
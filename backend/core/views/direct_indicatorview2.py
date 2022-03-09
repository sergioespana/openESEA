from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from ..models import DirectIndicator
from ..serializers import DirectIndicatorSerializer2


class DirectIndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = DirectIndicatorSerializer2

    # [GET] request for direct indicators
    def get_queryset(self):
        return DirectIndicator.objects.filter(method=self.kwargs['method_pk'])
    
    # [POST] request for direct indicators
    def create(self, request, method_pk):
        # request.data is the object you want to save to the backend. ['method'] = int(method_pk) adds direct indicator to the correct method based on url pk (added in urlpatterns in urls.py).
        request.data['method'] = int(method_pk)
        # call to serialize or deserialize data
        serializer = DirectIndicatorSerializer2(data=request.data)
        # check if all required fields are present in request and if given fields are valid. If not, raise exception.
        serializer.is_valid(raise_exception=True)
        # call function in serializer to save data to database
        serializer.save()
        # return serializer object
        return Response(serializer.data)
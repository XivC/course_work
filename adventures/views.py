from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from adventures.models import Adventure
from adventures.serializers import AdventureSerializer
from adventures.serializers import EditAdventureSerializer
from adventures.services import AdventureStarter


class AdventureViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    queryset = Adventure.objects.all()
    serializer_class = AdventureSerializer

    @action(methods=['post'], detail=False, url_path='start')
    @swagger_auto_schema(request_body=EditAdventureSerializer, responses={
        200: AdventureSerializer()
    })
    def start(self, request, *args, **kwargs):
        serializer = EditAdventureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        adventure = AdventureStarter(data=serializer.validated_data)()
        return Response(AdventureSerializer(instance=adventure).data, status=201)

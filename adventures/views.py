from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from adventures.models import Adventure
from adventures.serializers import AdventureSerializer
from adventures.serializers import EditAdventureSerializer
from adventures.services import AdventureStarter, AdventureStepper
from battles.models import Battle
from battles.serializers import BattleSerializer


class AdventureViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    queryset = Adventure.objects.all().order_by('-created_at')
    serializer_class = AdventureSerializer

    @property
    def adventure(self):
        return get_object_or_404(Adventure.objects.all(), pk=self.kwargs.get('pk'))

    @action(methods=['post'], detail=False, url_path='start')
    @swagger_auto_schema(request_body=EditAdventureSerializer, responses={
        200: AdventureSerializer()
    })
    def start(self, request, *args, **kwargs):
        serializer = EditAdventureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        adventure = AdventureStarter(data=serializer.validated_data)()
        return Response(AdventureSerializer(instance=adventure).data, status=201)

    @action(methods=['post'], detail=True, url_path='step', )
    @swagger_auto_schema(request_body=no_body, responses={
        200: BattleSerializer()
    })
    def step(self, request, *args, **kwargs):

        battle = AdventureStepper(adventure=self.adventure)()
        return Response(BattleSerializer(instance=battle).data, status=201)

    @action(methods=['get'], detail=True, url_path='battles', )
    @swagger_auto_schema(request_body=no_body, responses={
        200: BattleSerializer(many=True)
    })
    def battles(self, request, *args, **kwargs):

        battles = Battle.objects.filter(adventure=self.adventure)
        return Response(BattleSerializer(instance=battles, many=True).data, status=201)


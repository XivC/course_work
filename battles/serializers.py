from rest_framework import serializers

from affects.serializers import WeaponSerializer
from battles.models import Battler


class BattlerSerializer(serializers.ModelSerializer):
    weapon = WeaponSerializer(read_only=True)

    # TODO: add creature serializer

    class Meta:
        model = Battler
        fields = [
            'creature',
            'weapon',
        ]

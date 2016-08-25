from rest_framework import serializers

from api.models import Team

class PointTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'game_played', 'win', 'lost', 'draw', 'goal_fo', 'goal_against', 'point')

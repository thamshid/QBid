import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Team, Match, Player
from api.serializer import PointTableSerializer, MatchSerializer, PlayerSerializer

log = logging.getLogger(__name__)


class Login(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            try:
                team = Team.objects.get(username=username, password=password)
            except:
                return Response({"status": -1, "message": "Invalid username or password"})
            return Response({"status": 1, "message": "Login success"})
        except:
            pass


class PointTable(APIView):
    def get(self, request):
        try:
            queryset = Team.objects.all().order_by('-point', '-goal_fo', 'goal_against', 'game_played')
            data = PointTableSerializer(queryset, many=True)
            return Response(data.data)
        except Exception as e:
            log.error(e.message)
            return Response({"status": -1, "message": str(e.message)})


class LastMatches(APIView):
    def post(self, request):
        try:
            numbers = int(request.data.get('numbers', 3))
            queryset = Match.objects.filter(match_status=2).order_by('-date')[:numbers]
            data = MatchSerializer(queryset, many=True)
            return Response(data.data)
        except Exception as e:
            log.error(e.message)
            return Response({"status": -1, "message": str(e.message)})


class LeadingGoalScorer(APIView):
    def post(self, request):
        try:
            numbers = int(request.data.get('numbers', 3))
            queryset = Player.objects.filter(no_of_goals__gt=0).order_by('-no_of_goals')[:numbers]
            data = PlayerSerializer(queryset, many=True)
            return Response(data.data)
        except Exception as e:
            log.error(e.message)
            return Response({"status": -1, "message": str(e.message)})


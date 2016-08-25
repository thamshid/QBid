import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Team
from api.serializer import PointTableSerializer

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
        except exceptions as e:
            log.error(e.message)


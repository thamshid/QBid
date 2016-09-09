import logging

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Team, Match, Player, Goal, TeamPlayer
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


class MatchDetails(APIView):
    def post(self, request):
        try:
            match_id = int(request.data.get('match_id', 0))
            if match_id:
                match = Match.objects.get(id=match_id)
            elif Match.objects.filter(Q(match_status=1) | Q(match_status=2)):
                match = Match.objects.filter(Q(match_status=1) | Q(match_status=2)).order_by('date')[0]
            else:
                return Response({"status": -2, "message": "No matches started"})
            data = {}
            goal_list = []
            goals = Goal.objects.filter(match=match, team=match.team1)
            for goal in goals:
                goal_list.append({'player_id': goal.player.id,
                                  'player_name': goal.player.name,
                                  'minute': goal.goal_time,
                                  'self_status': goal.self_status
                                  })
            data['team1'] = {
                "team": match.team1.name,
                "team_image": match.team1.image.image_file.url,
                "goals": goal_list,
                "no_of_gols": len(goals)
            }
            goal_list = []
            goals = Goal.objects.filter(match=match, team=match.team2)
            for goal in goals:
                goal_list.append({'player_id': goal.player.id,
                                  'player_name': goal.player.name,
                                  'minute': goal.goal_time,
                                  'self_status': goal.self_status
                                  })
            data['team2'] = {
                "team": match.team2.name,
                "team_image": match.team2.image.image_file.url,
                "goals": goal_list,
                "no_of_gols": len(goals),
            }
            data['date'] = str(match.date)
            data['status'] = match.match_status

            return Response(data)
        except Exception as e:
            log.error(e.message)
            return Response({"status": -1, "message": str(e.message)})


class UpcomingMatches(APIView):
    def post(self, request):
        try:
            numbers = int(request.data.get('numbers', 3))
            queryset = Match.objects.filter(match_status=0).order_by('date')[:numbers]
            data = MatchSerializer(queryset, many=True)
            return Response(data.data)
        except Exception as e:
            log.error(e.message)
            return Response({"status": -1, "message": str(e.message)})


class TeamPlayerList(APIView):
    def post(self, request):
        try:
            team_id = request.data['team_id']
            teamplayer = TeamPlayer.objects.filter(team__id=team_id)
            player_data = []
            for player in teamplayer:
                queryset = player.player
                data = PlayerSerializer(queryset, many=False)
                player_data.append(data.data)
            return Response(player_data)
        except Exception as e:
            log.error(e.message)
            return Response({"status": -1, "message": str(e.message)})


class MatchFixture(APIView):
    def post(self, request):
        try:
            queryset = Match.objects.all()
            if "match_status" in request.data:
                queryset = queryset.filter(match_status=int(request.data['match_status']))
            queryset = queryset.order_by('-match_status', 'date')
            data = MatchSerializer(queryset, many=True)
            return Response(data.data)
        except Exception as e:
            log.error(e.message)
            return Response({"status": -1, "message": str(e.message)})
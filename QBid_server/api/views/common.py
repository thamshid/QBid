from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Team


class Login(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
            try:
                team = Team.objects.get(username=username, password=password)
            except:
                return Response({"status": -1, "message": "Invalid username or password"})
            return Response({"status": 1, "message":"Login success"})
        except:
            pass

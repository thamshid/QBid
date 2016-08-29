import itertools
import os

from django.core.wsgi import get_wsgi_application

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    application = get_wsgi_application()
    from api.models import Team, Match

    try:
        teams = Team.objects.all()
        no_of_teams = len(teams)
        matches = list(itertools.permutations(teams, 2))
        for match in matches:
            match_obj = Match()
            match_obj.name = 'Group level'
            match_obj.team1 = match[0]
            match_obj.team2 = match[1]
            match_obj.save()
    except Exception as e:
        print e.message

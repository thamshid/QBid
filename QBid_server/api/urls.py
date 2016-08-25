from django.conf.urls import url

from api.views import common

urlpatterns = [
    url(r'^login/$', common.Login.as_view(), name='home'),
    url(r'^point_table/', common.PointTable.as_view(), name='note_list'),
    url(r'^last_matches/', common.LastMatches.as_view(), name='last_matches_list'),
    url(r'^leading_goal_scorer/', common.LeadingGoalScorer.as_view(), name='leading_goal_scorer'),
    url(r'^match_details/', common.MatchDetails.as_view(), name='MatchDetails'),
    url(r'^upcoming_matches/', common.UpcomingMatches.as_view(), name='UpcomingMatches'),
    url(r'^team_player/', common.TeamPlayerList.as_view(), name='TeamPlayerList'),
]

from api.models import Goal, EmailList, Player, Team
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string
from email.mime.image import MIMEImage

def send_match_email(match):
    try:
        match_details = {}
        team1 = {}
        team2 = {}
        images = {}
        team1['name'] = match.team1.name
        team1['goal'] = match.team1_goal
        images['team1'] = match.team1.image.image_file.path
        images['team2'] = match.team2.image.image_file.path
        goals = Goal.objects.filter(match=match, team=match.team1)
        team_goal = []
        for goal in goals:
            team_goal.append({
                'player': goal.player.name,
                'minute': goal.goal_time,
                'self_status': goal.self_status
            })
        team1['goal_details'] = team_goal
        team2['name'] = match.team2.name
        team2['goal'] = match.team2_goal
        goals = Goal.objects.filter(match=match, team=match.team2)
        team_goal = []
        for goal in goals:
            team_goal.append({
                'player': goal.player.name,
                'minute': goal.goal_time,
                'self_status': goal.self_status
            })
        team2['goal_details'] = team_goal
        match_details['team1'] = team1
        match_details['team2'] = team2

        player_list = []
        players = Player.objects.filter(no_of_goals__gt=0).order_by('-no_of_goals')[:3]
        for player in players:
            player_list.append({
                'id': player.id,
                'name': player.name,
                'goals': player.no_of_goals
            })
            images[''+str(player.id)] = player.image.image_file.path

        point_table = []
        teams = Team.objects.all().order_by('-point', '-goal_fo', 'goal_against', 'game_played')
        for team in teams:
            point_table.append({
                "team_name": team.name,
                "win": team.win,
                "lost": team.lost,
                "draw": team.draw,
                "gemes": team.game_played,
                "point": team.point,
                "GA": team.goal_against,
                "GF": team.goal_fo
            })

        headers = {
            'Reply-To': "QPl<thamshid@gmail.com>",
            'From': "QPL<thamshid@gmail.com>",
        }
        sender = "QPL<thamshid@gmail.com>"
        subject = "QPL Result - " + str(match)
        to_list = EmailList.objects.all()
        to = []
        for i in to_list:
            to.append(i.email)
        dic = {"match_details":match_details,
                    "topers": player_list,
                    "pont_table": point_table
                }
        print dic
        message = render_to_string('match_email.html', dic)
        msg = EmailMessage(subject, message, sender, to, headers=headers)
        msg.content_subtype = "html"
        msg.mixed_subtype = 'related'
        for cid, img in images.items():
            fp = open(img, 'rb')
            msg_image = MIMEImage(fp.read())
            fp.close()
            msg_image.add_header('Content-ID', '<' + cid + '>')
            msg.attach(msg_image)
        print message
        return 1
        #return msg.send()
    except Exception as e:
        return e.message
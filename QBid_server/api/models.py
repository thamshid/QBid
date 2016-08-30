from __future__ import unicode_literals

from datetime import datetime

from django.db import models

from libraries.custom_exceptions import SameTeam, PlayerSoldOUT


class Image(models.Model):
    title = models.CharField(max_length=100)
    image_file = models.FileField(upload_to='images/')
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.now()
        self.updated = datetime.now()
        super(Image, self).save(*args, **kwargs)


class PlayerCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ForeignKey(Image, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=250)
    image = models.ForeignKey(Image, null=True, blank=True)
    balance = models.IntegerField(default=0)
    game_played = models.IntegerField(default=0)
    win = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    goal_fo = models.IntegerField(default=0)
    goal_against = models.IntegerField(default=0)
    point = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100)
    image = models.ForeignKey(Image, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    category = models.ForeignKey(PlayerCategory)
    base_value = models.IntegerField(default=0)
    reduced_value = models.IntegerField(default=0)
    sold_value = models.IntegerField(null=True, blank=True)
    sold_out = models.BooleanField(default=False)
    no_of_goals = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class Bid(models.Model):
    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)
    value = models.IntegerField()
    created = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()
        super(Bid, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.player.name


class TeamPlayer(models.Model):
    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)
    value = models.IntegerField()
    created = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()
        if self.player.sold_out:
            raise PlayerSoldOUT
        else:
            self.player.sold_out = True
            self.player.sold_value = self.value
            self.player.save()

        super(TeamPlayer, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.player.name + " -> " + self.team.name


class Galary(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    image = models.ForeignKey(Image)

    def __unicode__(self):
        return self.title


class Match(models.Model):
    name = models.CharField(max_length=50)
    team1 = models.ForeignKey(Team, related_name='team1')
    team2 = models.ForeignKey(Team, related_name='team2')
    date = models.DateField(null=True)
    match_status = models.IntegerField(default=0)
    winner = models.ForeignKey(Team, related_name="winner", null=True, blank=True)
    looser = models.ForeignKey(Team, related_name="looser", null=True, blank=True)
    draw = models.BooleanField(default=False)
    team1_goal = models.IntegerField(default=0)
    team2_goal = models.IntegerField(default=0)
    update_game_played = models.BooleanField(default=False)

    def __unicode__(self):
        return self.team1.name + " x " + self.team2.name

    def save(self, *args, **kwargs):
        if self.match_status == 1 and not self.update_game_played:
            self.team1.game_played += 1
            self.team1.save()
            self.team2.game_played += 1
            self.team2.save()
            self.update_game_played = True
        if self.match_status == 2:
            if self.team1_goal == self.team2_goal:
                self.draw = True
                self.team1.draw += 1
                self.team1.save()
                self.team2.draw += 1
                self.team2.save()
            elif self.team1_goal < self.team2_goal:
                self.winner = self.team2
                self.looser = self.team1
                self.team1.lost += 1
                self.team1.save()
                self.team2.win += 1
                self.team2.save()
            else:
                self.winner = self.team1
                self.looser = self.team2
                self.team2.lost += 1
                self.team2.save()
                self.team1.win += 1
                self.team1.save()
        super(Match, self).save(*args, **kwargs)


class Goal(models.Model):
    match = models.ForeignKey(Match)
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team, related_name="team")
    op_team = models.ForeignKey(Team, related_name="Opposite_team")
    self_status = models.BooleanField(default=False)
    goal_time = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.team == self.op_team:
            raise SameTeam
        if TeamPlayer.objects.filter(team=self.team, player=self.player):
            self.player.no_of_goals += 1
            self.player.save()
            self.self_status = True
        self.team.goal_fo += 1
        self.op_team.goal_against += 1
        self.team.save()
        self.op_team.save()
        if self.match.team1 == self.team:
            self.match.team1_goal += 1
        else:
            self.match.team2_goal += 1
        self.match.save()
        super(Goal, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.player.name


class EmailList(models.Model):
    email = models.CharField(max_length=100)

    def __unicode__(self):
        return self.email

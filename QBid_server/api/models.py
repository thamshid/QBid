from __future__ import unicode_literals

from datetime import datetime

from django.db import models


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
    image = models.ForeignKey(Image, null=True)

    def __unicode__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=250)
    image = models.ForeignKey(Image, null=True)
    balance = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100)
    image = models.ForeignKey(Image, null=True)
    dob = models.DateField(null=True)
    category = models.ForeignKey(PlayerCategory)
    base_value = models.IntegerField(default=0)
    reduced_value = models.IntegerField(default=0)
    sold_value = models.IntegerField(null=True)
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
            raise

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
    team1 = models.ForeignKey(Team, related_name='team1')
    team2 = models.ForeignKey(Team, related_name='team2')
    date = models.DateField(null=True)
    match_status = models.IntegerField(default=0)

    def __unicode__(self):
        return self.team1.name + " x " + self.team2.name


class MatchResult(models.Model):
    match = models.ForeignKey(Match)
    winner = models.ForeignKey(Team, related_name="winner", null=True)
    looser = models.ForeignKey(Team, related_name="looser", null=True)
    draw = models.BooleanField(default=False)
    team1_goal = models.IntegerField(default=0)
    team2_goal = models.IntegerField(default=0)

    def __unicode__(self):
        return self.match.team1.name + " x " + self.match.team2.name

    def save(self, *args, **kwargs):
        if self.match.match_status == 2:
            if self.team1_goal == self.team2_goal:
                self.draw = True
            elif self.team1_goal < self.team2_goal:
                self.winner = self.match.team2
                self.looser = self.match.team1
            else:
                self.winner = self.match.team1
                self.looser = self.match.team2
        super(MatchResult, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.match


class Goal(models.Model):
    match = models.ForeignKey(Match)
    player = models.ForeignKey(Player)
    team = models.ForeignKey(Team)
    self_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not TeamPlayer.objects.filter(team=self.team, player=self.player):
            self.player.no_of_goals += 1
            self.player.save()
            self.self_status = True
        super(Goal, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.player.name

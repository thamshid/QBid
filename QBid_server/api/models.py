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

    def __unicode__(self):
        return self.name


class TeamPlayer(models.Model):
    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)
    value = models.IntegerField()
    created = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()
        super(TeamPlayer, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.player


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
        return self.player


class Galary(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    image = models.ForeignKey(Image)

    def __unicode__(self):
        return self.title

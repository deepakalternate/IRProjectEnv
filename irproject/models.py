from __future__ import unicode_literals

from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)

    def __unicode__(self):
        return str(self.username)


class FriendStatus(models.Model):
    f_id = models.AutoField(primary_key=True)
    req_sender = models.ForeignKey(Users, related_name='sender')
    req_receiver = models.ForeignKey(Users, related_name='receiver')
    status = models.CharField(max_length=50)

    def __unicode__(self):
        return self.f_id


class Queries(models.Model):
    q_id = models.AutoField(primary_key=True)
    q_filename = models.CharField(max_length=100)
    asked_by = models.ForeignKey(Users)

    def __unicode__(self):
        return self.q_id


class Answers(models.Model):
    a_id = models.AutoField(primary_key=True)
    a_filename = models.CharField(max_length=50)
    answered_by = models.ForeignKey(Users)
    query = models.ForeignKey(Queries)


class QueriesReceived(models.Model):
    asked_to = models.ForeignKey(Users)
    question_asked = models.ForeignKey(Queries)


class FriendValue(models.Model):
    friendship_no = models.ForeignKey(FriendStatus)
    value_by_user = models.ForeignKey(Users)
    value = models.IntegerField()
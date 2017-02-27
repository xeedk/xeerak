from django.db import models
from plugins.native.models import Native
from plugins.identity.models import SmsIdentity





class Guess(models.Model):
    guessValue = models.IntegerField(default=0)
    guessLabel = models.CharField(max_length=100)
    wasGuess = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now=True, db_index=True)


class RecognizerImage(models.Model):
    imageLocation = models.FileField(upload_to='media/')
    imageName = models.CharField(max_length=100)
    size = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now=True, db_index=True)
    wasSuccess = models.BooleanField(default=False)
    isBlocked = models.BooleanField(default=False)
    guess = models.ForeignKey(Guess,null=True)


class SuccessfullPermission(models.Model):
    imageRecognizer =  models.ForeignKey(RecognizerImage)
    nativeIdentity  =  models.ForeignKey(Native)
    guessId  =  models.ForeignKey(Guess)
    createdAt = models.DateTimeField(auto_now=True, db_index=True)


class SmsRequest(models.Model):
    number = models.CharField(max_length=20)
    sms  = models.CharField(max_length=40)
    wasSuccess = models.BooleanField(default=False)
    isBlocked = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now=True, db_index=True)
    smsIdentity = models.ForeignKey(SmsIdentity,null=True)

class SuccessfullSmsPermission(models.Model):
    smsIdentity =  models.ForeignKey(SmsIdentity)
    smsRequest  =  models.ForeignKey(SmsRequest)
    createdAt = models.DateTimeField(auto_now=True, db_index=True)
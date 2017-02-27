from django.db import models
from plugins.native.models import Native


# Create your models here.
class Identity(models.Model):
    identityNative =  models.ForeignKey(Native)
    #zipFile =  models.FileField(upload_to='zipIdentities/%Y/%m/%d')
    identityCover  =  models.CharField(max_length=100)
    createdAt =  models.DateTimeField(auto_now=True, db_index=True)


class IdentityImage(models.Model):
    imageName = models.CharField(max_length=250)
    imageFile = models.FileField()
    imageIdentity = models.ForeignKey(Identity)
    imageSize = models.IntegerField(default=0)
    createdAt =  models.DateTimeField(auto_now=True, db_index=True)


class SmsIdentity(models.Model):
    identityNative = models.ForeignKey(Native)
    smsNumber = models.CharField(max_length=20)
    smsText = models.CharField(max_length=40)
    createdAt =  models.DateTimeField(auto_now=True, db_index=True)
    status = models.BooleanField(default=True)

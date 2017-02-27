from django.db import models

# Create your models here.


class Native(models.Model):
	firstName = models.CharField(max_length=20)
	lastName = models.CharField(max_length=20)
	nativeName = models.CharField(max_length=40)
	nativeStatus = models.BooleanField(default=True)
	createdAt =  models.DateTimeField(auto_now=True, db_index=True)

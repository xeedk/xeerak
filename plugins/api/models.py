from django.db import models

# Create your models here.

class TFlow(models.Model):
	tfLabelsFileLocation = models.CharField(max_length=500)
	tfGraphFileLocation	 = models.CharField(max_length=500)
	tfNNeckDirectory	 = models.CharField(max_length=500)
	tfModelDirectory	 = models.CharField(max_length=500)
	tfImagesDirectory	 = models.CharField(max_length=500)
	tfMaxScore	 		 = models.IntegerField()
	tfMaxSteps	 		 = models.IntegerField()
	tfScriptLocation     = models.CharField(max_length=500)
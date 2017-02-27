from django.template.response import TemplateResponse

from django.contrib.auth.decorators import login_required

from plugins.api.models import TFlow
from django.http import JsonResponse

@login_required(login_url='/admin/')
def homePage(request):
    #images = Image.objects.all()
    return TemplateResponse(request,'index.html')    
    #return TemplateResponse(request,'index.html',{'images':images})


def TensorFlowSettings(request):
	tfLabelsFile = request.POST['tfLabelsFile']
	tfGraphFile	 = request.POST['tfGraphFile']
	tfNNeckDir	 = request.POST['tfNNeckDir']
	tfModelDir	 = request.POST['tfModelDir']
	tfMaxScore	 = request.POST['tfMaxScore']
	tfMaxSteps	 = request.POST['tfMaxSteps']

	tflow = TFlow.objects.get(id=1)

	if tfLabelsFile != tflow.tfLabelsFileLocation:
		tflow.tfLabelsFileLocation = tfLabelsFile
	if tfGraphFile != tflow.tfGraphFileLocation:
		tflow.tfGraphFileLocation = tfGraphFile
	if tfNNeckDir != tflow.tfNNeckDirectory:
		tflow.tfNNeckDirectory = tfNNeckDir
	if tfModelDir != tflow.tfModelDirectory:
		tflow.tfModelDirectory = tfModelDir
	if tfMaxScore != tflow.tfMaxScore:
		tflow.tfMaxScore = tfMaxScore
	if tfMaxSteps != tflow.tfMaxSteps:
		tflow.tfMaxSteps = tfMaxSteps

	tflow.save()
	
	print(tflow.tfLabelsFileLocation)
	print(tfLabelsFile,tfGraphFile,tfNNeckDir,tfModelDir,tfMaxScore,tfMaxSteps)
	data = {'status': 'ok'}
	return JsonResponse(data)

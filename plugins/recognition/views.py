

import tensorflow ,sys
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser

import datetime

from rest_framework import status

from django.shortcuts import render

import uuid,os

from django.template.response import TemplateResponse

from plugins.recognition.serializer import RecognizerImageModelSerializer,RecognizerSmsModelSerializer

from plugins.recognition.models import Guess,SuccessfullPermission,RecognizerImage,SmsRequest,SuccessfullSmsPermission

from plugins.native.models import Native

from plugins.identity.models import SmsIdentity

from plugins.api.models import TFlow

from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def ListEntries(request):
    entriees = RecognizerImage.objects.all()
    successes = SuccessfullPermission.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(entriees, 6)

    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)

    return TemplateResponse(request,'Pages/entries.html',{'entries':entries,'success':successes})    
    #return TemplateResponse(request,'index.html',{'images':images})



def createGuess(humanString,score,image):
    guess = Guess()
    guess.imageRecognizer = image
    guess.guessLabel = humanString
    guess.guessValue = score
    guess.createdAt =  datetime.datetime.now()
    guess.save()
    print("Guess:",guess.id)
    return guess


def createImage(fileName):
    image = RecognizerImage()
    image.imageName = fileName
    image.imageLocation= "core/media/recog/"+fileName
    image.createdAt = datetime.datetime.now()
    image.size=os.stat("core/media/recog/"+fileName).st_size
    image.save()
    print("Image:",image.id)
    return image




def SettingsPage(request):
    tflow = TFlow.objects.get(id=2)
    return render(request, 'Pages/settings.html', {'tflow':tflow})

def DocumentationPage(request):
	return render(request, 'Documentation/index.html')

def SmsEntries(request):
    entriees = SmsRequest.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(entriees, 10)

    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)

    return render(request, 'Pages/smsEntries.html',{'entries':entries})

class RecognizerImageList(APIView):
    serializer_class = RecognizerImageModelSerializer
    parser_classes = (MultiPartParser, FormParser,)


    def tryImage(self,fileName):
        image_data = tensorflow.gfile.FastGFile("core/media/recog/"+fileName, 'rb').read()
       # tfModel = settings.TFlowModel
        #tfLabel = settings.TFlowLabels
        label_lines = [line.rstrip() for line in tensorflow.gfile.GFile("/home/ros2/test/ll.txt")]
        #label_lines = [line.rstrip() for line in tensorflow.gfile.GFile(tfLabel)]
        with tensorflow.gfile.FastGFile("/home/ros2/test/gg.pb", 'rb') as f:
        #with tensorflow.gfile.FastGFile(tfModel, 'rb') as f:

            graph_def = tensorflow.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tensorflow.import_graph_def(graph_def, name='')

        imageId = createImage(fileName)
        highScore = 0
        highLabel = ""
    
        with tensorflow.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

            top_predictions = predictions[0].argsort()[-len(predictions[0]):][::-1]
            guesses = dict()
            for node_id in top_predictions:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                if(score > highScore):
                    highScore = score
                    highLabel = human_string

            if(highScore > .8 ):
                gues = createGuess(highLabel,highScore*100,imageId)
                if self.isNativeAllowed(highLabel):
                    print(highLabel)
                    sp = SuccessfullPermission()
                    sp.guessId = gues
                    sp.imageRecognizer = imageId
                    native = Native.objects.get(nativeName=highLabel)
                    sp.nativeIdentity = native
                    sp.save()
                    #i have to update the image and the guess
                    gues.wasSuccess = True
                    gues.save()
                    imageId.wasSuccess = True
                    imageId.guess = gues
                    imageId.save()
                    return {
                        'status':'Ok',
                        'message':highLabel
                    }
                else:
                    gues.wasSuccess = False
                    imageId.wasSuccess = False
                    imageId.isBlocked = True
                    imageId.guess = gues
                    gues.save()
                    imageId.save()
                    return {
                        'status':'blocked',
                        'Message': highLabel
                    }
            else:
                return {
                    'status':'notOk',
                    'Message': 'ring'
                }



    def post(self, request, format='jpg'):
        image_file = request.FILES['image_file']
        fileName = 'Image_' + str(str(uuid.uuid4())) + '.jpg'
        destination = open("core/media/recog/"+fileName, 'wb+')

        for chunk in image_file.chunks():
            destination.write(chunk)
        
        destination.close()

        response = self.tryImage(fileName)


          #return Response({'status:' 'ok'}, status.HTTP_201_CREATED)
       # response = self.recognitionResponse(guesses)

        return Response(response, status.HTTP_201_CREATED)

    def isNativeAllowed(self,nativeNameLabel):
    	try:
            native = Native.objects.get(nativeName=nativeNameLabel)
            return native.nativeStatus
    	except:
    		pass
    	return False


class SmsRecognizerList(APIView):
    serializer_class = RecognizerSmsModelSerializer

    def post(self, request, format='jpg'):
        phone = request.POST.get('smsNumber')
        message = request.POST.get('smsText')
        smsRequest = SmsRequest()
        smsRequest.number = phone
        smsRequest.sms = message[1:] 
        smsRequest.save()

        smsIdentity = SmsIdentity.objects.filter(smsNumber=phone.strip(),smsText=message[1:].strip())
        response=''
        for smsId in smsIdentity:
            if smsId:
                if smsId.status:
                    sp = SuccessfullSmsPermission()
                    sp.smsIdentity = smsId
                    sp.smsRequest = smsRequest
                    smsRequest.wasSuccess = True
                    smsRequest.smsIdentity = smsId
                    smsRequest.save()
                    sp.save()
                    response = {
                        'status':'Ok',
                        'Message': 'Success'
                    }
                    break
                else:
                    smsRequest.wasSuccess = False
                    smsRequest.isBlocked = True
                    smsRequest.smsIdentity = smsId
                    smsRequest.save()
                    response = {
                        'status':'notOk',
                        'Message': 'Blocked'
    	               }
            else:
                response = {
                        'status':'notOk',
                        'Message': 'Not Registered'
                    }
        return Response(response, status.HTTP_201_CREATED)




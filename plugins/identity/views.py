

import tensorflow ,sys ,datetime ,uuid ,os

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser,FormParser

from django.shortcuts import render

from django.template.response import TemplateResponse

from plugins.recognition.serializer import RecognizerImageModelSerializer,RecognizerSmsModelSerializer

from plugins.recognition.models import Guess,SuccessfullPermission,RecognizerImage

from rest_framework.views import APIView

from plugins.native.models import Native

from plugins.identity.models import SmsIdentity,IdentityImage,Identity

from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.conf import settings



def smsIdentities(request):

    identitieses = SmsIdentity.objects.all()

    natives = Native.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(identitieses, 10)

    try:

    	identities = paginator.page(page)

    except PageNotAnInteger:

    	identities = paginator.page(1)

    except EmptyPage:

    	identities = paginator.page(paginator.num_pages)

    return TemplateResponse(request,'Pages/smsIdentities.html',{'identities':identities,'natives':natives})   



def Identities(request):

    identitieses = Identity.objects.all()

    page = request.GET.get('page', 1)

    paginator = Paginator(identitieses, 10)

    try:

    	identities = paginator.page(page)

    except PageNotAnInteger:

    	identities = paginator.page(1)

    except EmptyPage:

    	identities = paginator.page(paginator.num_pages)

    return TemplateResponse(request,'Pages/identities.html',{'identities':identities}) 


def ShowIdentity(request,identity_Id):

    identity = Identity.objects.get(id=identity_Id)

    images = IdentityImage.objects.filter(imageIdentity=identity)

    return TemplateResponse(request,'Components/Identity/view.html',{'identity':identity,'images' : images})    




def ChangeStatus(request):

    identityId  = request.POST['id']

    try:

    	identity = Identity.objects.get(id=identityId)

    	native = identity.identityNative

    	if native.nativeStatus :

    		native.nativeStatus = False

    	else:

    		native.nativeStatus = True

    	native.save()

    except:

    	pass

    data = {'status': 'ok'}

    return JsonResponse(data)  




def ForkIdentity(request):

	native = Native.objects.get(id=request.session['currentNewNative'])

	noOfImagesWithNative =  IdentityImage.objects.filter(imageIdentity=request.session['currentNewIdentity']).count()

	if(noOfImagesWithNative > 20):

		data = {'status': 'ok'}

		del request.session['currentNewIdentity']

		del request.session['currentNewNative']

		return JsonResponse(data)  

	else:

		data = {'status' : 'notOk'}

		return JsonResponse(data)




def ChangeSmsStatus(request):

    identityId   =   request.POST['id']

    SmsIden = SmsIdentity.objects.get(id=identityId)

    if SmsIden.status :

    	SmsIden.status = False

    else:

    	SmsIden.status = True

    SmsIden.save()

    data = {'status': 'ok'}

    return JsonResponse(data)  



class SmsIdentityAPI(APIView):

	serializer_class = RecognizerSmsModelSerializer

	def post(self, request):

		smsNumber  =   request.POST['smsNumber']

		smsText   =   request.POST['smsText']

		nativeName =   request.POST['nativeName']

		if  smsNumber and  smsText and  nativeName:

			print(smsNumber,smsText,nativeName)

			native = Native.objects.get(nativeName=nativeName)

			smsIdentity = self.newSmsIdentity(smsNumber,smsText,native)

			data = {'status': 'ok'}

			return JsonResponse(data)
			
		data = {'status': 'notOk'}

		return JsonResponse(data)	



	def newSmsIdentity(self,smsNumber,smsText,native):

	    smsIdentity = SmsIdentity()

	    smsIdentity.identityNative = native

	    smsIdentity.smsText = smsText

	    smsIdentity.smsNumber = smsNumber

	    smsIdentity.status = True

	    smsIdentity.save()

	    return smsIdentity




class IdentityImageUploadView(APIView):

    def get(self, request):

        identityNative = Native.objects.get(id=self.request.session['currentNewNative'])

        imagesWithIdentity =  IdentityImage.objects.filter(imageIdentity=self.request.session['currentNewIdentity'])

        return render(self.request, 'Components/Identity/create.html', {'imagesWithIdentity': imagesWithIdentity,'native':identityNative})



    def post(self, request):

        file = self.request.FILES['imageFile']

        nativeInSessionId = self.request.session['currentNewNative']

        identityInSessionId = self.request.session['currentNewIdentity']

        native= Native.objects.get(id=nativeInSessionId)

        identityMediaRoot = settings.MEDIA_ROOT + '/identities/'

        folderToSave = identityMediaRoot + native.nativeName + '/'

        fileName = native.nativeName +'_'+ str(str(uuid.uuid4())) + '.jpg'

        destination = open(folderToSave+fileName, 'wb+')

        for chunk in file.chunks():

        	destination.write(chunk)
        
        destination.close()

        identity = Identity.objects.get(id=identityInSessionId)

        imageLocation =  fileName

        imageSize = os.stat(folderToSave + imageLocation).st_size

        image = self.createImageForIdentity(identity,imageLocation,imageSize,fileName)

        data = {'url':  fileName,
        		'name': fileName,
        		'is_valid':True,
        		}

        return JsonResponse(data)


    def createImageForIdentity(self,identity,imageLocation,imageSize,fileName):

    	idImage = IdentityImage()

    	idImage.imageName = fileName

    	idImage.imageFile = imageLocation

    	idImage.imageIdentity = identity

    	idImage.save()

    	return idImage



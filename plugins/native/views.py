
from django.shortcuts import render

# Create your views here.

from plugins.native.models import Native

from plugins.native.models import Hours

from plugins.identity.models import Identity

from rest_framework.views import APIView


import os


from django.http import JsonResponse


from plugins.native.serializer import NativeModelSerializer

from django.template.response import TemplateResponse

def SetTimingsPage(request):

    hours = Hours.objects.all()

    natives = Native.objects.all()

    return TemplateResponse(request,'Components/Identity/timings.html',{'hours':hours,'range': range(25),'natives':natives})




def UpdateTimings(request):

	allowedFrom  =   request.POST['allowedFrom']

	allowedTill   =   request.POST['allowedTill']

	nativeName =   request.POST['nativeName']

	native = Native.objects.get(nativeName=nativeName)

	hours = Hours.objects.get(native=native)

	till = int(allowedTill) - 1

	if int(allowedFrom) < 10:

		allowedFrom = '0' + allowedFrom

	if int(allowedTill) < 10:

		allowedTill =  '0' + allowedTill


	hours.startTime = allowedFrom + ":00"


	hours.endTime = str(till)  + ":59"

	hours.save()

	data = {'status': 'ok'}

	return JsonResponse(data)





class NativeAPI(APIView):

	serializer_class = NativeModelSerializer

	def post(self, request):

		firstName  =   request.POST['firstName']

		lastName   =   request.POST['lastName']

		nativeName =   request.POST['nativeName']

		if  firstName and  lastName and  nativeName:

			native = self.newNative(firstName,lastName,nativeName)

			identity= self.newIdentity(native)

			request.session['currentNewIdentity'] = identity.id

			request.session['currentNewNative'] = native.id

			return render(request, 'Components/Identity/create.html')




	def newNative(self,firstName,lastName,nativeName):
	    native = Native()

	    native.firstName = firstName

	    native.lastName = lastName

	    native.nativeName = nativeName

	    native.save()

	    identityMediaRoot = settings.MEDIA_ROOT + '/identities/'

	    os.mkdir(os.path.join(identityMediaRoot, nativeName))

	    hours = self.newHours(native)

	    return native




	def newIdentity(self,nativE):

		identity = Identity()

		identity.identityNative = nativE

		identity.save()

		return identity





	def newHours(self,native):

		hours = Hours()

		hours.native = native

		hours.startTime = "00:00"

		hours.endTime = "24:00"

		hours.save()

		return hours
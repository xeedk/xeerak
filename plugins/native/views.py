
from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate, login

from django.views.decorators.csrf import ensure_csrf_cookie

from plugins.native.models import Native
from plugins.identity.models import Identity
from rest_framework.views import APIView
from django.conf import settings

import os
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.conf import settings

from plugins.native.serializer import NativeModelSerializer

class NativeAPI(APIView):
	serializer_class = NativeModelSerializer

	def post(self, request):

		firstName  =   request.POST['firstName']
		lastName   =   request.POST['lastName']
		nativeName =   request.POST['nativeName']

		if  firstName and  lastName and  nativeName:
			print(firstName,lastName,nativeName)
			native = self.newNative(firstName,lastName,nativeName)
			identity= self.newIdentity(native)
			request.session['currentNewIdentity'] = identity.id
			request.session['currentNewNative'] = native.id
			print(native.id,identity.id)
			return render(request, 'Components/Identity/create.html')

	def newNative(self,firstName,lastName,nativeName):
	    native = Native()
	    native.firstName = firstName
	    native.lastName = lastName
	    native.nativeName = nativeName
	    native.save()
	    identityMediaRoot = settings.MEDIA_ROOT + '/identities/'
	    os.mkdir(os.path.join(identityMediaRoot, nativeName))
	    return native

	def newIdentity(self,nativE):
		identity = Identity()
		identity.identityNative = nativE
		identity.save()
		return identity

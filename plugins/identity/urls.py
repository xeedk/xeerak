from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url

from django.conf.urls.static import static

from plugins.identity.views import IdentityImageUploadView
from plugins.identity.views import SmsIdentityAPI

from plugins.identity.views import ShowIdentity
from plugins.identity.views import ChangeStatus
from plugins.identity.views import ChangeSmsStatus
from plugins.identity.views import ForkIdentity

urlpatterns = [
	url(r'^create', IdentityImageUploadView.as_view(), name='identityImage'),
	url(r'^sms', SmsIdentityAPI.as_view()),
	url(r'^view/(?P<identity_Id>.+?)/$', ShowIdentity),
	url(r'^sms', SmsIdentityAPI.as_view()),
	url(r'^status', ChangeStatus),
	url(r'^messageStatus', ChangeSmsStatus),
	url(r'^fork', ForkIdentity),

]
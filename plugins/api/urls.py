from django.conf.urls import *
from rest_framework.urlpatterns import format_suffix_patterns
from plugins.recognition.views import SmsRecognizerList
from plugins.recognition.views import RecognizerImageList

from core.views import TensorFlowSettings

from core.mytensor import StartTrainingXeerak
from plugins.native.views import UpdateTimings

urlpatterns = [
    url(r'^imageRecognize/$',RecognizerImageList.as_view()),
    url(r'^smsRecognize/$', SmsRecognizerList.as_view()),
    url(r'^identity/', include('plugins.identity.urls')),
    url(r'^native', include('plugins.native.urls')),
    url(r'^settings', TensorFlowSettings),
    url(r'^training', StartTrainingXeerak),
    url(r'^hours', UpdateTimings),

]
urlpatterns = format_suffix_patterns(urlpatterns)
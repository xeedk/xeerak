"""ami URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url

from django.conf.urls.static import static

from plugins.identity.views import smsIdentities
from plugins.identity.views import Identities
from plugins.native.views import SetTimingsPage

from plugins.recognition.views import ListEntries
from plugins.recognition.views import SettingsPage
from plugins.recognition.views import DocumentationPage
from plugins.recognition.views import SmsEntries

from .views import homePage


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',homePage),
    url(r'^api/', include('plugins.api.urls')),
    url(r'^identity/', include('plugins.identity.urls')),
    url(r'^entries/',ListEntries),
    url(r'^smsEntries/',SmsEntries),
    url(r'^identities/',Identities),
    url(r'^smsIdentities/',smsIdentities),
    url(r'^settings', SettingsPage),
    url(r'^timings', SetTimingsPage),
    url(r'^documentation', DocumentationPage),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


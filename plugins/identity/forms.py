
from django import forms

from plugins.identity.models import IdentityImage

class PhotoForm(forms.ModelForm):
    class Meta:
        model = IdentityImage
        fields = ('imageFile', )
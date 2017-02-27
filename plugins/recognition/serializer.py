from rest_framework import serializers
from plugins.recognition.models import RecognizerImage,Guess,SuccessfullPermission,SuccessfullSmsPermission,SmsRequest

class RecognizerImageModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecognizerImage
        fields = ('imageLocation', 'imageName','createdAt','size')


        def create(self, validated_data):
            return Image.objects.create(**validated_data)



class RecognizerSmsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SmsRequest
        fields = ('smsNumber', 'smsText')


        def create(self, validated_data):
            return SmsRequest.objects.create(**validated_data)


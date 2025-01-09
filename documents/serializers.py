from rest_framework import serializers
from .models import Company, Document, Signer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class SignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signer
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    signers = SignerSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = '__all__'

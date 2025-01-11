from rest_framework import serializers
from .models import Company, Document, Signer

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'api_token', 'created_at']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'company', 'name', 'status', 'open_id', 'token', 'created_at']

class SignerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signer
        fields = ['id', 'document', 'name', 'email', 'status', 'created_at']

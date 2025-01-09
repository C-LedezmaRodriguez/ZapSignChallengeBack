# documents/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from .serializers import CompanySerializer, DocumentSerializer, SignerSerializer
from .models import Company, Document, Signer



class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @action(detail=True, methods=['post'])
    def create_document(self, request, pk=None):
        """Crea un documento en ZapSign y guarda la respuesta"""
        company = self.get_object()
        data = request.data

        # Llamada a la API de ZapSign
        zapsign_url = "https://sandbox.api.zapsign.com.br/api/v1/docs/"
        headers = {"Authorization": f"Token {company.api_token}"}
        response = requests.post(zapsign_url, headers=headers, data=data)

        if response.status_code == 201:
            response_data = response.json()
            document = Document.objects.create(
                company=company,
                name=data.get("name"),
                status=response_data["status"],
                open_id=response_data["id"],
                token=response_data["token"]
            )
            return Response(DocumentSerializer(document).data)
        return Response({"error": "Error al crear el documento"}, status=response.status_code)


class SignerViewSet(ModelViewSet):
    queryset = Signer.objects.all()
    serializer_class = SignerSerializer

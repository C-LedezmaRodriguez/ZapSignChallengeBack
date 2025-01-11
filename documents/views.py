from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.conf import settings
import requests
from .serializers import CompanySerializer, DocumentSerializer, SignerSerializer
from .models import Company, Document, Signer

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    @action(detail=True, methods=['post'], url_path='create-document', url_name='create_document')
    def create_document(self, request, pk=None):
        """
        Endpoint para crear un documento en ZapSign y registrarlo en la base de datos local.
        """
        company = self.get_object()
        data = request.data

        if not data.get("name"):
            raise ValidationError({"name": "El campo 'name' es obligatorio."})

        zapsign_url = "https://api.zapsign.com.br/api/v1/docs/"
        headers = {
            "Authorization": f"Bearer {settings.ZAPSIGN_API_KEY}",
        }

        response = requests.post(zapsign_url, headers=headers, json=data)

        if response.status_code == 201:
            response_data = response.json()
            document = Document.objects.create(
                company=company,
                name=data.get("name"),
                status=response_data.get("status"),
                open_id=response_data.get("id"),
                token=response_data.get("token")
            )
            return Response(DocumentSerializer(document).data)
        else:
            error_message = response.json().get("detail", response.json().get("error", "Error desconocido al crear el documento."))
            return Response({"error": error_message}, status=response.status_code)

    @action(detail=True, methods=['get'], url_path='update-status', url_name='update_status')
    def update_status(self, request, pk=None):
        """
        Endpoint para actualizar el estado de un documento existente desde ZapSign.
        """
        document = self.get_object()
        zapsign_url = f"https://api.zapsign.com.br/api/v1/docs/{document.open_id}/"
        headers = {
            "Authorization": f"Bearer {settings.ZAPSIGN_API_KEY}",
        }
        response = requests.get(zapsign_url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            document.status = response_data.get("status", document.status)
            document.save()
            return Response(DocumentSerializer(document).data)
        else:
            error_message = response.json().get("detail", response.json().get("error", "Error desconocido al actualizar el estado del documento."))
            return Response({"error": error_message}, status=response.status_code)


class SignerViewSet(ModelViewSet):
    queryset = Signer.objects.all()
    serializer_class = SignerSerializer

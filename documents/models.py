from django.db import models

class Company(models.Model):
    """Class Company"""
    name = models.CharField(max_length=255)
    api_token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)


class Document(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="documents")
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    open_id = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Signer(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="signers")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    status = models.CharField(max_length=50, default="pending")
    signer_token = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(f"{self.name} - {self.document.name}")

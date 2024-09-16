from django.db import models
  
class ZohoToken(models.Model):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    api_domain =models.URLField()
    token_type = models.CharField(max_length=50)
    expires_in = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        from datetime import datetime, timedelta
        return self.created_at + timedelta(seconds=self.expires_in) < datetime.now()
    
class Lead(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    zoho_id = models.CharField(max_length=255, unique=True)  # ID de Zoho CRM para evitar duplicados

    def __str__(self):
        return f'{self.name} - {self.name}'

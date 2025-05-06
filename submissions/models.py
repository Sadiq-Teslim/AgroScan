# models.py
from django.db import models
from django.contrib.auth.models import User

class PlantDiagnosis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='diagnosis_images/')
    image_prompt = models.TextField(blank=True)
    diagnosis_title = models.CharField(max_length=255)
    health_condition = models.TextField()
    disease_signs = models.TextField()
    control_suggestions = models.TextField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

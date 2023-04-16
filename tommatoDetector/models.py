from django.db import models

# Create your models here.
class predictiondata(models.Model):
    result = models.TextField()
    confidencerate = models.FloatField()
    image = models.ImageField(upload_to='uploaded/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.result
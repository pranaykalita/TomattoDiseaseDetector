from django.contrib import admin
from .models import predictiondata

# Register your models here.
class predictdataAdmin(admin.ModelAdmin):
    list_display = ('result', 'confidencerate', 'created_at')
    list_filter = ('created_at',)

admin.site.register(predictiondata, predictdataAdmin)

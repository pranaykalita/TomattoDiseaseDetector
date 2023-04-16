from django.shortcuts import render
from .models import predictiondata
from django.core.files.storage import FileSystemStorage
from .predict_lite import predictDisease
import os
from urllib.parse import quote
from django.conf import settings
# Create your views here.
fs = FileSystemStorage()

def home(request):
    if request.method == 'POST':
        
        uploaded_file = request.FILES["predictimage"]
        file_name = uploaded_file.name
        image_name = quote(file_name).replace('%20','_')

        filename = fs.save(uploaded_file.name,uploaded_file)
        request.session['file_path'] = filename

        filepath = fs.path(filename)

        confidence , result = predictDisease(filepath)
        context = {
            "img_name": image_name,
            "Diseases" : result,
            "confidence" : confidence,
        }
        print(context)

        # Save the image and prediction results to the database
        store = predictiondata(
            result=result,
            confidencerate=confidence,
            image=uploaded_file
        )
        store.save()

        return render(request, 'predict.html', context)
    
    else:
        # Check if the file path is stored in the session
        file_path = request.session.get('file_path')

        if file_path:
            # Delete the file from the filesystem
            fs.delete(file_path)

        # Clear the file path from the session
        request.session.pop('file_path', None)
        return render(request, 'home.html')

    return render(request, 'home.html')

def result(request):

    images = predictiondata.objects.all().order_by('-created_at')
    
    context ={ 'images': images}
    return render(request, 'results.html',context)
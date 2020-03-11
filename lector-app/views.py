from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class Home(TemplateView):
    template_name= 'home.html'

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/upload.html')
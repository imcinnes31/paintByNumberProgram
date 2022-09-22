from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from . import pbnUtils

def index(request):
     return render(request, "paintByNumberMeApp/index.html")

def upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        pbnUtils.convert(file_url)
        return render(request, "paintByNumberMeApp/paint.html", 
        {
            # 'file_url1': file_url.replace('media/','media/result').replace('.jpg','1.png'),
            # 'file_url2': file_url.replace('media/','media/result').replace('.jpg','2.png'),
            'file_url3': file_url.replace('media/','media/result').replace('.jpg','3.png'),
            # 'file_url4': file_url.replace('media/','media/result').replace('.jpg','4.png'),
            # 'file_url5': file_url.replace('media/','media/result').replace('.jpg','5.png'),        
        })
    return render(request, "paintByNumberMeApp/upload.html")



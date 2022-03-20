from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UploadForm

from PIL import Image
import os

# def edit():
    # pass

# TODO: Add user specific features.
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            img = form.instance
            # return HttpResponseRedirect('/upload/')
            # print(img.image.url)
            return render(request,'image.html',{'form':form,'img':img.image.url, 'msg': 'Successfully uploaded!'})
    else:
        #localhost:8000/upload?edit=monochrome&filename=123.jpg
        form = UploadForm()
        edit = request.GET.get('edit',None)
        filename = request.GET.get('filename',None)
        if filename and edit:
            if edit == "monochrome":
                print(filename)
                if filename.startswith('/image'):
                    filename = filename.split('/')[3]
                print(filename)
                cool = os.path.join(os.path.dirname(__file__),'images',filename)
                img = Image.open(cool)
                img = img.convert("L")    
                # link = f'/images/monochrome/{filename}'
                link = os.path.join(os.path.dirname(__file__),'images','monochrome',filename)
                img.save(link)
                return render(request,'image.html',{'form':form,'img': '/image/' + link,'msg':'monochromed'})
        
    form = UploadForm()
    return render(request,'image.html',{'form':form})
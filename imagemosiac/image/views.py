from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UploadForm

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/upload/')
    else:
        form = UploadForm()
    return render(request,'image.html',{'form':form})
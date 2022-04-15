from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UploadForm

from PIL import Image
import os

from image.mosaic import *

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
                cool = os.path.abspath(os.path.join(os.path.dirname(__file__),'images',filename))
                img = Image.open(cool)
                img = img.convert("L")    
                # link = f'/images/monochrome/{filename}'
                link = os.path.join(os.path.dirname(__file__),'images',filename)
                img.save(link)
                return render(request,'image.html',{'form':form,'img': '/image/' + link,'msg':'monochromed'})
            
            elif edit == "mosaic":
                print(filename)
                if filename.startswith('/image'):
                    filename = filename.split('/')[3]
                print(filename)
                
                image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images',filename))
                folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images','input_images'))
   
                # image to be mosaic'd
                target_image = Image.open(image_path)
                # target_image = Image.open(args.target_image)

                # images to tile
                # input_images = getImages(args.input_folder)
                input_images = getImages(folder_path)

                # size of grid
                # resolution = (int(args.resolution[0]), int(args.resolution[1]))
                resolution = (64, 64)
                # resolution = (256, 256)

                # get largest image in input images
                largest_image = max(input_images, key=lambda x: x.size[0] * x.size[1])
                # dims = (largest_image.size[0], largest_image.size[1])


                for img in input_images:
                    # scale input images to size of largest image so they are g.t.e. the largest image of the set
                    # img.thumbnail( (largest_image.size[0] / resolution[1], largest_image.size[1] / resolution[0]) )
                    # img.resize( (largest_image.size[0] // resolution[1], largest_image.size[1] // resolution[0]) )
                    ### OR ###
                    # scale input images down to keep target_image aspect ratio
                    # img.resize((target_image.size[0] // resolution[1], target_image.size[1] // resolution[0]))
                    img.resize((target_image.size[0] // resolution[0], target_image.size[1] // resolution[1]), Image.LANCZOS)


                output_mosaic = CreateMosaic(target_image, input_images, resolution)
                print('Mosaic Complete!')

                # img = img.convert("L")    
                # link = f'/images/monochrome/{filename}'
                link = os.path.join(os.path.dirname(__file__),'images',filename)
                # img.save(link)
                output_mosaic.save(link)

                return render(request,'image.html',{'form':form,'img': '/image/' + link,'msg':'mosaic'})
        
    form = UploadForm()
    return render(request,'image.html',{'form':form})
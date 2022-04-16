import os
from PIL import Image
import numpy as np

def calcAverageRGB(image):

    img = np.array(image)

    # w - image width || h - image height || d - depth of colors, i.e. rgba = 4, rgb = 3
    w, h, d = img.shape

    # get average
    # create linear array of d-tuple (3 for rgb) with length w*h for all pixels and average over each rgb tuple
    return tuple(np.average(img.reshape(w * h, d), axis=0))

def tileImage(image, size):
    """
    _________________
    |_1_|_2_|_3_|_4_|
    |_5_|_6_|_7_|_8_|
    |_9_|_._|_._|_._|
    |_._|_._|_._|_._|
    |_._|_._|_._|_._|
    gridify the image, return this as a list of individual images
    """
    m, n = size
    w, h = image.size[0] // n, image.size[1] // m
    imgs = []
    for j in range(m):
        for i in range(n):
            chunk = image.crop((i * w, j * h, (i + 1) * w, (j + 1) * h))
            imgs.append(chunk)
    return imgs

def getImages(imageDir):
    files = os.listdir(imageDir)
    imgs = []
    for file in files:
        # get absolute path of image, script is ran from /imageMosaic/, need to join with /images/filename
        filePath = os.path.abspath(os.path.join(imageDir, file))
        try:
            fp = open(filePath, "rb")
            im = Image.open(fp)
            im.load()
            imgs.append(im)
            fp.close()
        except Exception:
            print(f"Error loading image: {file}")

    # return a list of all the images in the folder
    return imgs

def findClosestMatch(input_avg, avgs):

    index = 0                # current index
    min_index = 0            # index of running min avg.
    min_dist = float('inf')  # starting dist at infinity so first image check starts the tracking

    # calculate euclidean distance w.r.t the RGB color-space (3-dim)
    # track the minimum distance to get the image w closest avg color
    for sample in avgs:
        dist = (((sample[0] - input_avg[0]) ** 2) +
                ((sample[1] - input_avg[1]) ** 2) +
                ((sample[2] - input_avg[2]) ** 2))
        # if lower dist found, update min trackers
        if dist < min_dist:
            min_dist = dist
            min_index = index

        index += 1

    return min_index

def CreateMosaic(target_image, input_images, resolution):

    target_grid = tileImage(target_image, resolution)
    output_images = []

    # calculate average RGB for all the images
    avgs = []
    for img in input_images:
        avgs.append(calcAverageRGB(img))

    # calculate average RGB for each chunk of target image
    # find the closest image
    # add that image to the output images
    for img in target_grid:
        avg = calcAverageRGB(img)
        match_index = findClosestMatch(avg, avgs)
        output_images.append(input_images[match_index])

    # create new image with dimensions = mosaic resolution * largest of the images
    m, n = resolution
    width, height = max([img.size[0] for img in output_images]), max([img.size[1] for img in output_images])
    MOSAIC = Image.new('RGB', size=(n * width, m * height))

    # tile images onto original image
    for i in range(len(output_images)):
        row = int(i / n)
        col = i - n * row
        MOSAIC.paste(output_images[i], (col * width, row * height))

    return MOSAIC

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--target-image', dest='target_image', required=True)
    parser.add_argument('--input-folder', dest='input_folder', required=True)
    parser.add_argument('--resolution', nargs=2, dest='resolution', required=True)
    args = parser.parse_args()

    # image to be mosaic'd
    target_image = Image.open(args.target_image)

    # images to tile
    input_images = getImages(args.input_folder)

    # size of grid
    resolution = (int(args.resolution[0]), int(args.resolution[1]))

    # get largest image in input images
    largest_image = max(input_images, key=lambda x: x.size[0] * x.size[1])
    # dims = (largest_image.size[0], largest_image.size[1])


    for img in input_images:
        # scale input images to size of largest image so they are g.t.e. the largest image of the set
        img.thumbnail((largest_image.size[0], largest_image.size[1]))
        ### OR ###
        # scale input images down to keep target_image aspect ratio
        # img.thumbnail((target_image.size[0] // resolution[1], target_image.size[1] // resolution[0]))


    output_mosaic = CreateMosaic(target_image, input_images, resolution)
    output_mosaic.save('mosaic.png', 'PNG')
    print('Mosaic Complete!')
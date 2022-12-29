from PIL import Image
import json
from multiprocessing import Pool
import pygetwindow as gw
import psutil
import os
import msvcrt
import sys
import time



class Config:

    def __init__(self,
        mode = "auto",
        imageviewer = "photos",
        inputfile = "Source Files",
        outputfile = "Output Files",
        errorlog = "errorlog.txt",
        correction = "150",
        dimensions = [[740, 740]],
        formats =  ["jpg", "jpeg", "png", "webp", "bmp"]
    ):
        self.mode = mode
        self.imageviewer = imageviewer 
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.errorlog = errorlog
        self.correction = correction
        self.dimensions = dimensions
        self.formats = formats
    

    def get_configuration(self):
        return {
            "mode":self.mode,
            "imageviewer":self.imageviewer,
            "inputfile":self.inputfile,
            "outputfile":self.outputfile,
            "errorlog":self.errorlog,
            "correction":self.correction,
            "dimensions":self.dimensions,
            "formats":self.formats,
        }

config = Config().get_configuration()


def create_folders(data: dict) -> None:
    try:
        os.mkdir(data["outputfile"])
    except: pass
    for dimension in data['dimensions']:
        filename = f"{dimension[0]}x{dimension[1]}"
        try:
            os.mkdir(os.path.join(data["outputfile"], filename))
        except: pass


def get_source_filenames(data: dict) -> list[str]:
    return os.listdir(data["inputfile"])


def test_function(args):
    image, config = args
    print(image, config)


def resize_image(args):
    image, config = args

    for width, height in config['dimensions']:
        try:
            with Image.open(os.path.join(config['inputfile'], image)) as img:
                bkgd = Image.new('RGB', (width,height), (255,255,255))
                acting = max(img.height, img.width)
                correction = (width)/acting
                target = (int(img.width *correction), int(img.height * correction))
                img2 = img.resize(target, Image.Resampling.LANCZOS)
                targetpaste = (int((bkgd.width-img2.width)/2),int((bkgd.height-img2.height)/2))
                bkgd.paste(img2, targetpaste)
                out = bkgd

                out.save(os.path.join(config['outputfile'], f"{str(width)}x{str(height)}", image), quality = 95)
                print(f"Resized image: {image}")
        except:
            with open(config['errorlog'], 'a') as f:
                f.write(f"File {image} is not an image\n")


def main(threads = 4, config = config):
    create_folders(config)
    image_names = get_source_filenames(config)
    config_data = [config]*len(image_names)
    images: tuple[str, dict] = zip(image_names, config_data)
    with Pool(threads) as pool:
        pool.map(resize_image, images)


if __name__ == "__main__":
    main()




















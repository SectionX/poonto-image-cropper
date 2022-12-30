from PIL import Image
import json
from multiprocessing import Pool, cpu_count
import pygetwindow as gw
import psutil
import os
import msvcrt
import sys
from time import perf_counter, sleep, time
from typing import Generator
from pprint import pprint
from datetime import datetime as dt



class Config:

    def __init__(self,
        mode = "auto",
        imageviewer = "photos",
        inputfile = "Source Files",
        outputfile = "Output Files",
        errorlog = f"{dt.now().strftime('%Y-%m-%d-%H%M')} - errorlog.txt",
        correction = "150",
        dimensions = [[740, 740]],
        formats =  ["jpg", "jpeg", "png", "webp", "bmp"],
        threads = cpu_count() // 2
    ):
        self.mode = mode
        self.imageviewer = imageviewer 
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.errorlog = errorlog
        self.correction = correction
        self.dimensions = dimensions
        self.formats = formats
        self.threads = threads
    

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
            "threads":self.threads
        }

config = Config().get_configuration()
config_file = {}
for file in os.scandir(os.path.dirname(__file__)):
    if file.name == 'config.json':
        with open(file.name, 'r') as f: config_file = json.load(f)
        break

if config_file['mode'] != "ignore":
    for k, v in config_file.items():
        config[k] = v





def create_folders(data: dict) -> None:
    try:
        os.mkdir(data["outputfile"])
    except: pass
    for dimension in data['dimensions']:
        filename = f"{dimension[0]}x{dimension[1]}"
        try:
            os.mkdir(os.path.join(data["outputfile"], filename))
        except: pass


def get_source_filenames(data: dict) -> Generator:
    return os.scandir(data["inputfile"])


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


def main(config = config):
    print("Running application with settings:")
    pprint(config)
    sleep(3)
    create_folders(config)
    image_names = get_source_filenames(config)
    images: Generator[str, dict] = ([i.name, config] for i in image_names)
    print(sys.getsizeof(images))
    with Pool(config["threads"]) as pool:
        pool.map(resize_image, images)


if __name__ == "__main__":
    start = perf_counter()
    main()
    print(perf_counter() - start)
    input("Press enter to exit the program.")




















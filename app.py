from PIL import Image
import json
from multiprocessing import Pool
import pygetwindow as gw
import psutil
import os
import msvcrt
import sys
import time










def read_config() -> dict:
    # with open("config.pycfg") as txt:
    #     mode = (txt.readline().split(":")[1]).strip()
    #     print(mode)
    #     imageviewer = (txt.readline().split(":")[1]).strip()
    #     inputfile = (txt.readline().split(":")[1]).strip()
    #     outputfile = (txt.readline().split(":")[1]).strip()
    #     failedfile = (txt.readline().split(":")[1]).strip()
    #     correction = int((txt.readline().split(":")[1]).strip())
    #     dimensions = [(740,740), (800,800)]
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except:
        print('Error: config.json was not found. Check the documentation to create one.')
        sys.exit(1)


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
                img2 = img.resize(target, Image.LANCZOS)
                targetpaste = (int((bkgd.width-img2.width)/2),int((bkgd.height-img2.height)/2))
                bkgd.paste(img2, targetpaste)
                out = bkgd

                out.save(os.path.join(config['outputfile'], f"{str(width)}x{str(height)}", image), quality = 95)
                print(f"Resized image: {image}")
                # print("Picture saved")
                # try:
                #     gw.getWindowsWithTitle(imageviewer)[0].close()
                # except: pass
        except:
            with open(config['errorlog'], 'a') as f:
                f.write(f"File {image} is not an image\n")


def main(threads = 4, data = read_config()):
    create_folders(data)
    image_names = get_source_filenames(data)
    config_data = [data]*len(image_names)
    images: tuple[str, dict] = zip(image_names, config_data)
    with Pool(threads) as pool:
        pool.map(resize_image, images)


if __name__ == "__main__":
    main()











def to_refactor():
    for dimension in dimensions:
        width = dimension[0]
        height = dimension[1]
        print("space = ok, esp = failed, q = exit")
        imglst = os.listdir(inputfile)
        try:
            win = gw.getWindowsWithTitle("py.exe")[0]
            win.height = 200
            win.width = 400
            win.moveTo(0,0)
        except: pass
        for image in imglst:
            with Image.open(os.path.join(inputfile, image)) as img:
                bkgd = Image.new('RGB', (width,height), (255,255,255))
                acting = max(img.height, img.width)
                correction = (width-200)/acting
                target = (int(img.width *correction), int(img.height * correction))
                img2 = img.resize(target, Image.LANCZOS)
                targetpaste = (int((bkgd.width-img2.width)/2),int((bkgd.height-img2.height)/2))
                bkgd.paste(img2, targetpaste)
                out = bkgd

                out.save(os.path.join(outputfile, str(width), image), quality = 95)
                # print("Picture saved")
                try:
                    gw.getWindowsWithTitle(imageviewer)[0].close()
                except: pass








































                

                # if mode == "manual":
                #     out.show()
                #     try:
                #         win.minimize()
                #         win.restore()
                #     except: pass
                #     response = ord(msvcrt.getch())
                #     if response == 32:
                #         out.save(os.path.join(outputfile, image), quality = 95)
                #         print("Picture saved")
                #         gw.getWindowsWithTitle(imageviewer)[0].close()
                #     elif response == 113 or response == 81:
                #         gw.getWindowsWithTitle(imageviewer)[0].close()
                #         out.save(os.path.join(outputfile, image), quality = 95)
                #         print("Picture saved in Output Files")
                #     else:
                #         img.save(os.path.join(failedfile, image), quality = 95)
                #         print("Picture needs further editing")
                #         gw.getWindowsWithTitle(imageviewer)[0].close()
                # elif mode == "auto":
                #     out.save(os.path.join(outputfile, str(width), image), quality = 95)
                #     # print("Picture saved")
                #     try:
                #         gw.getWindowsWithTitle(imageviewer)[0].close()
                #     except: pass
                # else:
                #     print("Mode Error. Please make sure mode in config is either 'auto' or 'manual'")
                #     input("Press any key to exit")
                #     sys.exit()



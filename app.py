from PIL import Image
import pygetwindow as gw
import psutil
import os
import msvcrt
import sys
import time

with open("config.pycfg") as txt:
    mode = (txt.readline().split(":")[1]).strip()
    print(mode)
    imageviewer = (txt.readline().split(":")[1]).strip()
    inputfile = (txt.readline().split(":")[1]).strip()
    outputfile = (txt.readline().split(":")[1]).strip()
    failedfile = (txt.readline().split(":")[1]).strip()
    correction = int((txt.readline().split(":")[1]).strip())
    dimensions = [(740,740), (800,800)]


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

            if mode == "manual":
                out.show()
                try:
                    win.minimize()
                    win.restore()
                except: pass
                response = ord(msvcrt.getch())
                if response == 32:
                    out.save(os.path.join(outputfile, image), quality = 95)
                    print("Picture saved")
                    gw.getWindowsWithTitle(imageviewer)[0].close()
                elif response == 113 or response == 81:
                    gw.getWindowsWithTitle(imageviewer)[0].close()
                    out.save(os.path.join(outputfile, image), quality = 95)
                    print("Picture saved in Output Files")
                else:
                    img.save(os.path.join(failedfile, image), quality = 95)
                    print("Picture needs further editing")
                    gw.getWindowsWithTitle(imageviewer)[0].close()
            elif mode == "auto":
                out.save(os.path.join(outputfile, str(width), image), quality = 95)
                # print("Picture saved")
                try:
                    gw.getWindowsWithTitle(imageviewer)[0].close()
                except: pass
            else:
                print("Mode Error. Please make sure mode in config is either 'auto' or 'manual'")
                input("Press any key to exit")
                sys.exit()

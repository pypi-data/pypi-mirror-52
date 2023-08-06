import img2pdf
import os
import zipfile
import rarfile

def getImages(path):
    return [os.path.join(path, img) for img in os.listdir(path) if img.endswith(".jpg") or img.endswith(".png")]

def zipDir(path, handle):
    relroot = os.path.abspath(os.path.join(path, os.pardir))
    for root, dirs, files in os.walk(path):
        handle.write(root, os.path.relpath(root, relroot))

        for file in files:
            fileName = os.path.join(root, file)
            if os.path.isfile(fileName):
                arcname = os.path.join(os.path.relpath(root, relroot), file)
                handle.write(fileName, arcname)

class Converter:
    def toPDF(self, img_path, output):   
        with open(output, "wb") as f:
            f.write(img2pdf.convert(getImages(img_path)))

    def toCBZ(self, comic_path, output):
        handle = zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED)
        zipDir(comic_path, handle)
        handle.close()
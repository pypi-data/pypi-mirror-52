from comickaze.Comickaze import Comickaze
from comickaze.Converter import Converter
import zipfile
import os

SAMPLE_COMIC_PATH = os.path.normpath("C:\\Users\\dev\\comickaze\\downloads\\Uncanny Inhumans (2015-)\\")
OUTPUT = os.path.normpath("C:\\Users\\dev\\comickaze\\downloads\\Uncanny Inhumans (2015-).cbz")

def convertToCBZ(comic_path, output):
    converter.toCBZ(comic_path, output)


c = Comickaze()
converter = Converter()

if __name__ == "__main__":
    convertToCBZ(SAMPLE_COMIC_PATH, OUTPUT)
    pass
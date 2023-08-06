import re
from . import util, config
from .Converter import Converter
from os import path
from tqdm import tqdm
import sys
import time

HEADERS = {
    "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36",
}

# 0 - formatted title of comic, 1- chapter, 2 - page
CHAPTER_PAGE_FORMAT = "https://readcomicsonline.ru/comic/{0}/{1}/{2}"
# 0 - formatted title of comic, 1 - chapter, 2 - page
IMAGE_DL_FORMAT = "https://readcomicsonline.ru/uploads/manga/{0}/chapters/{1}/{2}.jpg"

class Downloader:
    def __init__(self, comic, dl_path, dl_range="*", session=None, output_format="cbz"):
        self.COMIC = comic
        self.DL_PATH = path.join(path.normpath(dl_path), self.cleanPath(self.COMIC["title"]))
        self.URL_COMIC = self.getURLComicTitle()

        if session == None:
            self.SESSION = util.createSession()
        else:
            self.SESSION = session

        self.RANGE = dl_range
        self.OUTPUT_FORMAT = output_format
        self.TO_DL = self.getToBeDownloadedChapters()

        util.createFolder(self.DL_PATH)

    def getToBeDownloadedChapters(self):
        if self.RANGE != "*":
            start = int(self.RANGE[0]) - 1
            end = self.RANGE[1]
            if end == "*":
                return self.COMIC["chapters"][start:]
            else:
                end = int(end)
                return self.COMIC["chapters"][start:end]

        return self.COMIC["chapters"]

    def cleanPath(self, path):
        return re.sub("[\\/:*?\"<>|]", ' ', path)

    def getURLComicTitle(self):
        return self.COMIC["link"].split("/")[4]

    def getURLChapter(self, chapterLink):
        return chapterLink.split("/")[-1]

    def formatPageNum(self, page):
        if int(page) < 10:
            return "0" + page
        return page

    def getPages(self, chapter, referer):
        headers = HEADERS
        headers["referer"] = referer

        soup = util.soupify(self.SESSION.get(chapter["chapterLink"], headers=headers, cookies=self.SESSION.cookies).text)
        select = soup.find("select", attrs={"id": "page-list", "class": "selectpicker"})
        pages = select.find_all("option")

        return [(i + 1, IMAGE_DL_FORMAT.format(self.URL_COMIC, self.getURLChapter(chapter["chapterLink"]), self.formatPageNum(page["value"]))) for i, page in enumerate(pages)]

    def downloadPage(self, dl_path, page, pbar):
        link = page[1]
        fileName = link.split("/")[-1]
        fileDir = path.normpath(path.join(dl_path, fileName))

        try:
            r = self.SESSION.get(link, stream=True, headers=HEADERS, cookies=self.SESSION.cookies)
            r.raise_for_status()
            if r.status_code == 200 or r.status_code == 304:
                with open(fileDir, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
            else:
                pbar.write("Could not download this page: {0}".format(page))
                pbar.write("Error: {0}".format(r.status_code))
        except Exception as e:
            pbar.write("Something went wrong.")
            pbar.write("Error: {0}".format(repr(e)))
            sys.exit()


    def startDownload(self):
        currReferer = self.COMIC["link"]

        for chapter in self.TO_DL:
            title = self.COMIC["title"]
            chapterTitle = chapter["chapterTitle"]

            pages = self.getPages(chapter, currReferer)

            pbar = tqdm(total=len(pages), position=0, unit="page(s)")
            pbar.set_description("Comickaze :: Downloading {0}".format(chapterTitle))

            for page in pages:
                downloadFolder = path.join(self.DL_PATH, self.cleanPath(chapterTitle))
                util.createFolder(downloadFolder)

                self.downloadPage(downloadFolder, page, pbar)
                pbar.update()
                # time.sleep(0.5)

            pbar.close()

            if self.OUTPUT_FORMAT != "jpg":
                convert = Converter()
                if self.OUTPUT_FORMAT == "pdf":
                    convert.toPDF(downloadFolder, path.join(path.dirname(downloadFolder), chapterTitle + ".pdf"))
                    util.deleteFolder(downloadFolder)
                    
            time.sleep(2)
            currReferer = chapter["chapterLink"]

        if self.OUTPUT_FORMAT == "cbz":
            convert.toCBZ(self.DL_PATH, path.join(path.dirname(self.DL_PATH), title + ".cbz"))

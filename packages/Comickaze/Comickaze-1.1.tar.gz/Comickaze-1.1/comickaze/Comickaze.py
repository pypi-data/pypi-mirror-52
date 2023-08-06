import click
from . import util, config
from .Downloader import Downloader

BASE = "https://readcomicsonline.ru/"
SEARCH_URL = BASE + "search"
COMIC_URL = BASE + "comic/"
HEADERS = {
    "referer": BASE,
    "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36",
}

class Comickaze:
    def __init__(self):
        self.SESSION = util.createSession()

    def search(self, keyword):
        params = {
            "query": keyword
        }
        headers = HEADERS
        headers["x-requested-with"] = "XMLHttpRequest"
        data = self.SESSION.get(SEARCH_URL, params=params, headers=headers, cookies=self.SESSION.cookies).json()

        comics = data["suggestions"]

        if comics:
            res = [{"title": comic["value"], "link": COMIC_URL + comic["data"]} for comic in comics]
            return res

        return None

    def downloader(self, comic, dl_path, dl_range="*", output_format="cbz"):
        comic["chapters"] = self.getComicChapters(comic)
        return Downloader(comic, dl_path, dl_range=dl_range, session=self.SESSION, output_format=output_format)

    def getComicChapters(self, comic):
        data = self.SESSION.get(comic["link"], headers=HEADERS).text

        soup = util.soupify(data)

        chaptersList = soup.find("ul", attrs={"class": "chapters"})

        chapters = []
        for chapter in chaptersList.find_all("li"):
            h5 = chapter.find("h5", attrs={"class": "chapter-title-rtl"})
            title = h5.text.strip()
            link = h5.find("a")["href"]

            chapters.append({
                "chapterTitle": title,
                "chapterLink": link
            })

        # reversed
        return chapters[::-1]

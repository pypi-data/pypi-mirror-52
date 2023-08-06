from comickaze.Comickaze import Comickaze

c = Comickaze()
res = c.search("Deadpool")
comic = res[0]
c.downloader(comic).startDownload()
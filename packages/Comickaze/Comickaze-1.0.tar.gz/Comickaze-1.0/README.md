# Comickaze
> A Python CLI that scrapes and lets you download comics easily.
> Comickaze gets comic data, images from ReadComicsOnline.ru

![Comickaze Demo](https://i.imgur.com/a1LY2hH.gif "Comickaze Demo")

### Sample Usage ###

**Command line:**

```comickaze dl "deadpool"```

### Module: ###

```python
from comickaze.Comickaze import Comickaze

c = Comickaze()
res = c.search("Deadpool")
comic = res[0] #gets the first result
c.downloader(comic).startDownload()
```

### Arguments ###

**Command line:**

```
--path                          Specifies the download directory
--dl-range      --range         Specifies the range of issues to be downloaded, <start>-<end>. Can use * at the <end> to download all chapters from <start>.
```

### Methods: ###

+ search(keyword)
```python
res = c.search("Deadpool")
```

+ downloader(comic, dl_range (default: *), path (default: C:\Users\<User>\comickaze\downloads))
```python
downloader = c.downloader(comic)
```

+ Downloader.startDownload()
```python
downloader.startDownload()
```
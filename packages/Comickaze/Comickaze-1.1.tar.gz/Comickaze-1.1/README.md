# Comickaze
> A Python CLI that scrapes and lets you download comics easily.
> Comickaze gets comic data, images from ReadComicsOnline.ru

![Comickaze Demo](https://i.imgur.com/a1LY2hH.gif "Comickaze Demo")

### Install ###

```pip install Comickaze```

### Sample Usage ###

**Command line:**

```comickaze dl "deadpool"```

### Install ###

```pip install Comickaze```

### Module: ###

```python
from comickaze.Comickaze import Comickaze

c = Comickaze()
res = c.search("Deadpool")
comic = res[0] #gets the first result
c.downloader(comic).startDownload()
```

### CLI Commands ###

```
config      Comickaze : Configuration
dl          Comickaze : Downloader
```

**DL**

```
--path PATH                                     Specifies the download directory
--dl-range, --range TEXT                        Specifies the range of issues to be
                                                downloaded, Ex: 1-5 or 1-*. See docs for
                                                valid inputs.  [default: *]
--output-format, --format [cbz|pdf|jpg]     Specifies the output format of the download
                                comics
```

### Methods: ###

**Comickaze**

```python
Comickaze()
```

+ search(keyword)

```python
res = c.search("Deadpool")
```

+ getComicChapters(comic)

```python
chapters = c.getComicChapters(res[0])
```

+ downloader(comic, dl_path, dl_range="*", output_format="cbz")

```python
downloader = c.downloader(comic, "C:\\")
```

**Downloader**

```python
Downloader(comic, dl_path, dl_range="*", session=None, output_format="cbz")
```

+ startDownload()

```python
downloader.startDownload()
```

**Converter**

```python
Converter()
```

+ toPDF(img_path, output)

+ toCBZ(comic_path, output)

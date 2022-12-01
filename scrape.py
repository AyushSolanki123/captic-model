from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import requests


def scrape_bbc(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)

    t = soup.find("h1", {"class": "ssrcss-15xko80-StyledHeading e1fj1fc10"})
    if t != None:
        title = t.text.strip()
        images = soup.findAll("img", {
            "class": "ssrcss-evoj7m-Image ee0ct7c0", "srcset": True, "loading": "eager"})
        caption = soup.findAll(
            "div", {"class": "ssrcss-y7krbn-Stack e1y4nx260", "spacing": 6})
        articles = soup.findAll(
            "div", {"class": "ssrcss-7uxr49-RichTextContainer e5tfeyi1"})

        image_links = []
        image_alts = []
        image_captions = []

        for i in images:
            a = i.get('src')
            b = i.get('alt')
            image_links.append(a)
            image_alts.append(b)

        for i in caption:
            if (1 != len(image_captions)):
                image_captions.append(i.text.strip())

        article = ''
        for i in articles:
            article += str(i.text.strip())

        data = {
            'title': title,
            'image_urls': image_links[0],
            'image_alts': image_alts[0],
            'captions': image_captions[0],
            'article': article,
        }
        return data
    else:
        return None


def scrape_toi(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)

    t = soup.find("h1", {"class": "_1Y-96"})
    if t != None:
        title = t.text.strip()
        image = soup.findAll("img", {"fetchpriority": "high"})

        j = soup.find('div', {"data-articlebody": "1"})
        article = j.find("div", {"class": "_3YYSt"}).text.strip()
        image_link = ""
        image_alt = ""
        image_caption = ""

        for i in image:
            a = i.get('src')
            b = i.get('alt')
            c = i.get('title')
            image_link = a
            image_alt = b
            image_caption = c

        data = {
            'title': title,
            'image_urls': image_link,
            'image_alts': image_alt,
            'captions': image_caption,
            'article': article,
        }
        return data
    else:
        return None


def scrape_hitwada(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)

    t = soup.find("div", {"class": "heading clsNewsTitleHeading2"})
    if t != None:
        title = t.text.strip()

        image = soup.findAll("img")
        articles = soup.findAll("div", {"id": "pastingspan1"})
        image_link = ""
        image_alt = ""
        image_caption = ""

        for i in image:
            a = i.get('src')
            b = i.get('alt')
            c = i.get('title')
            image_link = a
            image_alt = b
            image_caption = c

        if articles == []:
            articles = soup.findAll("div", {"class": "newscontent"})

        article = ""
        for i in articles:
            article += i.text.strip()

        data = {
            'title': title,
            'image_urls': image_link,
            'image_alts': image_alt,
            'captions': image_caption,
            'article': article,
        }
        return data
    else:
        return None

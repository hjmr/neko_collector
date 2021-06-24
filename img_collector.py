import os
import time
import random
import argparse
import urllib.error
import urllib.request

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from bs4 import BeautifulSoup


BASE_URL = "https://www.neko-jirushi.com"
QUERY_URL = BASE_URL + "/foster/cat/kw-{}"


def parse_arg():
    parser = argparse.ArgumentParser(description="search and retrieve cats' images.")
    parser.add_argument("-t", "--save_to", type=str, help="specify a folder to where images will be saved.")
    parser.add_argument("QUERY", type=str, help="query keyword.")
    return parser.parse_args()


def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
            local_file.write(web_file.read())
    except urllib.error.URLError as e:
        print(e)


def download_file_to_dir(url, dst_dir):
    download_file(url, os.path.join(dst_dir, os.path.basename(url)))


def extract_image_urls(driver, url, page):
    img_urls = []
    page_url = url + "/?page={}".format(page)

    try:
        driver.get(page_url)
        time.sleep(5)  # 5秒待つ
        html = driver.page_source.encode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        main_area = soup.find("div", {"id": "vueRootArea"})
        img_area = main_area.find("div", {"class": "kitten-row"})
        img_list = img_area.select("div.item_img > a > img")
        for item in img_list:
            img_urls.append(item["src"].split("?")[0])
    finally:
        driver.close()
    return img_urls


def retrieve_images(url_list, save_to):
    for url in url_list:
        full_url = BASE_URL + url
        print(full_url)
        if save_to is not None:
            download_file_to_dir(full_url, save_to)
            time.sleep(random.uniform(1, 3))  # 1〜3秒待つ


def main(query, save_to):
    try:
        driver = webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME)
        url = QUERY_URL.format(query)
        page = 1
        img_urls = extract_image_urls(driver, url, page)
        while 0 < len(img_urls):
            retrieve_images(img_urls, save_to)
            img_urls = extract_image_urls(driver, url, page)
    finally:
        driver.quit()


if __name__ == "__main__":
    args = parse_arg()
    main(query=args.QUERY, save_to=args.save_to)

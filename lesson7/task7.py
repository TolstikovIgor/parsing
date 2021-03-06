import time
from tqdm import tqdm
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient

some_text = "рок"

PAUSE_TIME = 3
url = "https://vk.com/tokyofashion"
DRIVER_PATH = "./chromedriver"

driver = webdriver.Chrome(DRIVER_PATH)
driver.get(url)

MONGO_URL = "127.0.0.1:27017"
MONGO_DB = "vk_posts"
client = MongoClient(MONGO_URL)
db = client[MONGO_DB]
collection = db["posts"]


def insert_posts_to_db(collection, info_list):
    for item in info_list:
        collection.update_one({"$and": [{'link': {"$eq": item['link']}},
                                        {'text': {"$eq": item['text']}}]},
                              {'$set': item}, upsert=True)
    print('Посты загружены в базу данных!')


def find_on_wall(what_find):

    find_button = driver.find_element_by_xpath('//a[contains(@class, "ui_tab_search")]')
    time.sleep(PAUSE_TIME)
    find_button.click()
    time.sleep(PAUSE_TIME)
    find_field = driver.find_element_by_id("wall_search")
    # find_field.click()
    time.sleep(PAUSE_TIME)
    find_field.send_keys(what_find + Keys.ENTER)
    print('Поиск по постам завершен!')


def scroll_page(limit):
 
    html = driver.find_element_by_tag_name('html')
    for _ in range(limit):
        time.sleep(PAUSE_TIME)
        try:
            close_button = driver.find_element_by_xpath('//a[contains(@class, "JoinForm__notNow")]')
            if close_button:
                close_button.click()
        except Exception as e:
            print(e)
        finally:
            html.send_keys(Keys.END)
    print(f'Готово!')


def scroll_page_unlim():

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        time.sleep(PAUSE_TIME)
        try:
            close_button = driver.find_element_by_xpath('//a[contains(@class, "JoinForm__notNow")]')
            if close_button:
                close_button.click()
        except Exception as e:
            print(e)
        finally:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    print(f'Готово!')


def get_posts_info():
    items = driver.find_elements_by_xpath('//div[contains(@class, "_post post")]')
    print(f'Количество постов {len(items)}')
    info_items = []
    for item in tqdm(items[:]):
        info = {}
        try:
            info["text"] = item.find_element_by_xpath('.//div[contains(@class, "wall_post_text")]').text
            info["link"] = item.find_element_by_xpath('.//a[contains(@class,"post_link")]').get_attribute('href')
            info["date"] = item.find_element_by_xpath('.//span[contains(@class,"rel_date")]').text
            info["likes"] = item.find_element_by_xpath('.//a[contains(@class, "like_btn like _like")]//div[contains(@class, "like_button_count")]').text
            info["shares"] = item.find_element_by_xpath('.//a[contains(@class, "like_btn share _share")]//div[contains(@class, "like_button_count")]').text
            info["views"] = item.find_element_by_xpath('.//div[contains(@class, "_views")]').text
        except Exception as e:
            print(e)
        pprint(info)
        try:
            if info["text"]:
                info_items.append(info)
        except Exception as e:
            print(e)
        time.sleep(PAUSE_TIME)
    return info_items


if __name__ == '__main__':
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.ARROW_DOWN + Keys.ARROW_DOWN + Keys.ARROW_DOWN)
    # find_on_wall(some_text)
    # time.sleep(PAUSE_TIME)
    scroll_page(5)
    # scroll_page_unlim()
    # time.sleep(PAUSE_TIME)
    posts_info = get_posts_info()
    time.sleep(PAUSE_TIME)
    driver.quit()
    pprint(posts_info)
    insert_posts_to_db(collection, posts_info)

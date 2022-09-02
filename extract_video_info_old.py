import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_format(driver:webdriver) -> str :
    """
    Get the format of the given YouTube video page. \n
    It is observed that while using test softwares like Selenium,
    two different formats of webpage is shown for the same url.
    Hence, this function returns the format of the loaded page.
    :param driver: Selenium driver
    :return: returns 'new' for new format and 'old' for the old format
    """
    content = driver.find_element(By.ID, "below")
    try :
        channel_info = content.find_element(By.ID, "above-the-fold")
        Format = 'new'
    except :
        try :
            title_info = content.find_element(By.ID, "info-contents")
            Format = 'old'
        except Exception as e:
            print(e)

    return Format

def get_title(driver:webdriver) -> str :
    """
    Fetch the title of the youtube video \n
    :param driver: selenium webdriver
    :return: title string
    """

    content = driver.find_element(By.ID, "below")
    title =  ''

    if get_format(driver) == 'new':
        try :
            channel_info = content.find_element(By.ID, "above-the-fold")
            title_info = channel_info.find_element(By.ID, "title").find_element(By.TAG_NAME, "h1")
            title = title_info.find_element(By.TAG_NAME, "yt-formatted-string").get_attribute("innerHTML")
            print(title)
        except Exception as e:
            print(e)
    else :
        try :
            title_info = content.find_element(By.ID, "info-contents").find_element(By.TAG_NAME, "h1")
            title = title_info.find_element(By.TAG_NAME, "yt-formatted-string").get_attribute("innerHTML")
            print(title)
        except Exception as e:
            print(e)

    return title

def get_views_date(driver:webdriver) -> dict :
    """
    Fetch views and date from the YouTube video page. \n
    :param driver:
    :return: dictionary containing 'views' and 'date' as keys
    """

    result = {'views' : '', 'date' : ''}

    content = driver.find_element(By.ID, "below")
    if get_format(driver) == 'new':
        try :
            channel_info = content.find_element(By.ID, "above-the-fold")
            info = channel_info.find_element(By.ID, "top-row").find_element(By.ID, "description")
            tag = info.find_element(By.ID, "formatted-snippet-text").find_elements(By.TAG_NAME, "span")
            result['views'] = tag[0].get_attribute("innerHTML")
            result['date'] = tag[2].get_attribute("innerHTML")
            print(result['views'], result['date'])

        except Exception as e:
            print(e)
    else :
        try :
            info = content.find_element(By.ID, "info-contents").find_element(By.ID, "info")

            views_tag = info.find_element(By.ID, "count").find_elements(By.TAG_NAME, "span")[0]
            result['views'] = views_tag.get_attribute("innerHTML")
            print(result['views'])

            date_tag = info.find_element(By.ID, "info-strings").find_element(By.TAG_NAME, "yt-formatted-string")
            result['date'] = date_tag.get_attribute("innerHTML")
            print(result['date'])
        except Exception as e:
            print(e)

    return result





def extract_video_info(driver: webdriver, video_link:str):
    driver.maximize_window()
    driver.get(video_link)
    time.sleep(5)

    title = get_title(driver)
    print("Title is : %s" %title)

    print(get_views_date(driver))




opt = webdriver.ChromeOptions()
opt.add_argument("user-agent=Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
driver = webdriver.Chrome(options=opt)

extract_video_info(driver, "https://www.youtube.com/watch?v=k2P_pHQDlp0")
#driver.close()
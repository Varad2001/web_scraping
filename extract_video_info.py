import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# function : in case there are errors due to different page formats
def get_proper_format(video_link:str) -> webdriver :
    while True :
        driver = webdriver.Chrome()
        driver.get(video_link)
        try :
            info = driver.find_element(By.ID, "below").find_element(By.ID, "above-the-fold")
            print("This format is not supported. Retrying...")
            driver.close()
        except :
            print("Valid format page found.")
            return driver

def get_title(driver:webdriver) -> str :
    """
    Fetch the title of the youtube video \n
    :param driver: selenium webdriver
    :return: title string
    """

    content = driver.find_element(By.ID, "below")
    title =  ''

    try :
        title_info = content.find_element(By.ID, "info-contents").find_element(By.TAG_NAME, "h1")
        title = title_info.find_element(By.TAG_NAME, "yt-formatted-string").get_attribute("innerHTML")
    except Exception as e:
        print(e)

    return title

def get_views_date_likes(driver:webdriver) -> dict :
    """
    Fetch views and date from the YouTube video page. \n
    :param driver:
    :return: dictionary containing 'views' and 'date' as keys
    """

    result = {'views' : '', 'date' : '' , 'likes' : ''}

    content = driver.find_element(By.ID, "below")
    try :
        info = content.find_element(By.ID, "info-contents").find_element(By.ID, "info")

        views_tag = info.find_element(By.ID, "count").find_elements(By.TAG_NAME, "span")[0]
        result['views'] = views_tag.get_attribute("innerHTML")

        date_tag = info.find_element(By.ID, "info-strings").find_element(By.TAG_NAME, "yt-formatted-string")
        result['date'] = date_tag.get_attribute("innerHTML")

        likes_tag = info.find_element(By.ID, "menu").find_element(By.TAG_NAME, "ytd-toggle-button-renderer").find_element(By.TAG_NAME, "yt-formatted-string")
        result['likes'] = likes_tag.get_attribute("innerHTML")
    except Exception as e:
        print(e)

    return result

def get_channel_info(driver:webdriver) -> dict:
    result = {'channel_name' : '', 'subscribers':'' }
    content = driver.find_element(By.ID, "below")
    info = content.find_element(By.ID, "meta-contents")

    channel_tag = info.find_element(By.ID, "channel-name").find_element(By.TAG_NAME, "a")
    result['channel_name'] = channel_tag.get_attribute("innerHTML")

    subs_tag = info.find_element(By.ID, "owner-sub-count")
    result['subscribers'] = subs_tag.get_attribute("innerHTML")

    return result

def get_comments_info(driver:webdriver) :
    # load the comments section first by scrolling down
    js_query = "window.scrollBy(0, " \
               "document.getElementById('player').scrollHeight  + " \
               "document.getElementById('info').scrollHeight +" \
               "document.getElementById('meta').scrollHeight);"
    driver.execute_script(js_query)
    time.sleep(4)

    content = driver.find_element(By.ID, "below")
    comment_section = driver.find_element(By.ID, "comments")


    # extract the number of comments
    comment_number_tag = comment_section.find_element(By.ID, "header").find_element(By.ID, "title")
    comment_number_tag = comment_number_tag.find_elements(By.TAG_NAME, "span")[0]
    comments_num = comment_number_tag.get_attribute("innerHTML")
    comments_num = int(comments_num.replace(',',''))
    print("Total comments : %s" %comments_num)

    comments = []           # format : [{'name':"text"}, ... ]
    while len(comments) < comments_num:
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight || document.documentElement.scrollHeight);")
        comments_tags = comment_section.find_element(By.ID, "contents").find_elements(By.TAG_NAME,
                                                                                      "ytd-comment-thread-renderer")

        for comment_tag in comments_tags[len(comments):]:
            header_info = comment_tag.find_element(By.ID, "header")
            commenter_name = header_info.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "span").get_attribute("innerHTML")
            print(commenter_name)
            comment_time = header_info.find_element(By.TAG_NAME, "yt-formatted-string").find_element(By.TAG_NAME, "a").get_attribute("innerHTML")
            print(comment_time)

            comment_info = comment_tag.find_element(By.ID, "comment-content").find_element(By.ID, "content")
            comment_text = comment_info.find_element(By.TAG_NAME, "yt-formatted-string").get_attribute("innerHTML")
            print(comment_text)





def extract_video_info(video_link:str):
    #driver = get_proper_format(video_link)
    driver = webdriver.Chrome()
    driver.get(video_link)
    driver.maximize_window()
    time.sleep(3)

    print(get_title(driver))
    print(get_views_date_likes(driver))
    print(get_channel_info(driver))
    print(get_comments_info(driver))

extract_video_info( "https://www.youtube.com/watch?v=AuqZ4recf0s")

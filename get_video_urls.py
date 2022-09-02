import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
logging.basicConfig(filename="video_scraper.log", level=logging.INFO, format="%(name)s:%(levelname)s:%(asctime)s:%(message)s" )


def get_video_urls(driver: webdriver,channel_link : str , number_of_videos : int) -> list :
    """
    :param channel_link: url of the youtube channel
    :param number_of_videos: number of videos to fetch
    :return: list containing urls of the videos
    """

    logging.info("\nGET_VIDEO_URLS:")
    driver.maximize_window()
    try:
        driver.get(channel_link+"/videos")
    except Exception as e:
        logging.exception(e)
    time.sleep(1)
    
    # select the 'SORT-BY' option to 'Most recent'
    try :
        sort_button = driver.find_element(By.ID, "sort-menu")
        sort_button.click()
        sort_options = sort_button.find_elements(By.TAG_NAME, "a")
        opt1 = sort_options[2].find_elements(By.TAG_NAME,"div")
        logging.info("Selecting option :%s" %opt1[0].get_attribute("innerHTML") )

        # get the webpage for the selected option
        link = sort_options[2].get_attribute("href")
        driver.get(link)
        time.sleep(1.5)
    except Exception as e:
        logging.exception(e)
    
    
    # now we are on the 'Most recent videos' page
    # get the video urls by selecting proper elements
    try :
        videos = driver.find_elements(By.XPATH, "//div[@id='contents']")[1]
        videos = videos.find_element(By.ID, "items")
        logging.info("Reached items tag...")       # 'items' tag contains the info related to all the videos
    except Exception as e:
        logging.exception(e)


    video_urls = []         # to save urls 
    finished = 0            # flag to know if the task is complete

    logging.info("Starting extraction ....")

    while len(video_urls) < number_of_videos:
            # scroll down
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight || document.documentElement.scrollHeight);")
            time.sleep(1)

            try :
                videos_tag = videos.find_elements(By.ID, "dismissible")
            except Exception as e:
                logging.exception(e)

            # if there are no more videos to load, i.e., if we have reached to the end
            if len(videos_tag) == len(video_urls) :
                logging.info("Cannot scroll down... Reached to the end...")
                logging.info("Extracted %s videos. Complete." % len(video_urls))
                break
    
            logging.info("Found %s elements ...." %len(videos_tag))

            # extract the links
            for elem in videos_tag[len(video_urls):]:
                link = elem.find_element(By.TAG_NAME, "a")
                url = link.get_attribute("href")
                video_urls.append(url)

                if len(video_urls) == number_of_videos:
                    logging.info("Extracted %s videos. Complete." %len(video_urls))
                    finished = 1
                    break
    
            if finished :
                break
            else :
                logging.info("Scrolling down and looking for more videos... ")

    logging.info("\nGET_VIDEO_URLS FUNCTION COMPLETE.\n")
    return video_urls



driver = webdriver.Chrome()
urls = get_video_urls(driver, "https://www.youtube.com/c/iNeuroniNtelligence", 10)


driver.close()



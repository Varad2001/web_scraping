from db_ops import mongodb_ops, sql_ops
from flask import request, render_template, Flask
from selenium import webdriver
import channel
import os
import pickle
import logging
logging.basicConfig(filename="video_scraper.log", level=logging.INFO, format="%(name)s:%(levelname)s:%(asctime)s:%(message)s" )


app = Flask(__name__)

# global variables
channel2 = None
url = ''
num = 0
driver = None
counter = 0

@app.route('/')
def home_page():
    logging.info("\nApp running....rendering index.html...")
    return render_template("index.html")


@app.route('/results', methods=['POST'])
def get_results():
    if request.method == 'POST' :
        logging.info("Getting input for channel name and number of videos...")
        global driver, channel2, num , url

        url = request.form['url']
        num = int(request.form['num'])
        try :
            # set up selenium webdriver
            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
                                      chrome_options=chrome_options)

            channel2 = channel.Channel(url, driver)          # create a channel object instance
            channel2.get_channel_info(driver)        # get the channel details
            channel_file = open('channel_obj', 'ab')
            pickle.dump(channel2, channel_file)
        except Exception as e:
            logging.exception(e)
            return "<p>%s</p>" %e

        logging.info("Input for channel name and videos number received. Rendering results.html...")
        return render_template("results.html", name=channel2.name, subs= channel2.subscribers)

@app.route('/get_urls', methods=['POST'])
def get_urls():
    global driver, channel2, url , num

    try :
        channel2 = pickle.load(open('channel_obj', 'rb'))
        channel2.get_video_urls(num, driver)         # retrieve the urls of the videos

        data = []
        for video in channel2.video_objs:
            data.append(str(video.video_url))
    except Exception as e:
        return "<p>%s</p>" %e

    logging.info("Rendering get_urls.html....")
    return render_template("get_urls.html", urls = data)

@app.route('/save_data', methods=['POST'])
def save_videos():
    global driver, channel2
    try :
        channel2 = pickle.load(open('channel_obj', 'rb'))
        channel2.save_data()
    except Exception as e:
        logging.exception(e)

    logging.info("All data saved.")
    return "<h2>All data have been saved successfully !!</h2>"


@app.route('/get_updates', methods=['POST'])
def updates():
    global counter,channel2
    logging.info("Getting updates...")
    try :
        channel2 = pickle.load(open('channel_obj', 'rb'))
        data = sql_ops.fetch_data(channel2.name, "videodata")
    except Exception as e:
        logging.exception(e)
        return "<p>Fetching data failed.</p>"
    if counter < len(data):
        titles = []
        i = counter
        for v in data[counter:]:
            title = v[1]
            titles.append(title)
        counter = len(data)

        logging.info("Updates received. Rendering video.html..")
        return render_template("video.html", video_names = titles, idx=i+1)

    msg = "<p>No new data updated to the database yet... please make sure you have clicked 'Save data' button; " \
           "if done already,please try again after about 4-5 seconds.</p><hr>"
    return msg




if __name__ == '__main__':
    app.run()
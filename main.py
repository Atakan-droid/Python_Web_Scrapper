
import base64
from io import BytesIO
import numpy as np
import requests
import cv2

from gi_scraper import Scraper
from PIL import Image
import os
# The object creation has an overhead time
# The same object can be reused to fire multiple queries

# headless=True will run the browser in background
query_param = {"sarma":50,"pizza":50,"burger":50,"pasta":50}

def scraper(param):
    sc = Scraper(headless=True)

    print("Querying...", param[0])

        # scrape method returns a stream object
    stream = sc.scrape(param[0], param[1])

        # stream.get method yields Response object with following attributes
        # - query (str): The query associated with the response.
        # - name (str): The name attribute of the response.
        # - src_name (str): The source name attribute of the response.
        # - src_page (str): The source page attribute of the response.
        # - thumbnail (str): The thumbnail attribute of the response.
        # - image (str): The image attribute of the response.
        # - width (int): The width attribute of the response.
        # - height (int): The height attribute of the response.
    count = 0
    for response in stream.get():
            # response.to_dict returns python representable dictionary
        print(response.thumbnail)

        try:
            base64Img = response.thumbnail.split(',')[1]
            img = Image.open(BytesIO(base64.b64decode(base64Img)))
        except:
            img_data = requests.get(response.thumbnail).content
            img = Image.open(BytesIO(img_data))
        count += 1
        img = np.array(img)
        img = cv2.resize(img,(224,224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(f'{param[0]}_{count}' + '.jpg', img)

    # call this to terminate scraping (auto-called by destructor)
    sc.terminate()


if __name__ == "__main__":
    os.makedirs('Images', exist_ok=True)
    os.chdir('Images')
    for index,item in enumerate(query_param.items()):
        print("Starting to download images for ",item[0],"...")
        os.makedirs(item[0], exist_ok=True)
        os.chdir(item[0])
        scraper(item)
        os.chdir('..')
        print("Downloaded images for ",item[0],"...")
    os.chdir('..')
    print("Downloaded all images...")
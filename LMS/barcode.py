
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import bs4
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup

class BarCode:
    def fetchcode(self):
        # code = None
        # cap = cv2.VideoCapture(0)
        # while code is None:
        #     _, frame = cap.read()

        #     decodedObjects = pyzbar.decode(frame)
        #     for obj in decodedObjects:
        #         code=obj.data.decode('ascii')
                
        #     cv2.imshow("Frame", frame)
        #     cv2.waitKey(1)

        # # print(data)                              # B016ENLJJM
        cv2.destroyAllWindows()
        code = "9780262033848"
        my_url = "https://google.com/search?q=" + code

        # print(my_url)

        req = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})
        uClient = urlopen(req)
        webpage = uClient.read()
        uClient.close()
        page_soup = soup(webpage,"html.parser")  

        find1 = page_soup.findAll("span")
        title = find1[15].text
        return title,code
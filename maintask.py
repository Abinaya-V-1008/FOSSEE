import sys
import requests

import os
import random

from urllib.parse import urljoin
from bs4 import BeautifulSoup


from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton,QLabel


class MWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Task")
        #self.setContentsMargins(20,20,20,20)

        self.setFixedSize(QSize(500,300))
        button=QPushButton("Press me!",self)
        button.move(50,50)
        button.clicked.connect(self.onclick)
        #button.pressed.connect(self.onclick)
        #button.released.connect(self.onclick)

        self.image_label = QLabel(self)

        # Define the base URL
        base_url = "https://github.com/hfg-gmuend/openmoji/tree/master/src/symbols/geometric"

        # Send a GET request to the base URL
        response = requests.get(base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        link_tags = soup.find_all("a", class_="js-navigation-open")

        # Create a directory to save the downloaded images
        os.makedirs("downloaded_images", exist_ok=True)

        for link_tag in link_tags:
            href = link_tag.get("href")
            
            if href.endswith(".svg"):
                image_url = urljoin(base_url, href)
                
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                
                filename = os.path.basename(href)
                
                save_path = os.path.join("downloaded_images", filename)
                
                
                with open(save_path, "wb") as f:
                    f.write(image_response.content)
                
                print(f"Downloaded: {filename}")

        print("All images downloaded successfully.")

    def onclick(self):
        image_files = os.listdir("downloaded images")
        image_label = QLabel(window)
        image_label.setScaledContents(True)  

        #Function to load and display a random image
        def display_random_image():
            # Choose a random image file
            image_file = random.choice(image_files)
            
            pixmap = QPixmap(os.path.join("downloaded_images", image_file))
            
            image_label.setPixmap(pixmap)
            window.resize(pixmap.width(), pixmap.height())

        # Display the initial random image
        display_random_image()
app=QApplication(sys.argv)

window=MWindow()
window.show()

app.exec()

       
    
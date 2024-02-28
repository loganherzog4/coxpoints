from PIL import Image
from pytesseract import Output

import cv2
import pytesseract


class DataService:

    def generate_csv(self, base_path: str, folders: list[str]):
        """
        1) Loops through each Chambers of Xeric loot image in each folder in folders list.
        2) Uses OCR to grab raid points value.
        3) Writes raid type, file name, date, and raid points to dict.
        4) Create DataFrame from dict and csv from DataFrame.

        :param base_path: Base path where folders are located.
        :param folders: Folders containing image files (RuneScape usernames).
        :return: Raid points .csv.
        """

        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        images = [f"{base_path}\\{folders[0]}\\Boss Kills\\Chambers of Xeric Challenge Mode(64) 2021-12-01_21-54-51.png"]
        for image_path in images:
            img = cv2.imread(image_path)[63:182, 1293:1420]
            text = pytesseract.image_to_string(img, lang="eng")
            print(text)

from PIL import Image
from pytesseract import Output

import cv2
import os
import pandas as pd
import pytesseract
import re


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
        data = {
            "Date": [],
            "Username": [],
            "KC": [],
            "Points": []
        }
        for folder in folders:
            directory = f"{base_path}\\{folder}\\Boss Kills\\"
            for file in os.listdir(directory):
                file_name = os.fsdecode(file)
                if file_name.startswith("Chambers of Xeric Challenge Mode"):
                    # Grab date from file name.
                    split_name = file_name.split(' ')
                    date = split_name[5][:-4]
                    data["Date"].append(date)

                    username = folder
                    data["Username"].append(username)

                    # Grab KC from file name.
                    kc = split_name[4][5:-1]
                    data["KC"].append(kc)

                    # Grab points from box within image.
                    try:
                        img = cv2.imread(os.path.join(directory, file_name))[63:182, 1293:1420]
                        text = pytesseract.image_to_string(img, lang="eng")
                        split_text = re.split(" |\\n", text)
                        if split_text[4] in ['', "Time"]:
                            pts_index = 3
                        elif split_text[5] in ['', "Time"]:
                            pts_index = 4
                        elif split_text[6] in ['', "Time"]:
                            pts_index = 5
                        else:
                            pts_index = 6
                        pts = split_text[pts_index]
                    except SystemError:
                        print(f"File {file_name} has points box in different area.")
                        pts = 0
                    data["Points"].append(pts)

                    print(f"Date: {date}. Username: {username}. KC: {kc}. Points: {pts}")

        df = pd.DataFrame(data=data)
        df.to_csv(path_or_buf=f"{os.environ['OUTPUT_PATH']}output.csv", index=False)

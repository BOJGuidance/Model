from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from tqdm import tqdm
from django.http import JsonResponse

import re
import csv
import requests
import pandas as pd
import base64

from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties


def base64image(path):
    image_path = path

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    return JsonResponse({'image': encoded_image})


def analysisModel(handle):
    imageSave = 'data/images/'+handle+'.png'

    User_Page_Link = 'https://www.acmicpc.net/user/'
    User_name = handle
    User_Solved_Problem = []

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    service = Service(executable_path='/usr/local/bin/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver.ChromeOptions())

    driver.get(User_Page_Link + User_name)
    for i in range(1, 30000):
        try:
            User_Solved_Problem.append(driver.find_element(By.XPATH,
                                                        '/html/body/div[2]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]/div/a[' + str(
                                                            i) + ']').text)
        except NoSuchElementException:
            break


    # Load the algorithm dataset
    algorithm_df = pd.read_csv('data/algorithm.csv')

    # Ensure problem IDs are strings to match with scraped data
    algorithm_df['problem_id'] = algorithm_df['problem_id'].astype(str)

    # Filter the dataframe to get only the rows corresponding to the solved problems
    solved_df = algorithm_df[algorithm_df['problem_id'].isin(User_Solved_Problem)]


    # Initialize a Counter to keep track of category frequencies
    category_counts = Counter()

    # Iterate through each row in the solved problems dataframe
    for categories in solved_df['name']:
        # Assuming categories are stored as a comma-separated string
        categories_list = categories.split(',')
        # Remove any leading/trailing whitespace and count each category
        category_counts.update([category.strip() for category in categories_list])

    # Display the frequency of each category

    # Set the font properties for Korean support
    font_path = r'data/NANUMBARUNGOTHIC.TTF'  # Adjust the path to your Korean font
    korean_font = FontProperties(fname=font_path, size=8)

    # Create labels and values
    labels = list(category_counts.keys())
    values = list(category_counts.values())

    # Create the bar chart
    plt.figure(figsize=(14, 8))  # Increase figure size for better visibility
    plt.bar(labels, values, color='royalblue')

    # Add title and labels with Korean font properties
    plt.title('유형별 풀이수', fontproperties=korean_font, size=16)
    plt.xlabel('유형명', fontproperties=korean_font, size=14)
    plt.ylabel('풀이 횟수', fontproperties=korean_font, size=14)

    # Rotate x-labels for better visibility
    plt.xticks(rotation=90, fontproperties=korean_font)

    # Show the plot
    plt.tight_layout()  # Adjust layout to fit labels

    plt.savefig(imageSave, dpi=300, bbox_inches='tight')

    return base64image(imageSave)

    
        
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

import re
import csv
import requests
import pandas as pd

from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.font_manager import FontProperties


def base64image():
    image_path = "/Users/hyun/Desktop/test.png"

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    return JsonResponse({'image': encoded_image})


def solvedProblemsList(userName):
    # Load the user dataset
    user_df = pd.read_csv('User_Dataset.csv')

    # Find the row with the specified userName and extract their solved problems
    # Ensure the 'User_name' and 'Solved_Problems' column names match those in your CSV
    try:
        solved_problems_str = user_df[user_df['User_name'] == userName]['Solved_Problem'].iloc[0]
        # Use regular expression to find all numbers and remove any unwanted characters
        solved_problems_list = re.findall(r'\d+', solved_problems_str)
        # Convert list elements from strings to integers
        solved_problems_list = [int(problem) for problem in solved_problems_list]
    except IndexError:
        solved_problems_list = []  # In case no entry is found for the user
        print(f"No entry found for user {userName}")
    return solved_problems_list


def categoryCounts():
    # Load the algorithm dataset
    algorithm_df = pd.read_csv('algorithm.csv')

    # Filter the dataframe to get only the rows corresponding to the solved problems
    solved_df = algorithm_df[algorithm_df['problem_id'].isin(solvedProblemsList(userName))]

    # Initialize a Counter to keep track of category frequencies
    category_counts = Counter()

    # Iterate through each row in the solved problems dataframe
    for categories in solved_df['name']:
        # Assuming categories are stored as a comma-separated string
        categories_list = categories.split(',')
        # Remove any leading/trailing whitespace and count each category
        category_counts.update([category.strip() for category in categories_list])
    return category_counts


def tagCounting():
    file_path = 'Problem_Dataset.csv'

    # Read the CSV file
    df = pd.read_csv(file_path)

    # Print column names to verify
    print("Column names:", df.columns)

    # Extract the column values into a list (replace 'Problem_number' with the correct column name)
    correct_column_name = 'Problem_Number'  # Replace this with the verified column name from the print output
    problem_numbers = df[correct_column_name].tolist()

    return problem_numbers


def imageGeneration(userName):


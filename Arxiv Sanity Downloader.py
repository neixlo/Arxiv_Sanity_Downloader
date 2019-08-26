#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
import os
import time
import requests
from pathlib import Path

# Save current project WD as path
Path_Main = os.getcwd()

# Webdriver Path (Chromium)
chrome_driver_path = CHROMEDRIVER_LOCATION

# Arxiv Login and Password
Login = YOURLOGIN
Password = YOURPASSWORD

payload = {"username" : Login, "password" : Password}

# All folders to be checked for papers
folders = ["Read", "Unread"]

# The folder all new papers will be downloaded into
download_folder = "Unread"

# Makes sure the download folder is in the list
assert(download_folder in folders), "Download Folder needs to be in the list of folders"

# Get a list of all files in the folder
all_files = os.listdir()

# Makes sure the Folders are in there. Creates them if not.
for folder in folders:
    if not(folder in all_files):
        os.mkdir(folder)

# Start Webdriver and navigate to arxiv sanity
driver = webdriver.Chrome(chrome_driver_path)
driver.get("http://arxiv-sanity.com")
# Wait 5 seconds
time.sleep(5)

# Locate the input login stuff
username_field = driver.find_element_by_name("username")
password_field = driver.find_element_by_name("password")
login_button = driver.find_element_by_xpath("/html/body/div[2]/div[1]/form/input[3]")

# Login
username_field.clear()
password_field.clear()
username_field.send_keys(Login)
password_field.send_keys(Password)
login_button.submit()

#Navigate to Library and scroll all the way down
# navigate
driver.get("http://arxiv-sanity.com/library")
# Wait a couple of seconds
time.sleep(5)

# Find how many papers are in the library
msg = driver.find_element_by_class_name("msg").text
num_papers = int(msg[0:msg.find(" ")])
print("Total Papers in your library : {}".format(num_papers))

# We have to scroll down until an element with xpath selector of:
# /html/body/div[7]/div[1]/div[num_papers + 2] exists and has" content "Results Complete"
done_scrolling = False
xpath_base = "/html/body/div[7]/div[1]/div["

xpath = "/html/body/div[7]/div[1]/div[{}]".format(num_papers+2)

while not done_scrolling:
    try:
        final_message = driver.find_element_by_xpath(xpath)
        done_scrolling = True
    except:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.1)

print("Done Scrolling!")

# Populate the list of titles of articles found by looking for all things of class apaper (THANK YOU ANDREJ)
papers = driver.find_elements_by_class_name("apaper")

paper_titles = []
paper_links = []

for paper in papers:
    # Find the Title
    title_end = paper.text.find("\n")
    # We will use the paper titles to name the files
    # Files on a macbook can't have names past 255 characters. For safety limit is 200
    if title_end > 200:
        title_end = 200
        print("Paper title too long. Cutting off after 200 chars")
    # Get the title
    paper_title = paper.text[0:title_end]
    # Print the title
    print("Paper found: " + paper_title)
    # Get the arxiv ID
    paper_arxiv_id = paper.get_attribute("id")
    # Add to list
    paper_titles.append(paper_title)
    paper_links.append(paper_arxiv_id)

# Check that all papers were found
assert(len(paper_titles) == num_papers), "Something went wrong while looking for papers, sorry"
print(50 * "*")
print("All Papers found, quitting driver")
print(50 * "*")
driver.quit()

# Compile all the titles in the specified folders
local_paper_titles = []

for folder in folders:
    folder_papers = os.listdir(folder)
    for paper in folder_papers:
        local_paper_titles.append(paper[0:paper.find(".pdf")])

# Print all local paper titles
print("Local Papers found:")
print(local_paper_titles)

# Find paper Differences:

already_found_papers = list(set(paper_titles).intersection(set(local_paper_titles)))
print("Papers to be downloaded: (total of {})".format(num_papers - len(already_found_papers)))

indices = []
# Remove the papers that are already local from the download list:
for found_paper in already_found_papers:
    indices.append(paper_titles.index(found_paper))

# Sort indices in reverse to make removing from list easy
indices.sort(reverse = True)

# Remove Titles and arxiv links
for index in indices:
    print("Stopping {} paper from downloading".format(paper_titles[index]))
    del paper_titles[index]
    del paper_links[index]

# Downloading the remaining papers:

# Change the WD to be in the download folder
os.chdir(download_folder)
#print(os.listdir())

for i in range(len(paper_titles)):
    # Filename will be paper title.pdf
    filename = Path(paper_titles[i] + ".pdf")
    #print(filename)
    url = "https://arxiv.org/pdf/" + paper_links[i] + ".pdf"
    #print(url)
    response = requests.get(url)
    # Download
    filename.write_bytes(response.content)

#coding=utf-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import argparse
import json
import re

# outputs the price substring
def extract_price(string):
    match = re.search("(\d+)(\.?)(\d*)", string)
    if match:
        substring = match.group(0)
        return substring
    else:
        return None

# outputs the size substring (convert to GB)
def extract_size(string):
    if 'unlimited' in string.lower():
        return 'unlimited'
    pattern = re.compile(r"(\d+)\s?(GB|TB)")
    match = pattern.search(string)

    if match:
        size = float(match.group(1))
        if 'TB' in match.group(0):
            size *= 1024
    else:
        return None

    return size


# Open the file
with open('info-cloud.json', 'r') as f:
    # Read the contents of the file
    contents = f.read()

# Split the contents of the file into individual JSON objects
objects = contents.split('\n')

def crawl():
    for obj in objects:
        # Load the JSON object
        data = json.loads(obj)

        if data['table_check'] == 1:
            continue
        
        resp = requests.get(data['urls'])
        soap = BeautifulSoup(resp.content, 'html.parser')

        if data['pakage']['filter'] == 1:
            soap = soap.find_all(data['pakage']['filter_tag'], {'id': data['pakage']['filter_id'], 'class': data['pakage']['filter_class']})
            soap = BeautifulSoup(str(soap), 'html.parser')

        if len(data['pakage']['all_group_tag_class']) == 1:
            groups = soap.find_all(data['pakage']['all_group_tag'], class_ = data['pakage']['all_group_tag_class'][0])
        else:
            groups = []
            count_class = len(data['pakage']['all_group_tag_class'])
            for i in range(count_class):
                temp = soap.find_all(data['pakage']['all_group_tag'], class_ = data['pakage']['all_group_tag_class'][i])
                groups.append(temp[0])

        output = ['', '', 0, [], []]
        number_of_options = len(groups)
        output[0] = data['providers']
        output[1] = data['urls']
        output[2] = number_of_options

        for group in groups:
            soap = BeautifulSoup(str(group), 'html.parser')
            detail_line = soap.text.splitlines()
            for keyword in keywords:
                for detail in detail_line:
                    check_keyword = False
                    for i in range(2, len(keyword)):
                        current_keyword = keyword[i]
                        if current_keyword in detail.upper():
                            check_keyword = True
                    if check_keyword == True:
                        output[keyword[1]].append(detail)
        
        output[3] = [extract_price(price) for price in output[3]]
        output[4] = [extract_size(size) for size in output[4]]
        print(output)

def crawl_table():
    for obj in objects:
        # Load the JSON object
        data = json.loads(obj)

        if data['table_check'] != 1:
            continue
        
        browser = webdriver.Firefox()
        browser.get(data['urls'])
        html = browser.page_source
        browser.quit()
        soap = BeautifulSoup(html, 'html.parser')

        tables = soap.find(data['table']['full_tag'], class_ = data['table']['full_class'])
        table = re.search(r'<table(.*?)</table>', str(tables)).group(0)
        table = BeautifulSoup(table, 'html.parser')
        table = table.find('table')
        cols_name = table.find('thead').find_all('tr')
        rows = table.find('tbody').find_all('tr')

        output = ['', '', 0, [], []]
        number_of_options = len(rows)
        output[0] = data['providers']
        output[1] = data['urls']
        output[2] = number_of_options
        
        cols_name = cols_name[0].find_all('th')
        cols_name = [th.text for th in cols_name]
        delete_index = []
        check_col_name_list = ['STORAGE', 'PRICE']
        for check_col in cols_name:
            check = False
            for i in check_col_name_list:
                if i in check_col.upper():
                    check = True
            if check == False:
                delete_index.append(cols_name.index(check_col))

        for row in rows:
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            for col in cols:
                if cols.index(col) in delete_index:
                    continue
                for keyword in keywords_table:
                    check_keyword = False
                    for i in range(2, len(keyword)):
                        current_keyword = keyword[i]
                        if current_keyword in col.upper():
                            check_keyword = True
                    if check_keyword == True:
                        output[keyword[1]].append(col)

        output[3] = [extract_price(price) for price in output[3]]
        output[4] = [extract_size(size) for size in output[4]]
        print(output)
        

        

keywords = [['price', 3, '$', 'USD'],
            ['storage', 4, 'STORAGE', 'SSD', 'SPACE']]

keywords_table = [['price', 3, '$', 'USD'],
            ['storage', 4, 'GB', 'TB']]

crawl_table()
crawl()

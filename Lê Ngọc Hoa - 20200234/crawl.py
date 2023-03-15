'''
@author: Lê Ngọc Hoa - 20200234 - IT2-02 K65
@version: 1.0
'''

#coding=utf-8
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json
import re
import pandas as pd
import hashlib


# host
FILE_HOST = './input/host.json'
# drive
FILE_DRIVE = './input/drive.json'
# VM
FILE_VM = './input/vm.json'

KEYWORDS = [['price', 4, '$', 'USD', '-MONTHLY', '-NORMALLY', '-EMAIL', '-PROMOTIONAL', '-BUY', '-NEW', '-TODAY', '-FREE'],
            ['storage', 5, 'STORAGE', 'SSD', 'SPACE', '-PLAN', '-BUSINESS', '-REDUCE', '-INCREASED'],
            ['saving', 6, 'SAVE', 'SAVING'],
            ['certificate', 7, 'CERTIFICATE'],
            ['support', 8, 'SUPPORT', '-PLANS'],
            ['website', 9, 'WEBSITE', '-YOU', '-CUSTOMER', '-BLUEHOST', '-FREE', '-BUILDER', '-EMAIL', '-LEVEL', '-STAGING', '-GREAT'],
            ['bandwidth', 10, 'BANDWIDTH'],
            ['backup', 11, 'BACKUP', '-PEACE', '-HOWEVER'],
            ['database', 12, 'DATABASE'],
            ['ram', 13, 'RAM', 'MEMORY'],
            ['email', 14, 'MAIL'],
            ['cores', 15, 'CORE'],
            ['gpu-type', 16, 'M4000', 'P4000', 'P5000', 'P6000', 'V100', 'RTX4000', 'RTX5000', 'A4000', 'A5000', 'A6000', 'A100'],
            ['gpu-size', 17, 'GPU']]
excel_total, excel_drive, excel_host, excel_vm = [], [], [], []


# GPU type
def extract_gpu_type(string):
    list_gpu = ['M4000', 'P4000', 'P5000', 'P6000', 'V100', 'RTX4000', 'RTX5000', 'A4000', 'A5000', 'A6000', 'A100']
    for i in list_gpu:
        if i in string.upper():
            return i

# outputs the number of website, database, email, cores
def extract_number(string):
    if 'unlimited' in string.lower():
        return 'unlimited'
    match = re.search("(\d+)", string)
    if match:
        substring = match.group(0)
        return substring
    else:
        return 'NULL'

# outputs number of saving (in %)
def extract_saving(string):
    match = re.search("(\d+)%", string)
    if match:
        substring = match.group(0)
        return substring[:-1]
    else:
        return 'NULL'

# outputs the price substring
def extract_price(string):
    if '.' in string:
        match = re.search("(\d+)(\.)(\d*)", string)
        if match:
            substring = match.group(0)
            return substring
        else:
            return 'NULL'
    else:
        match = re.search("(\d+)(\.?)(\d*)", string)
        if match:
            substring = match.group(0)
            return substring
        else:
            return 'NULL'

# outputs the size substring (convert to GB) - storge, bandwidth, ram
def extract_size(string):
    if 'unlimited' in string.lower():
        return 'unlimited'
    pattern = re.compile(r"(\d+)(\s?)(GB|TB)")
    match = pattern.search(string)
    if match:
        size = float(match.group(1))
        if 'TB' in match.group(0):
            size *= 1024
    else:
        return 'NULL'
    return size

# remove spaces in start and end of text
def remove_spaces(text):
    return text.strip()

# open file json
def input_file_json():
    with open(FILE_HOST, 'r') as f:
        contents_host = f.read()
    with open(FILE_DRIVE, 'r') as f:
        contents_drive = f.read()
    with open(FILE_VM, 'r') as f:
        contents_vm = f.read()
    global objects_host, objects_drive, objects_vm
    # Split the contents of the file into individual JSON objects
    objects_host = contents_host.split('\n')
    objects_drive = contents_drive.split('\n')
    objects_vm = contents_vm.split('\n')

# crawl
def crawl(objects, type):
    for obj in objects:
        # Load the JSON object
        data = json.loads(obj)

        if data['get_app_url'] == '':
            AppPoint = 0
        else:
            browser = webdriver.Firefox()
            browser.get(data['get_app_url'])
            html = browser.page_source
            browser.quit()
            soap = BeautifulSoup(html, 'html.parser')
            AppPoint_soap = soap.find('p', class_ = 'Typography Typography_root__Zc3Hi Typography_display-sm___JJRc RatingDisplay_number__m3Cwk')
            AppPoint = AppPoint_soap.text

        browser = webdriver.Firefox()
        browser.get(data['urls'])
        html = browser.page_source
        browser.quit()
        soap = BeautifulSoup(html, 'html.parser')

        soap_hash = hashlib.md5(str(soap).encode()).hexdigest()
        check_update(soap_hash, data['providers'])

        if len(data['block_tag_class']) == 1:
            groups = soap.find_all(data['block_tag'], class_ = data['block_tag_class'][0])
        else:
            groups = []
            count_class = len(data['block_tag_class'])
            for i in range(count_class):
                temp = soap.find(data['block_tag'], class_ = data['block_tag_class'][i])
                groups.append(temp)

        output = ['', '', 0, 0, [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        number_of_options = len(groups)
        output[0] = data['providers']
        output[1] = data['urls']
        output[2] = number_of_options
        output[3] = AppPoint

        for group in groups:
            soap = BeautifulSoup(str(group), 'html.parser')
            detail_line = soap.text.splitlines()
            for keyword in KEYWORDS:
                append_text = {"this is a set"}
                append_text.clear()
                for detail in detail_line:
                    for i in range(2, len(keyword)):
                        current_keyword = keyword[i]
                        if current_keyword[0] != '-':
                            if current_keyword in detail.upper():
                                append_text.add(detail)
                        if current_keyword[0] == '-':
                            current_keyword = current_keyword[1:]
                            if current_keyword in detail.upper() and detail in append_text:
                                append_text.remove(detail)
                if len(append_text) >= 1:
                    ele = append_text.pop()
                    output[keyword[1]].append(ele)
                else:
                    output[keyword[1]].append('NULL')
        # print(output)
        output[4] = [extract_price(price) for price in output[4]]
        output[5] = [extract_size(size) for size in output[5]]
        output[6] = [extract_saving(saving) for saving in output[6]]
        output[7] = [remove_spaces(certificate) for certificate in output[7]]
        output[8] = [remove_spaces(support) for support in output[8]]
        output[9] = [extract_number(website) for website in output[9]]
        output[10] = [extract_size(bandwidth) for bandwidth in output[10]]
        output[11] = [remove_spaces(backup) for backup in output[11]]
        output[12] = [extract_number(database) for database in output[12]]
        output[13] = [extract_size(ram) for ram in output[13]]
        output[14] = [extract_number(mail) for mail in output[14]]
        output[15] = [extract_number(core) for core in output[15]]
        output[16] = [extract_gpu_type(gpu_type) for gpu_type in output[16]]
        output[17] = [extract_size(gpu_size) for gpu_size in output[17]]
        
        # print(output)
        for i in range(output[2]):
            add_excel = []
            add_excel.append(type)
            add_excel.append(output[0]) # provider name
            add_excel.append(output[2]) # number of options
            add_excel.append(output[3]) # get app point
            add_excel.append(output[1]) # url
            for j in range(4, len(output)):
                add_excel.append(output[j][i])
            if type == 'host':
                excel_host.append(add_excel)
            elif type == 'drive':
                excel_drive.append(add_excel)
            elif type == 'vm':
                excel_vm.append(add_excel)

# output to excel
def out_to_excel():
    excel_total = excel_host + excel_drive + excel_vm

    # total.csv
    column_names = ['PType', 'ProviderName', 'NumberOfOption', 'GetAppPoint', 'URL', 'price (/mo)', 'storage (GB)', 'saving (in %)', 'certificate', 'support', 'website', 'bandwidth', 'backup', 'database', 'ram', 'email', 'cores', 'GPU type', 'GPU size']
    data = {col: list(val) for col, val in zip(column_names, zip(*excel_total))}
    df = pd.DataFrame(data)
    df['ProviderID'] = range(1, len(df) + 1)
    df = df.set_index('ProviderID')
    df.to_csv('./output/total.csv')

    # host.csv
    data = {col: list(val) for col, val in zip(column_names, zip(*excel_host))}
    df = pd.DataFrame(data)
    df['ProviderID'] = range(1, len(df) + 1)
    df = df.set_index('ProviderID')
    df.to_csv('./output/host.csv')

    # drive.csv
    data = {col: list(val) for col, val in zip(column_names, zip(*excel_drive))}
    df = pd.DataFrame(data)
    df['ProviderID'] = range(1, len(df) + 1)
    df = df.set_index('ProviderID')
    df.to_csv('./output/drive.csv')

    # vm.csv
    data = {col: list(val) for col, val in zip(column_names, zip(*excel_vm))}
    df = pd.DataFrame(data)
    df['ProviderID'] = range(1, len(df) + 1)
    df = df.set_index('ProviderID')
    df.to_csv('./output/vm.csv')

    # protype.csv
    column_names_protype = ['PType', 'ProviderName', 'NumberOfOption', 'GetAppPoint']
    data_protype = [[sublist[0], sublist[1], sublist[2], sublist[3]] for sublist in excel_total]
    data = {col: list(val) for col, val in zip(column_names_protype, zip(*data_protype))}
    df = pd.DataFrame(data)
    df.to_csv('./output/protype.csv', index = False)

    ####################################################################################

    # InsertHost.csv
    column_names_providerhostoption = ['ProviderName', 'Sduration', 'Price', 'Core', 'Ram', 'Capacity', 'Bandwidth', 'PricePoint', 'CPUPoint', 'RAMPoint', 'BandPoint', 'AveragePoint']
    data_providerhostoption = [[sublist[1], 'NULL', sublist[5], sublist[16], sublist[14], sublist[6], sublist[11], 'NULL', 'NULL', 'NULL', 'NULL', 'NULL'] for sublist in excel_host]
    data = {col: list(val) for col, val in zip(column_names_providerhostoption, zip(*data_providerhostoption))}
    df = pd.DataFrame(data)
    df['ProviderOpID'] = range(1, len(df) + 1)
    df = df.set_index('ProviderOpID')
    df.to_csv('./output/InsertHost.csv')

    # InsertDrive.csv
    column_names_providerdriveoption = ['ProviderName', 'MaxPeople', 'Sduration', 'Price', 'Capacity', 'GbPerPrice', 'PricePoint', 'PeoplePoint', 'AveragePoint']
    data_providerdriveoption = [[sublist[1], 'NULL', 'NULL', sublist[5], sublist[6], 'NULL', 'NULL', 'NULL', 'NULL'] for sublist in excel_drive]
    data = {col: list(val) for col, val in zip(column_names_providerdriveoption, zip(*data_providerdriveoption))}
    df = pd.DataFrame(data)
    df['ProviderOpID'] = range(1, len(df) + 1)
    df = df.set_index('ProviderOpID')
    df.to_csv('./output/InsertDrive.csv')

    # InsertVM.csv
    column_names_providervmoption = ['ProviderName', 'GPU type', 'GPU size', 'Price', 'Capacity', 'GbPerPrice', 'PricePoint', 'PeoplePoint', 'AveragePoint']
    data_providervmoption = [[sublist[1], sublist[17], sublist[18], sublist[5], sublist[6], 'NULL', 'NULL', 'NULL', 'NULL'] for sublist in excel_vm]
    data = {col: list(val) for col, val in zip(column_names_providervmoption, zip(*data_providervmoption))}
    df = pd.DataFrame(data)
    df['ProviderOpID'] = range(1, len(df) + 1)
    df = df.set_index('ProviderOpID')
    df.to_csv('./output/InsertVM.csv')

def check_update(hash_check, provider):
    check = False
    f = open('./input/checkupdate.txt', 'r')
    lines = []
    with open('./input/checkupdate.txt', 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            lines.append(line)

    for line in lines:
        index = lines.index(line)
        values = line.split(':')
        if values[0] == provider and values[1] != hash_check:
            check = True
            values[1] = hash_check
            lines[index] = values[0] + ':' + values[1]
    if check == True:
        with open('./input/checkupdate.txt', 'w') as f:
            for line in lines:
                f.write(str(line) + "\n")

def main():
    input_file_json()
    crawl(objects_host, 'host')
    crawl(objects_drive, 'drive')
    crawl(objects_vm, 'vm')
    out_to_excel()

main()
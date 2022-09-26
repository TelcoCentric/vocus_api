import json
import requests
from bs4 import BeautifulSoup

def login():
    data = {
        'staffname': 'portal@domain.com.au',
        'staffpass': ''
    }

    return s.post('https://members.wcg.net.au/news.php', data=data)

def getTransactionLog():
    params = {
        'page': 'all',
        'id': '',
        'supply_status': '',
        'service_status': '',
        'lastupdated': '',
        'linesize': '',
        'ourplan': '',
        'username': '',
        'servicenumber': '',
        'name': '',
        'usertypedata': '',
        'filter': 'filter'
    }

    return s.get('https://members.wcg.net.au/nbnuserlist.php', params=params)

s = requests.Session()

l = login()
gt = getTransactionLog()

soup = BeautifulSoup(gt.text, 'html.parser')
table_data = [[cell.text for cell in row("td")] for row in soup("tr")]

header_row = list(filter(lambda x: "ID\n\n\n" in x, table_data))
data_rows = list(filter(lambda x: "wba.telcocentric.com.au" in x, table_data))
header = list()

for h in header_row[0]:
    header.append(h.replace("\n", ""))
print(header)

services_list = list()

for service in data_rows:
    services_list.append(dict(zip(header, service)))

for service in services_list:
    id = service["ID"]
    username = service["Username"]
    print(f"{id} = {username}")

quit()
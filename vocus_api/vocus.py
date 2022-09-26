from . import session

import json
from bs4 import BeautifulSoup

BASE_URL = "https://members.wcg.net.au"

class Vocus(object):

    def __init__(self):
        pass

    def Login(username, password):
        data = {
            'staffname': username,
            'staffpass': password
        }

        session.post(f'{BASE_URL}/news.php', data=data)

    class Service(object):
        def __init__(self, id):
            self.id = id

        def basic_info(self):
            params = {
                'page': 'all',
                'id': self.id,
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

            response = session.get(f'{BASE_URL}/nbnuserlist.php', params=params)
            soup = BeautifulSoup(response.text, 'html.parser')
            table_data = [[cell.text for cell in row("td")] for row in soup("tr")]

            header_row = list(filter(lambda x: "ID\n\n\n" in x, table_data))
            data_rows = list(filter(lambda x: "wba.telcocentric.com.au" in x, table_data))
            header = list()

            assert 0 

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

            return {'ID': self.id}

        def detailed_info(self):
            pass



 
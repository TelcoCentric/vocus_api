import re
import requests
from bs4 import BeautifulSoup
from typing import List

class Portal(object):
    _session = None
    username: str
    password: str
    base_url: str

    @property
    def session(self):
        if self._session:
            return self._session

        data = {
            'staffname': self.username,
            'staffpass': self.password
        }

        session = requests.Session()
        session.post(f'{self.base_url}/news.php', data=data)

        self._session = session
        return session

    def __init__(self, base_url, username, password):
        self.username = username
        self.password = password
        self.base_url = base_url

    def get_nbn_user_list_as_html(self, **kwargs):
        params = {
            'page': 'all',
            'id' : '',
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

        for arg in kwargs:
            if kwargs[arg] is not None:
                params[arg] = kwargs[arg]

        breakpoint()
        v = self.session.get(f'{self.base_url}/nbnuserlist.php', params=params)
        return v

    def get_service(self, id):
        response = self.get_nbn_user_list_as_html(id=id)
        soup = BeautifulSoup(response.text, 'html.parser')

        string_details = "Current NBN Details of"
        string_nbn_allowances = "NBN Allowances"
        string_service_history = "Service History"

        # tables = soup.find_all('table')
        table_details = soup.find('td', string=re.compile(string_details)).find_parent('table')
        
        service = Service()
        service_mapping = {
            "current_service" : "Current Status",
            "id" : "ID",
            "username" : "Username",
            "name" : "Name",
            "address" : "Address",
            "password" : "Password",
            "carrier_id" : "Carrier ID",
            "request" : "Request",
            "line_size" : "Line Size",
            "plan_type" : "Plan Type",
            "mapping" : "Mapping",
            "product_type" : "Product Type",
            "ip_address" : "IP Address",
            "service_class" : "Service Class",
            "date_submitted" : "Date Submitted",
            "nbn_service_level" : "NBN Service Level",
        }

        for mapping in service_mapping:
            try:
                status_text = table_details.find('td', string=re.compile(service_mapping[mapping])).find_next_sibling('td').get_text()
                setattr(service, mapping, status_text)
            except:
                setattr(service, mapping, "")
                
        table_nbn_allowances = soup.find('td', string=re.compile(string_nbn_allowances)).find_parent('table')
        table_service_history = soup.find('td', string=re.compile(string_service_history)).find_parent('table')

        return service




class PlannedOutageNotification:
    nbn_cr_id: str
    status: str
    description: str
    start_date: str
    end_date: str
    duration_hours: str

    def __init__(self, **kwargs) -> None:
        for arg in kwargs:
            setattr(self, kwargs, kwargs[arg])

class NBNSpeedInformation:
    nbn_record_date: str
    mean_speed: str
    current_assured_speed: str

    def __init__(self, **kwargs) -> None:
        for arg in kwargs:
            setattr(self, kwargs, kwargs[arg])

class ServiceHistory:
    id: str
    request: str
    status: str
    line_size: str
    plan_type: str
    date_updated: str

    def __init__(self, **kwargs) -> None:
        for arg in kwargs:
            setattr(self, kwargs, kwargs[arg])

class NBNAllowance:
    allowance_id: str
    username: str
    reset_date: str
    quota: str
    consummed: str
    balance: str
    reset_amount: str

    def __init__(self, **kwargs) -> None:
        for arg in kwargs:
            setattr(self, kwargs, kwargs[arg])

class Service:
    current_status: str
    id: str
    username: str
    name: str
    address: str
    password: str
    carrier_id: str
    request: str
    line_size: str
    plan_type: str
    mapping: str
    product_type: str
    ip_address: str
    service_class: str
    date_submitted: str
    nbn_service_level: str
    nbn_speed_information: List[NBNSpeedInformation]
    planned_outage_notification: List[PlannedOutageNotification]
    nbn_allowances: List[NBNAllowance]
    service_history: List[ServiceHistory]
    service_number: str
    nbn_type: str

    def __init__(self, **kwargs) -> None:
        for arg in kwargs:
            setattr(self, kwargs, kwargs[arg])


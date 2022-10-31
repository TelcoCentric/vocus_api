import re
import os
import string
import requests
from bs4 import BeautifulSoup
from typing import List

def camel_case_convert (camel_input):
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', camel_input.strip())
    word = '_'.join(map(str.lower, words))
    if word in ('class', 'def'):
        return word + "_"
    return word

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

    def __init__(self, base_url=None, username=None, password=None):

        if base_url is None: base_url = os.environ.get('VOCUS_BASE_URL', None)
        if username is None: username = os.environ.get('VOCUS_USERNAME', None)
        if password is None: password = os.environ.get('VOCUS_PASSWORD', None)

        self.username = username
        self.password = password
        self.base_url = base_url

    def get_nbn_availability_as_html(self, **kwargs):
        data = {
            'LotNumber': '',
            'Unit1stNumber': '',
            'Unit1stSuffix': '',
            'Unit1stType': '',
            'FloorNumber': '',
            'FloorSuffix': '',
            'Street1stNumber': '',
            'Street1stNumberSuffix': '',
            'StreetName': '',
            'StreetType': 'ST', # defaults to ST in form
            'city': '',
            'state': 'NSW', # defaults to NSW in form
            'postcode': '',
            'locationid': '',
            'fnn_carrier_id': '',
            'Submit': 'Submit' # defaults to Submit in form
        }

        for arg in kwargs:
            if kwargs[arg] is not None:
                data[arg] = kwargs[arg]

        return self.session.post(f'{self.base_url}/nbnavailable.php', data=data)

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

        return self.session.get(f'{self.base_url}/nbnuserlist.php', params=params)

    def get_services(self):
        services = list()

        response = self.get_nbn_user_list_as_html()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        string_nbn_transaction_list = "NBN  Transaction List"
        table = soup.find('td', string=re.compile(string_nbn_transaction_list)).find_parent('table')

        title_row = table.find_next('tr') # eg: Check Availability, Help, ... Logout
        header_row = title_row.find_next('tr') # eg: ID, Status, Request, Date Updated ... Name, Domain
        search_row = header_row.find_next('tr') 

        headers = [camel_case_convert(x.text.strip()) for x in header_row.find_all('td')]

        data_rows = search_row.find_all_next('tr')
        footer_row = data_rows.pop(-1) # eg: Check Availability, Help, ... Logout
        page_indicator_row = data_rows.pop(-1) # page indicator eg: Rows 1 to 128 of 128

        for row in data_rows:
            service = Service()
            details = [x.text.strip() for x in row.find_all('td')]

            for x in range(len(details)):
                setattr(service, headers[x], details[x])
            
            # Carrier ID seems to be Location ID with two additional digits on the end.
            # This is a bit of an assumption, but so far, so good.
            # get_service() will fill out location_id from an actual input on vocus page.
            service.location_id = "LOC" + service.carrier_id[:-2]

            services.append(service)

        return services

    def get_service(self, id):
        service = Service()

        response = self.get_nbn_user_list_as_html(id=id)
        soup = BeautifulSoup(response.text, 'html.parser')

        string_details = "Current NBN Details of"
        string_nbn_allowances = "NBN Allowances"
        string_service_history = "Service History"
        string_speed_information = "NBN Speed Information"
        string_outage_notification = "Planned Outage Notification"

        table_details = soup.find('td', string=re.compile(string_details)).find_parent('table')
        Portal.obj_map_mapping_from_table_by_next_td(service, table_details, Service.mapping)

        #TODO find/test multiple nbn_speed_information
        nbn_speed_information = NBNSpeedInformation()
        td_nbn_speed_information = soup.find('td', string=re.compile(string_speed_information))
        if td_nbn_speed_information is not None:
            table_nbn_speed_information = td_nbn_speed_information.find('table')
            Portal.obj_map_mapping_from_table_by_next_td(nbn_speed_information, table_nbn_speed_information, NBNSpeedInformation.mapping)
            service.nbn_speed_information.append(nbn_speed_information)

        # #TODO find/test multiple planned_outage_notification
        # planned_outage_notification = NBNOutageNotification()
        # table_planned_outage_notification = soup.find('td', string=re.compile(string_outage_notification)).find('table')
        # Portal.obj_map_mapping_from_table_by_next_td(planned_outage_notification, table_planned_outage_notification, PlannedOutageNotification.mapping)
        # service.planned_outage_notification.append(planned_outage_notification)

        #TODO
        # table_nbn_allowances = soup.find('td', string=re.compile(string_nbn_allowances)).find_parent('table')
        
        #TODO
        # table_service_history = soup.find('td', string=re.compile(string_service_history)).find_parent('table')

        b = soup.find("input", {"name":"carrier_id"})
        if b is not None:
            service.location_id = "LOC" + b.get('value').strip()

        a = soup.find("input", {"name":"nbn_type"})
        if a is not None:
            service.nbn_type = a.get('value').strip()

        return service

    def get_availability(self, location_id):
        availability = Availability()

        response = self.get_nbn_availability_as_html(locationid=location_id)
        soup = BeautifulSoup(response.text, 'html.parser')

        string_nbn_availability = 'NBN Availability'
        table_nbn_availability = soup.find('td', string=re.compile(string_nbn_availability)).find_parent('table').find_next('table').find_next('table')
        Portal.obj_map_mapping_from_table_by_next_td(availability, table_nbn_availability, Availability.mapping)

        return availability

    def obj_map_mapping_from_table_by_next_td(service, table, service_mapping):
        for mapping in service_mapping:
            try:
                text = table.find('td', string=re.compile(service_mapping[mapping])).find_next_sibling('td').get_text().strip()
                setattr(service, mapping, text)
            except:
                setattr(service, mapping, "")
        
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
    
    mapping = {
        "nbn_cr_id" : "NBN CR ID",
        "status" : "Status",
        "description" : "Description",
        "start_date" : "Start Date",
        "end_date" : "End Date",
        "duration_hours" : "Duration (Hours)"
    } 

class NBNSpeedInformation:
    nbn_record_date: str
    mean_speed: str
    current_assured_speed: str

    def __init__(self, **kwargs) -> None:
        for arg in kwargs:
            setattr(self, kwargs, kwargs[arg])
    
    mapping = {
        "nbn_record_date" : "NBN Record Date",
        "mean_speed" : "Mean Speed",
        "current_assured_speed" : "Current Assured Speed"
    }  

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
    current_service: str
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
    #nbn_allowances: List[NBNAllowance]
    #service_history: List[ServiceHistory]
    location_id: str
    nbn_type: str

    def __init__(self, **kwargs) -> None:
        nbn_speed_information = list()
        planned_outage_notification = list()
        #nbn_allowances = list()
        #service_history = list()

        for arg in kwargs:
            setattr(self, kwargs, kwargs[arg])   

    mapping = {
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

class CopperPair:
    cpi_id: str
    pots_match: str
    status: str
    class_: str
    nbn_service_status: str
    max_download_speed: str
    max_upload_speed: str
    tc2_speed: str
    copper_disconnect_date: str

    def __init__(self, **kwargs) -> None:
        for arg in kwargs:
            setattr(self, kwargs, kwargs[arg])

class Availability:
    result: str
    connection_type: str
    service_type: str
    location_id: str
    availability: str
    address: str
    service_class: str
    new_development_charges: str
    additional_information: str
    cvc_id: str
    copper_disconnection_date: str
    csa_id: str
    min_through_put: str
    max_available_speed: str
    fttn_higher_speed_tier: str
    alternate_technology: str
    subsequent_install_charges: string
    copper_pairs: List[CopperPair]

    def __init__(self, **kwargs) -> None:
        copper_pairs = list()
        for arg in kwargs:
            setattr(self, kwargs, kwargs[arg])

    mapping = {
        "result": "Result",
        "connection_type": "Connection Type",
        "service_type": "Service Type",
        "location_id": "Location ID",
        "availability": "Availability",
        "address": "Address",
        "service_class": "Service Class",
        "new_development_charges": "New Development Charges",
        "additional_information": "Additional Information",
        "copper_disconnection_data": "Copper Disconnection Date",
        "csa_id": "CSA ID",
        "min_through_put": "Min ThroughPut",
        "max_available_speed": "Max Available Speed",
        "fttn_higher_speed_tier": "FTTN Higher Speed Tier",
        "alternate_technology": "Alternate Technology",
        "subsequent_install_charge": "Subsequent Install Charge"
    }

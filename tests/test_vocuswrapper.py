import vcr

from pytest import fixture
from vocus_api import vocus, VOCUS_BASE_URL, VOCUS_PASSWORD, VOCUS_USERNAME

portal = vocus.Portal(VOCUS_BASE_URL, VOCUS_USERNAME, VOCUS_PASSWORD)

@fixture
def service_keys():
    # Responsible only for returning the test data
    return [
        'current_status', 
        'id', 
        'username', 
        'name', 
        'address', 
        'password', 
        'carrier_id', 
        'request', 
        'line_size', 
        'plan_type', 
        'mapping', 
        'product_type', 
        'ip_address', 
        'service_class', 
        'date_submitted', 
        'nbn_service_level', 
        'nbn_speed_information', 
        'planned_outage_notification', 
        'nbn_allowances', 
        'service_history', 
        'service_number', 
        'nbn_type'
        ]
    

@vcr.use_cassette('tests/vcr_cassettes/vocus-service-info.yml')
def test_vocus_service_info(service_keys):
    """Test a call to get a Vocus service's info"""

    test_id = '12998156'
    vocus_service = portal.get_service(test_id)

    assert isinstance(vocus_service, vocus.Service)
    assert vocus_service.id == test_id, "The ID should be in the response"
    #assert set(service_keys).issubset(vocus_service.keys()), "All keys should be in the response"
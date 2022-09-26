from vocus_api import vocus
import vocus_api
import vcr

from pytest import fixture
from vocus_api import Vocus

@fixture
def service_keys():
    # Responsible only for returning the test data
    return ['ID', 'Status', 'Request', 'Date Updated', 'Line Size', 'Plan Type', 'Username', 'Carrier ID', 'Name', '']

@vcr.use_cassette('tests/vcr_cassettes/vocus-service-info.yml')
def test_vocus_service_info(service_keys):
    """Test a call to get a Vocus service's info"""

    test_id = '12998156'
    vocus_service = Vocus.Service(test_id)
    response = vocus_service.basic_info()

    assert isinstance(response, dict)
    assert response['ID'] == test_id, "The ID should be in the response"
    assert set(service_keys).issubset(response.keys()), "All keys should be in the response"
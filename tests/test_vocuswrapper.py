import vcr
from pytest import fixture
from dotenv import load_dotenv
from typing import List

load_dotenv()

from src.vocus_api import vocus

@vcr.use_cassette('tests/vcr_cassettes/vocus-service-detailed.yml')
def test_vocus_service_info():
    """Test a call to get a Vocus service's info"""

    test_id = '12784709'
    portal = vocus.Portal()
    vocus_service = portal.get_service(test_id)

    assert isinstance(vocus_service, vocus.Service)
    assert vocus_service.id == test_id, "The ID should be in the response"
    assert vocus_service.username is not None, "There should be a username in the response"
    assert vocus_service.password is not None, "There should be a password in the response"
    assert vocus_service.date_submitted is not None, "There should be a date_submitted in the response"

    assert isinstance(vocus_service.service_history, vocus.ServiceHistory)
    assert isinstance(vocus_service.user_online, vocus.Session)




@vcr.use_cassette('tests/vcr_cassettes/vocus-service-cancelled.yml')
def test_vocus_service_info_cancelled():
    """Test a call to a cancelled Vocus service"""

    test_id = '13015554'
    portal = vocus.Portal()
    vocus_service = portal.get_service(test_id)

    assert isinstance(vocus_service, vocus.Service)
    assert vocus_service.id == test_id, "The ID should be in the response"
    assert vocus_service.current_service == 'provisioned', "The status should be provisioned"
    assert vocus_service.ip_address == '', "There should be no IP associated with rejected."

@vcr.use_cassette('tests/vcr_cassettes/vocus-service-rejected.yml')
def test_vocus_service_info_rejected():
    """Test a call to a rejected Vocus service"""

    test_id = '13015428'
    portal = vocus.Portal()
    vocus_service = portal.get_service(test_id)

    assert isinstance(vocus_service, vocus.Service)
    assert vocus_service.id == test_id, "The ID should be in the response"
    assert vocus_service.current_service == 'rejected', "The status should be rejected"
    assert vocus_service.ip_address == '', "There should be no IP associated with rejected."

@vcr.use_cassette('tests/vcr_cassettes/vocus-service-list.yml')
def test_vocus_service_get_all():
    """Test a call to get list of vocus services"""

    portal = vocus.Portal()
    vocus_services = portal.get_services()

    assert isinstance(vocus_services[0], vocus.Service)

@vcr.use_cassette('tests/vcr_cassettes/vocus-availability-alternate-technology.yml')
def test_vocus_availability_of_alternate_technology():
    """Test a call to get availability of alternate technology nbn services"""

    test_loc_id = 'LOC000147494507'
    portal = vocus.Portal()
    availability = portal.get_availability(test_loc_id)

    assert availability.alternate_technology == "FTTP ( Available 2022-03-22)"

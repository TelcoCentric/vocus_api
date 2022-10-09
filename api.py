import vcr

from vocus_api import vocus, VOCUS_BASE_URL, VOCUS_USERNAME, VOCUS_PASSWORD

portal = vocus.Portal(VOCUS_BASE_URL, VOCUS_USERNAME, VOCUS_PASSWORD)
services = portal.get_services()

for service in services:
    availability = portal.get_availability(location_id=service.location_id)
    print(availability)

    break
import vcr
import csv

from vocus_api import vocus, VOCUS_BASE_URL, VOCUS_USERNAME, VOCUS_PASSWORD

portal = vocus.Portal(VOCUS_BASE_URL, VOCUS_USERNAME, VOCUS_PASSWORD)
services = portal.get_services()
filename = 'availabilities.csv'

availability1 = portal.get_availability(location_id=services[0].location_id)
header_row = list(services[0].__dict__.keys()) + list(availability1.__dict__.keys())

with open(filename, 'w', newline='') as f:

    writer = csv.writer(f)
    writer.writerow(header_row)

    for service in services:
        availability = portal.get_availability(location_id=service.location_id)
        row = list(service.__dict__.values()) + list(availability.__dict__.values())
        print(row)
        writer.writerow(row)


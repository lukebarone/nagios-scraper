import requests
from scraper import NAGIOS_DATA
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth, HTTPDigestAuth


def get_url_response(url, user, password, auth_type):
    """Get the response from a URL.

    Args:
        url (str): Nagios base URL
        user (str): Nagios username
        password (str): Nagios password
        auth_type (str): Nagios auth_type - Basic or Digest

    Returns: Response object
    """

    if auth_type == "Basic":
        return requests.get(url, auth=HTTPBasicAuth(user, password))
    return requests.get(url, auth=HTTPDigestAuth(user, password))


def print_stats(user, url, extracted_information):
    """Print the stats as a table.

    Args:
        user (str): The user of the Nagios Instance
        url (str): The URL of the Nagios Instance
        extracted_information (dict): Dictionary of stats from the instance

    Returns: A table for each instance listing its stats
    """

    template = """{user}@{url}:
                Hosts
    Up\tDown\tUnreachable\tPending\tProblems\tTypes
    {hosts_up}\t{hosts_down}\t{hosts_unreachable}\t\t{hosts_pending}\t{hosts_problems}\t\t{hosts_types}
                Services
    OK\tWarning\tUnknown\tCritical\tProblems\tTypes
    {service_ok}\t{service_warning}\t{service_unknown}\t{service_critical}\t\t{service_problems}\t\t{service_types}"""
    print(template.format(user=user, url=url, **extracted_information))


def main():
    """
    Main entry to the program
    """

    for url, auth_data in NAGIOS_DATA.items():
        user, password, auth_type = auth_data["user"], auth_data["password"], \
            auth_data["auth_type"]
        full_url = "{}/cgi-bin/status.cgi?host=all".format(url)
        response = get_url_response(full_url, user, password, auth_type)
        if response.status_code != 200:
            continue

        html = BeautifulSoup(response.text, "html.parser")
        td_elements = list(html.select('td'))
        hosts_all = td_elements[3].text.split('\n')
        service_all = td_elements[12].text.split('\n')
        extracted_information = {
            'hosts_up': hosts_all[12],
            'hosts_down': hosts_all[13],
            'hosts_unreachable': hosts_all[14],
            'hosts_pending': hosts_all[15],
            'hosts_problems': hosts_all[24],
            'hosts_types': hosts_all[25],
            'service_ok': service_all[13],
            'service_warning': service_all[14],
            'service_unknown': service_all[15],
            'service_critical': service_all[16],
            'service_problems': service_all[26],
            'service_types': service_all[27],
        }
        print_stats(user, url, extracted_information)


if __name__ == '__main__':
    main()

# import RPi.GPIO as GPIO
# from time import sleep

# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)
# while True:
#     GPIO.output(8, GPIO.HIGH)
#     sleep(1)
#     GPIO.output(8, GPIO.LOW)
#     sleep(1)

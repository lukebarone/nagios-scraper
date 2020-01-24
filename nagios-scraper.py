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


def main():
    """
    Main entry to the program
    """
    
    # for nagios_entry in ALL_NAGIOS_INFO:
    for url, auth_data in NAGIOS_DATA.items():
        user, password, auth_type = auth_data["user"], auth_data["password"], \
            auth_data["auth_type"]
        full_url = "{}/cgi-bin/status.cgi?host=all".format(url)
        response = get_url_response(full_url, user, password, auth_type)
        if response.status_code == 200:
            html = BeautifulSoup(response.text, "html.parser")
            for i, items in enumerate(html.select('td')):
                if i == 3:
                    hostsAll = items.text.split('\n')
                    hosts_up = hostsAll[12]
                    hosts_down = hostsAll[13]
                    hosts_unreachable = hostsAll[14]
                    hosts_pending = hostsAll[15]
                    hosts_problems = hostsAll[24]
                    hosts_types = hostsAll[25]
                if i == 12:
                    serviceAll = items.text.split('\n')
                    service_ok = serviceAll[13]
                    service_warning = serviceAll[14]
                    service_unknown = serviceAll[15]
                    service_critical = serviceAll[16]
                    service_problems = serviceAll[26]
                    service_types = serviceAll[27]
                # print(i, items.text) ## To get the index and text
            print_stats(
                user, url, hosts_up, hosts_down, hosts_unreachable,
                hosts_pending, hosts_problems, hosts_types, service_ok,
                service_warning, service_unknown, service_critical,
                service_problems, service_types)

    # print("Request returned:\n\n{}".format(html.text))
    # To get the full request


def print_stats(
        user, url, hosts_up, hosts_down, hosts_unreachable, hosts_pending,
        hosts_problems, hosts_types, service_ok, service_warning,
        service_unknown, service_critical, service_problems, service_types):
    print("""{}@{}:
                Hosts
    Up\tDown\tUnreachable\tPending\tProblems\tTypes
    {}\t{}\t{}\t\t{}\t{}\t\t{}
                Services
    OK\tWarning\tUnknown\tCritical\tProblems\tTypes
    {}\t{}\t{}\t{}\t\t{}\t\t{}""".format(
        user, url, hosts_up, hosts_down, hosts_unreachable, hosts_pending,
        hosts_problems, hosts_types, service_ok, service_warning,
        service_unknown, service_critical, service_problems, service_types))

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

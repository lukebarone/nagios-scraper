import requests
from scraper import NAGIOS_DATA
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from tabulate import tabulate
import sys
import argparse


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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

    template = (
        bcolors.HEADER + '{user}@{url}:\n'
        '        Hosts\n'
        'Up\tDown\tUnreachable\tPending\tProblems\tTypes\n'
        + bcolors.ENDC
        + bcolors.OKGREEN + '{hosts_up}\t'
        + bcolors.FAIL + '{hosts_down}\t'
        + bcolors.WARNING + '{hosts_unreachable}\t\t'
        + bcolors.OKBLUE + '{hosts_pending}\t'
        + bcolors.FAIL + '{hosts_problems}\t\t'
        + bcolors.ENDC + '{hosts_types}\n'
        + bcolors.HEADER + '        Services\n'
        'OK\tWarning\tUnknown\tCritical\tProblems\tTypes\n'
        + bcolors.OKGREEN + '{service_ok}\t'
        + bcolors.WARNING + '{service_warning}\t'
        + bcolors.OKBLUE + '{service_unknown}\t'
        + bcolors.FAIL + '{service_critical}\t\t{service_problems}\t\t'
        + bcolors.ENDC + '{service_types}\n')
    print(template.format(user=user, url=url, **extracted_information))


def print_all_stats(user, url, extracted_information):
    """Print the stats as a table.

    Args:
        user (str): The user of the Nagios Instance
        url (str): The URL of the Nagios Instance
        extracted_information (dict): Dictionary of stats from the instance

    Returns: A table for each instance listing its stats
    """

    header = (
        bcolors.HEADER + 'Hosts:\t\t\t\t\t\tServices:\n'
        + bcolors.OKGREEN + 'Up\t'
        + bcolors.FAIL + 'Dn\t'
        + bcolors.WARNING + 'Un\t'
        + bcolors.OKBLUE + 'Pn\t'
        + bcolors.FAIL + 'Pr\t'
        + bcolors.ENDC + 'Ty\t'
        + bcolors.OKGREEN + 'OK\t'
        + bcolors.WARNING + 'Wrn\t'
        + bcolors.OKBLUE + 'Unk\t'
        + bcolors.FAIL + 'Crt\tPr\t'
        + bcolors.ENDC + 'Ty\t\t'
        + bcolors.HEADER + 'Where\n')
    print(header)
    data_to_print = ""
    for (a, b, c) in zip(user, url, extracted_information):
        data_to_print += (
            bcolors.OKGREEN + '{hosts_up}\t'
            + bcolors.FAIL + '{hosts_down}\t'
            + bcolors.WARNING + '{hosts_unreachable}\t'
            + bcolors.OKBLUE + '{hosts_pending}\t'
            + bcolors.FAIL + '{hosts_problems}\t'
            + bcolors.ENDC + '{hosts_types}\t'
            + bcolors.OKGREEN + '{service_ok}\t'
            + bcolors.WARNING + '{service_warning}\t'
            + bcolors.OKBLUE + '{service_unknown}\t'
            + bcolors.FAIL + '{service_critical}\t{service_problems}\t'
            + bcolors.ENDC + '{service_types}\t'
            + bcolors.HEADER + '{user}@{url}\n').format(user=a, url=b, **c)
    print(data_to_print)


def print_tables(user, url, extracted_information):
    """Print the stats as a table in Wide Format.

    Args:
        user (str): The user of the Nagios Instance
        url (str): The URL of the Nagios Instance
        extracted_information (dict): Dictionary of stats from the instance

    Returns: A table for each instance listing its stats
    """
    headers = [
        bcolors.OKGREEN + 'H Up',
        bcolors.FAIL + 'H Down',
        bcolors.WARNING + 'H Unreach',
        bcolors.OKBLUE + 'H Pend',
        bcolors.FAIL + 'H Problems',
        bcolors.ENDC + 'Types',
        bcolors.OKGREEN + 'S OK',
        bcolors.WARNING + 'S Warning',
        bcolors.OKBLUE + 'S Unknown',
        bcolors.FAIL + 'S Critical', 'S Problems',
        bcolors.ENDC + 'S Types',
        bcolors.HEADER + 'Where']
    data = []
    for (a, b, c) in zip(user, url, extracted_information):
        data.append([
            bcolors.OKGREEN + c["hosts_up"],
            bcolors.FAIL + c["hosts_down"],
            bcolors.WARNING + c["hosts_unreachable"],
            bcolors.OKBLUE + c["hosts_pending"],
            bcolors.FAIL + c["hosts_problems"],
            bcolors.ENDC + c["hosts_types"],
            bcolors.OKGREEN + c["service_ok"],
            bcolors.WARNING + c["service_warning"],
            bcolors.OKBLUE + c["service_unknown"],
            bcolors.FAIL + c["service_critical"], c["service_problems"],
            bcolors.ENDC + c["service_types"],
            bcolors.HEADER + '{user}@{url}'.format(user=a, url=b)])
    print(tabulate(data, headers=headers, tablefmt='simple',
                   numalign='center'))


def get_info(html_to_parse):
    """Get the data parsed from the HTML Response

    Args:
        html_to_parse (HTTPResponse): The response object containing the Nagios
        webpage we are scraping

    Returns: Dictionary of parameters, sorted out
    """

    html = BeautifulSoup(html_to_parse.text, "html.parser")
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
    return extracted_information


def main(argv):
    """
    Main entry to the program
    """

    output_format = ""
    # Parse arguments, if any
    parser = argparse.ArgumentParser(description="Multi-site Nagios Scraper")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-w", "--wide",
                       help="Prints the table of information in wide-screen "
                       + "format",
                       action="store_true")
    group.add_argument("-n", "--narrow",
                       help="Prints the table of information in narrow format",
                       action="store_true")

    args = parser.parse_args()
    if args.wide:
        output_format = "wide"
    elif args.narrow:
        output_format = "narrow"
    else:
        output_format = "normal"
    all_info = []
    all_user = []
    all_url = []
    for url, auth_data in NAGIOS_DATA.items():
        user, password, auth_type = auth_data["user"], auth_data["password"], \
            auth_data["auth_type"]
        full_url = "{}/cgi-bin/status.cgi?host=all".format(url)
        response = get_url_response(full_url, user, password, auth_type)
        if response.status_code != 200:
            continue
        current_info = get_info(response)
        all_info.append(current_info)
        all_user.append(auth_data["user"])
        all_url.append(url)
        if output_format == "normal":
            print_stats(user, url, current_info)
    if output_format == "narrow":
        print_all_stats(all_user, all_url, all_info)
    if output_format == "wide":
        print_tables(all_user, all_url, all_info)


if __name__ == '__main__':
    main(sys.argv[1:])

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

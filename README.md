Nagios Scraper
===

![Python application](https://github.com/lukebarone/nagios-scraper/workflows/Python%20application/badge.svg)

### Purpose:

If you are running multiple Nagios sessions in your browser, you need to constantly check in with them. If authentication is turned on, sometimes you have to re-login to them. This script is built to give ONE console of information from ALL your Nagios sources through the command line.

### Installation:

- Clone this repo into a directory.
- Copy `scraper.py.example` to `scraper.py`
- Edit `scraper.py` to add the parameters to your install:
    - Keep the existing structure. It is pure-Python that gets imported
    - First key is the URL, without the trailing slash (i.e. `'http://192.168.0.5/nagios':`)
    - Each key has 3 required parameters:
        - `user` is the user that can log in to Nagios
        - `password` is their password
        - `auth_type` is either Basic or Digest. If one doesn't work, try the other.
    - You can have as many keys as you want, as long as the three parameters are specified
- Ensure you have `python3` installed (untested with Python2, which is EOL anyways)
- Ensure you have `pip3` installed to install the dependencies:
    - tabulate
    - bs4 (BeautifulSoup)
- Run `python3 -m pip install -r requirements.txt` to auto-install the required libraries
- Run `python3 nagios-scraper.py`

If you mess up the configuration, copy the example file back over the official .conf file, and start again.

### Output:

A table showing your Nagios instances, and the status of the hosts and services. Assuming the config file is updated with correct information, you will see something like this:

```
nagiosadmin@http://192.168.0.5/nagios:
                Hosts
    Up  Down    Unreachable     Pending Problems        Types
    24  0       0               0       0               24
                Services
    OK  Warning Unknown Critical        Problems        Types
    142 0       0       0               0               142
exampleuser@https://www.example.com/nagios:
                Hosts
    Up  Down    Unreachable     Pending Problems        Types
    3   0       0               0       0               3
                Services
    OK  Warning Unknown Critical        Problems        Types
    28  0       0       0               0               28
```

### Target Objectives (features to come)

- Colour coding the results (i.e. green for good, red for bad)
- Error handling
- Web page output
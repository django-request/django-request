import requests


def default_get_country_from_id(ip):
    print('get country from default')
    return requests.get(f"https://ip2c.org/?ip={ip}").text.split(';')[-1]
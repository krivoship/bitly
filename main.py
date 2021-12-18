import requests
import os
import argparse
from dotenv import load_dotenv
load_dotenv()


def shorten_link(token, url, group_guid, domain):
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json',
    }

    data = {
        "long_url": url,
        "domain": domain,
        "group_guid": group_guid,
        }

    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=headers,
        json=data,
        )
    response.raise_for_status()

    return response.json()['id']


def count_clicks(token, link):
    headers = {'Authorization': 'Bearer {}'.format(token)}

    params = (
        ('unit', 'day'),
        ('units', '-1'),
    )

    response = requests.get(
        'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(link),
        headers=headers,
        params=params,
        )
    response.raise_for_status()

    return response.json()['total_clicks']


def is_bitlink(token, url):
    headers = {'Authorization': 'Bearer {}'.format(token)}

    response = requests.get(
        'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(url),
        headers=headers,
        )
    return response.ok


def main():
    bitly_token = os.getenv("BITLY_TOKEN")
    group_guid = os.getenv("GROUP_GUID")
    domain = os.getenv("DOMAIN", "bit.ly")

    parser = argparse.ArgumentParser()
    parser.add_argument("link")
    user_link = parser.parse_args().link
    if is_bitlink(bitly_token, user_link):
        try:
            clicks_count = count_clicks(bitly_token, user_link)
            print('По вашей ссылке прошли: {} раз(а)'.format(clicks_count))
        except requests.exceptions.HTTPError as error:
            print('HTTP статус ответа:', error.response.status_code)
    else:
        try:
            bitlink = shorten_link(bitly_token, user_link, group_guid, domain)
            print('Битлинк', bitlink)
        except requests.exceptions.HTTPError as error:
            print('HTTP статус ответа:', error.response.status_code)

if __name__ == '__main__':
    main()

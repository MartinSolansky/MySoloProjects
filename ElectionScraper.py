#!/usr/bin/python3
# Election scraper
# Utility scrape results for 2017 election to Poslanecka Snemovna
# Result are saved to newly created file
# Should be compatible with all OS, report bugs please to: dixecz@gmail.com
# Created by: Martin Solansky

import csv
import os
import sys

import requests
import bs4

SERVER_URL = 'https://volby.cz/pls/ps2017nss/'


def get_soup(URL):
    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup

def get_tables(soup):
    return soup.find_all('table')

def get_rows(table):
    return table.find_all('tr')

def get_partional_url(row):
    try:
        partional_url = row.find('a').attrs.get('href')
        return partional_url
    except AttributeError:
        '''To protect from empty rows in tables'''
        pass

def get_district_url(district_name: str):
    """
    This function will take name of district and will return full link to the site of all municipalities for later use
    """
    URL = 'https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ'
    main_page_soup = get_soup(URL)
    tables = get_tables(main_page_soup)

    def get_table() -> list:
        for i, table in enumerate(tables):
            for r, row in enumerate(table.find_all('tr')):
                for column in row:
                    if column.string == district_name:
                        return [i, r, table]

    i, r, table = get_table()
    rows = get_rows(table)
    corresponding_tag = rows[r].find('td', {'headers': f't{i+1}sa3'})
    url_extension = corresponding_tag.a.attrs.get('href')
    district_url = SERVER_URL + url_extension
    return district_url

def csv_recording(list_of_results: list, file_name: str):
    header = [item for item in list_of_results[0]]
    with open(f'{file_name}.csv', 'w+', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(list_of_results)

def main():
    soup = get_soup(GENERAL_URL)
    tables = get_tables(soup)
    result_list = []
    for table in tables:
        rows = get_rows(table)
        for row in rows[2:]:
            try:
                link = os.path.join(SERVER_URL + get_partional_url(row))
            except TypeError:
                '''Continuous protection for empty rows in tables'''
                break
            numeric_name = row.find('a').string
            municipality_name = row.find_all('td')[1].string
            if not municipality_name:
                municipality_name = row.find_all('td')[1].text

            municipality_soup = get_soup(link)
            municipality_tables = get_tables(municipality_soup)
            registered = municipality_tables[0].find('td', {'headers': 'sa3'}).string.replace(u'\xa0', u'')
            envelopes = municipality_tables[0].find('td', {'headers': 'sa5'}).string.replace(u'\xa0', u'')
            valid = municipality_tables[0].find('td', {'headers': 'sa6'}).string.replace(u'\xa0', u'')

            municipality = {'code': numeric_name, 'location': municipality_name, 'registered': registered,
                            'envelopes': envelopes, 'valid': valid}

            for t in municipality_tables[1:]:
                for r in t.find_all('tr')[2:]:
                    party_name = r.find_all('td')[1].string.replace(u'\xa0', u' ')
                    party_votes = r.find_all('td')[2].string.replace(u'\xa0', u' ')
                    municipality[party_name] = party_votes.replace(u'\xa0', u' ')
            result_list.append(municipality)

    return result_list


if __name__ == '__main__':
    municipality = input('Please insert the name or the path to the desired district:\n')
    file_name = input('Please insert file name where results of scraping will be stored: ')

    if '\\' in municipality or '/' in municipality:
        while True:
            GENERAL_URL = municipality
            try:
                results = main()
            except:
                print('\nProvided path is not valid.')
                ending = input('If you want to type path to district once more pres enter\ntype any key to end program.\n')
                if not ending:
                    municipality = input('Please insert the path to the desired district:\n')
                    continue
                else:
                    sys.exit()
            csv_recording(results, file_name)
            print('='*60)
            print(f'Election results were stored in {file_name}.csv file.')
            print(f'The path to the file is: {os.path.join(os.getcwd(),(file_name + ".csv"))}')
            ending = input('Please enter any key to end the script.')

    else:
        while True:
            try:
                GENERAL_URL = get_district_url(municipality)
                csv_recording(main(), file_name)
                print('=' * 60)
                print(f'Election results were stored in {file_name}.csv file.')
                print(f'The path to the file is: {os.path.join(os.getcwd(),(file_name + ".csv"))}')
                ending = input('Please enter any key to end the script.')
                break
            except:
                print('The name if the district is not valid!')
                ending = input('If you want to type district once more pres enter\ntype any key to end program. ')
                if not ending:
                    municipality = input('Please insert the name of the desired district:\n')
                    continue
                else:
                    sys.exit()
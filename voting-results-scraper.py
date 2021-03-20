import click
import requests
from bs4 import BeautifulSoup
import json
import pandas


@click.command()
@click.option('--region_unit_url', prompt='URL to scrape', help='URL of the website to scrape data from.')
@click.option('--filename', prompt='File name with .csv extension', help='Name of the output CSV file.')
def scrape(region_unit_url, filename):
    """Web scraper for voting results data"""

    print(region_unit_url, filename)

    base_url = "".join(region_unit_url.partition('ps2017nss/')[0:2])

    print(base_url)

    response = requests.get(region_unit_url)

    content = response.content
    parsed_html = BeautifulSoup(content, 'html.parser')
    content = parsed_html.find("div", {"id": "content"})
    t3_divs = content.find_all("div", {"class": "t3"})
    region_voting_data = []

    for t3_div in t3_divs:

        tr_elements = t3_div.find_all("tr")
        for tr_element in tr_elements:

            town_data = {}
            try:
                town_data["town_code"] = tr_element.find("td", {"class": "cislo"}).find("a").string
                town_data["town_name"] = tr_element.find("td").find_next_sibling("td").text
                town_url = "".join(base_url + tr_element.find("td").find_next_sibling("td").find_next_sibling("td")
                                   .find("a", href=True)["href"])

                # data from town area page
                if "/ps33?" in town_url:
                    # town has multiple areas so go inside to get the data
                    response = requests.get(town_url)
                    content = response.content
                    parsed_html = BeautifulSoup(content, 'html.parser')
                    content = parsed_html.find("div", {"id": "content"})
                    td_elements = content.find_all("td")

                    area_code = 1
                    for td_element in td_elements:
                        try:
                            if td_element.find("a"):
                                town_data["area"] = area_code
                                area_url = "".join(base_url + td_element.find("a", href=True)["href"])
                                area_data = get_area_voting_data(area_url, town_data)
                                region_voting_data.append(area_data.copy()) # uuuhh python references, take a copy!!
                                area_code += 1
                                print(area_data)
                                print("\n")
                        except AttributeError:
                            pass

                else:
                    # town has only one area
                    town_data["area"] = 1
                    region_voting_data.append(get_town_voting_data(town_url, town_data).copy())
                    print(town_data)
                    print("\n")

            except AttributeError:
                pass


    #print(json.dumps(region_voting_data, indent=2))
    dataFrame = pandas.DataFrame(region_voting_data)
    dataFrame.to_csv("region_voting_data.csv", encoding="utf-8-sig", index=False)


def get_town_voting_data(town_url, town_data):
    response = requests.get(town_url)
    content = response.content
    parsed_html = BeautifulSoup(content, 'html.parser')
    content = parsed_html.find("div", {"id": "content"})
    ps311_t1_element = content.find("table", {"id": "ps311_t1"})
    town_data["voters"] = ps311_t1_element.find("td", {"headers": "sa2"}).text
    town_data["envelopes"] = ps311_t1_element.find("td", {"headers": "sa3"}).text
    town_data["legal_votes"] = ps311_t1_element.find("td", {"headers": "sa6"}).text

    # get political parties
    political_parties = []
    political_party_tables = content.find("div", {"id": "inner"})
    pp_tr_elements = political_party_tables.find_all("tr")

    for pp_tr_element in pp_tr_elements:
        try:
            political_parties.append(pp_tr_element.find("td").find_next_sibling("td").text)
        except AttributeError:
            pass

    town_data["political_parties"] = political_parties
    return town_data


def get_area_voting_data(area_url, town_data):
    response = requests.get(area_url)
    content = response.content
    parsed_html = BeautifulSoup(content, 'html.parser')
    content = parsed_html.find("div", {"id": "content"})
    ps311_t1_element = content.find("table", {"id": "ps311_6_t1"})
    town_data["voters"] = ps311_t1_element.find("td", {"headers": "sa2"}).text
    town_data["envelopes"] = ps311_t1_element.find("td", {"headers": "sa3"}).text
    town_data["legal_votes"] = ps311_t1_element.find("td", {"headers": "sa6"}).text

    # get political parties
    political_parties = []
    political_party_tables = content.find("div", {"id": "inner"})
    pp_tr_elements = political_party_tables.find_all("tr")

    for pp_tr_element in pp_tr_elements:
        try:
            political_parties.append(pp_tr_element.find("td").find_next_sibling("td").text)
        except AttributeError:
            pass

    town_data["political_parties"] = political_parties
    return town_data


def generateCsvFile(filename, data):
    """Saves the data into a csv file."""


if __name__ == '__main__':
    scrape()

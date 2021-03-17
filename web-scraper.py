import click
import requests
from bs4 import BeautifulSoup
import csv


@click.command()
@click.option('--url', prompt='URL to scrape', help='URL of the website to scrape data from.')
@click.option('--filename', prompt='File name with .csv extension', help='Name of the output CSV file.')
def scrape(url, filename):
    """Simple web scraper for a page http://pythonhow.com/example.html"""

    # Headers are being passed into the request because the website http://pythonhow.com doesn't like parsers.
    # By specifying the headers we tell the website that our request comes from a browser.
    response = requests.get('http://pythonhow.com/example.html',
                            headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu;'
                                                   'Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    content = response.content
    parsedHtml = BeautifulSoup(content, 'html.parser')
    divElements = parsedHtml.findAll("div", {"class": "cities"})
    cities = []

    for item in divElements:
        cities.append(item.find("h2").text)

    click.echo('\n====================================\n')
    click.echo('Scraping the data from: %s \n' % url)
    click.echo('Done scraping \n')
    generateCsvFile(filename, cities)


def generateCsvFile(filename, data):
    """Saves the data into a csv file."""

    click.echo('Saving the data... \n')

    with open(filename, mode='w') as citiesFile:
        citiesWriter = csv.writer(citiesFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        citiesWriter.writerow(['Cities'])
        for city in data:
            citiesWriter.writerow(
                [city])  # the writerow method accepts a collection, try passing in just a string to see what happens :)

    click.echo('Saved the scraped data to: %s \n' % filename)


# This tells python to run the scrape() method as a main function when web-scraper.py is executed
if __name__ == '__main__':
    scrape()

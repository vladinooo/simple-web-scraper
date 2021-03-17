import click

@click.command()
@click.option('--url', prompt='URL to scrape', help='URL of the website to scrape data from.')
@click.option('--filename', prompt='File name', help='Name of the output CSV file.')


def scrape(url, filename):

    """Simple web scraper."""

    click.echo('====================================')
    click.echo('Scraping the data from: %s' % url)
    click.echo('Done scraping')
    generateCsvFile(filename)


def generateCsvFile(filename):
    click.echo('Saving the data...')
    click.echo('Saved the scraped data to: %s' % filename)



# This tells python to run the scrape() method as a main function when web-scraper.py is executed
if __name__ == '__main__':
    scrape()

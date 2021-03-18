import requests
from bs4 import BeautifulSoup
import pandas

def scrape():

    baseUrl = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/#t=0&s="

    propertyDataList = []

    # Go through multiple pages
    # Range 0 = start from page 0; 30 = up to page 30; 10 = in increments of 10 pages
    for page in range(0, 30, 10):
        response = requests.get(baseUrl + str(page) + ".html",
                                headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu;'
                                                       'Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        content = response.content
        parsedHtml = BeautifulSoup(content, 'html.parser')
        divElements = parsedHtml.findAll("div", {"class": "propertyRow"})

        for element in divElements:
            propertyData = {}

            # Use the try/except block as some of the elements will return the None object.
            # The None object doesn't have the "text" function and an exception AttributeError is thrown
            try:
                propertyData["Address"] = element.find_all("span", {"class": "propAddressCollapse"})[0].text
            except AttributeError:
                propertyData["Address"] = None

            try:
                propertyData["Locality"] = element.find_all("span", {"class": "propAddressCollapse"})[1].text
            except AttributeError:
                propertyData["Locality"] = None

            try:
                propertyData["Price"] = element.find("h4", {"class": "propPrice"}).text.replace("\n", "").replace(" ", "")
            except AttributeError:
                propertyData["Price"] = None

            try:
                propertyData["Beds"] = element.find("span", {"class": "infoBed"}).find("b").text
            except AttributeError:
                propertyData["Beds"] = None

            try:
                propertyData["Area"] = element.find("span", {"class": "infoSqFt"}).find("b").text
            except AttributeError:
                propertyData["Area"] = None

            try:
                propertyData["Full baths"] = element.find("span", {"class": "infoValueFullBath"}).find("b").text
            except AttributeError:
                propertyData["Full baths"] = None

            try:
                propertyData["Half baths"] = element.find("span", {"class": "infoValueHalfBath"}).find("b").text
            except AttributeError:
                propertyData["Half baths"] = None

            for columnGroup in element.find_all("div", {"class": "columnGroup"}):
                # The zip function makes tuples from two collections
                for featureGroup, featureName in zip(columnGroup.find_all("span", {"class": "featureGroup"}),
                                                     columnGroup.find_all("span", {"class": "featureName"})):
                    if "Lot Size" in featureGroup.text:
                        try:
                            propertyData["Lot size"] = featureName.text
                        except AttributeError:
                            propertyData["Lot size"] = None

            propertyDataList.append(propertyData)

    dataFrame = pandas.DataFrame(propertyDataList)

    # Reindex the columns the way we want
    dataFrame = dataFrame.reindex(
        columns=["Address", "Locality", "Lot size", "Area", "Beds", "Full baths", "Half baths", "Price"])

    dataFrame.to_csv("property-data.csv")


if __name__ == '__main__':
    scrape()

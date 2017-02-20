from googleapiclient.discovery import build
import urllib.request
import os
from PyPDF2 import PdfFileReader
from PyPDF2 import utils


def getAPIKey():
    """
    API Key stored in seperate file for easy managing (and hiding from GIT
    uploads. Sorry, not sorry.
    :return: API Key
    """
    with open("API_Key.txt") as file:
        my_api_key = file.readline()
    return my_api_key


def getCX():
    """
    CX Code is the code for the custom search engine set up through google.
    Set to search all internet, very basic.
    :return: Returns ID for use in search
    """
    with open("SE_Code.txt") as file:
        my_id = file.readline()
        return my_id


def search(my_api_key,my_id,search_keyword,searchtype,count):
    """
    Query to the Google API for the search term. Result comes back as a JSON,
    which is then returned for parsing.
    :param my_api_key: API Key for google search.
    :param my_id: ID for the Custom Search Engine you created.
    :param search_keyword: Keyword for the search
    :param searchtype: Filetype you are searching for: going to hard code to pdf for now
    :param count: The start index for the search - used to loop through all 100 results allowed.
    :return: results of the search to be parsed
    """
    service = build("customsearch", version="v1", developerKey=my_api_key)
    res = service.cse().list(q=search_keyword, cx=my_id, fileType=searchtype, start=count).execute()
    return res


def parseResults(res,urls):
    """
    Parse the results to get the urls and save to list to be pulled.
    :param res: Results from API search to be parsed
    :param urls: List to add urls from results
    :return: List of the urls of PDFs
    """
    i = 0
    while i < 10:
        urls.append(res['items'][i]['link'])
        i += 1
    return urls


def pdfScrape(term,urls):
    """
    Save out the PDFs from the urls. Saves the urls of the PDFs that were not
    saved properly to an errors file for manual download and analyzation later.
    :param term: the search term being used for naming conventions
    :param urls: urls to grab PDFs from
    :return: none
    """
    errors = []
    if not os.path.exists(term):
        os.makedirs(term)
    fileNumber = 1
    for url in urls:
        try:
            # HTTPCookieProcessor removed an error with redirects? Looking into it.
            response = urllib.request.build_opener(urllib.request.HTTPCookieProcessor).open(url)
            with open(term + "/" + term + str(fileNumber) + ".pdf", "wb") as file:
                file.write(response.read())
        # HTTP request failed error - investigating
        except urllib.request.HTTPError:
            print("Error finding: " + url)
            # Save the erroed urls for manual use later
            errors.append(url)
        # URL error on URL from search - investigating
        except urllib.request.URLError:
            print("Error with URL: " + url)
            # Save the erroed urls for manual use later
            errors.append(url)
        fileNumber += 1
    # Save out errored urls
    with open(term + "_errors.txt", "w") as file:
        for i in errors:
            file.write(i + "\n")


def metaDump(term):
    """
    Get the metadata from the saved pdfs and save it out
    to a file for easier analyzing.
    :param term: search term used for naming conventions
    :return: none
    """
    info = {}
    for file in os.listdir(term):
        with open(term + "/" + file, "rb") as f:
            try:
                # open the file, get the metadata, then store in dictionary
                pdf_toread = PdfFileReader(f)
                pdf_info = pdf_toread.getDocumentInfo()
                info[file] = pdf_info
            # PDF error when file may be encrypted? - investigating
            except utils.PdfReadError:
                print("Error getting data from " + file + ". May be encrypted.")
            # General error except for possible library issues? - investigating
            except:
                print("General error with: " + file)
    # General metadata saving. TODO : Much better data handling needed. Looking into possible database.
    with open("metadata.txt", "w") as outfile:
        for i in info.keys():
            outfile.write(str(info[i]) + '\n')



if __name__ == '__main__':
    # Term to be searched for using API
    search_keyword = input("Keyword for search: ")
    # ask for filetype, if none default to pdf
    searchtype = input("Filetype to search: ")
    if searchtype == "":
        searchtype = "PDF"
    # Obtain current API key for search
    my_api_key = getAPIKey()
    # get cx id for the custom search
    my_id = getCX()
    # list for holding discovered URLs
    urls = []
    # count for number of results
    count = 1
    # loop search to get urls
    while count < 100 + 1:
        res = search(my_api_key, my_id, search_keyword, searchtype, count)
        urls = parseResults(res, urls)
        count += 10
    # grab search term for naming purposes TODO : Come up with a better naming convention
    term = search_keyword.replace(" ", "")
    # Save urls to file.. not necessary for script, but thought it was good for records/thought process
    with open(term+".txt", "w") as file:
        for url in urls:
            file.write(url + '\n')
    # Scrape the PDFs from discovered URLs
    pdfScrape(term, urls)
    # Dump out the metadata from the PDFs for analyzing
    metaDump(term)


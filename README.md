# Europeana Combine Harvester
The Europeana Combine harvester takes a query and a few parameters, and downloads all of the records the Search API returns. It download metadata in JSON format, and download the actual images/text files in a separate folder. Thus, it's a combine harvester. 
naming props go to @AdrianMurphy

## TO DO
- bug: script now skips objects with MIME Type Image/jpeg;utf-8, because mimetypeguess guesses None
- bug: script exits when handling exceptions. Make sure script passes in the while loop when excepting.
- bug: maximum amount of records to fetch only checks after every API call, which means the minimum amount of records fetched now is 100, and incerements by 100. 
- feature: instead of using json.dump, download metadata 1 item at a time and don't download metadata objects of which the object file cannot be downloaded.
- feature: split JSON dump into more than 1 JSON file to avoid getting humongous JSON files
- feature: download HasView objects if they are available, with same europeana id but with added `-1`
- feature: start input checking
- feature: create error logs

## Description
This harvester was initially created for the V4Design project. It is written in Python 3.6. and uses a few modules. It relies mostly on the Requests module (http://docs.python-requests.org/en/master/)

The harvester achieves two things:

- automatic metadata download
- automatic object download

The user enters:
- an API key (pro.europeana.eu/get-api)
- a query (e.g. ducks)
- the maximum amount of records to fetch (e.g. 1000)
- a reusability profile (open, permission, or restricted)

The script then creates a folder with todays date, and a .json file. Metadata gets written to the JSON file, and objects get downloaded to the folder. Objects are sorted by their dataset number in separate folders, and are named with their Europeana ID and the right file extension.

Allowed file extensions are: [".jpg", "jpeg", ".jpe", ".gif", ".tiff", ".pdf", ".txt", ".mp3",".doc",".docx",".odt",".png",".mpeg",".mpg",".mp4",".wmv"]

The requests module will send these headers to the websites it is requesting files from:
{
'User-Agent': 'Europeana data and metadata harvester v1.0',
'From' : 'jolan.wuyts[at]europeana.eu'
}
The script handles server-side errors fairly well, trying not to overload data providers' servers by making too many calls. When encountering download issues, the script will print these errors in the command line. It does not create error logs as of yet. 

When choosing a reusability filter, the script will only return and try to download objects that fall into that reusability category. If you don't enter a reusability filter, the script will return and download objects with any type of rights statement. At the end of the script a tally is made of how many objects were downloaded with which rights statement, and will display information on how to reuse the objects you downloaded correctly. Reusing objects correctly is the responsibility of the user, all necessary rights statement information has been given to ensure that the user is informed of what and how to reuse the downloaded objects.

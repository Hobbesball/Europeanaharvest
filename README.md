# Europeanaharvest
Metadata and object harvester using the Europeana Search API

## TO DO
- bug: script now skips objects with MIME Type Image/jpeg;utf-8, because mimetypeguess guesses None
- feature: split JSON dump into more than 1 JSON file to avoid getting humongous JSON files
- feature: download HasView objects if they are available, with same europeana id but with added `-1`
- bug: script exits when handling exceptions. Make sure script passes in the while loop when excepting.
- feature: start input checking
- feature: create a dict that keeps all the different rights statements attached to objects, and counts the amount of objects downloaded with those rights statements. Show these rights statements and their counts when the script finishes, with a disclaimer urging the user to adhere to attribution and copyright policies.

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

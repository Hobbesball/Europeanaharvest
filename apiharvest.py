# this script was written by Jolan Wuyts for Europeana. It was primarily developed to download datasets for the V4Design European project. It is a python 3 script that uses a few minor libraries, of which the requests library is used the most extensively.

#this script allows a user to download a json file of records from the response of the Europeana Search API to a query. The user inputs the query, the requested reusability, and the requested maximum amount of records to fetch. It uses cursor-based pagination to make it possible to get more than 960 items, as is the limit on Europeana Collections

#Secondly, this script also download all files that are in the allowed list of extensions and are referenced in the edm:IsShownBy or the edm:Object fields of the records.

# import stuff
import requests
from datetime import date
import json
import os
from mimetypes import guess_extension
from time import sleep

#query parameters
apikey = input('enter your API key (you can get it at pro.europeana.eu/get-api ): \n')
query = input('enter your query:  \n')

fetchedrecords=0
rows=100
records=''
limit=int(input("maximum amount of records to fetch:  \n"))
cursor='*'
profile= 'rich'
reusability=input("enter reusability: \n")
start=500
skippedrecords=0


#list of allowed exts
allowed_exts = [".jpg", "jpeg", ".jpe", ".gif", ".tiff", ".pdf", ".txt", ".mp3",".doc",".docx",".odt",".png",".mpeg",".mpg",".mp4",".wmv"]
#headers to send along with the HTTP requests
headers = {
'User-Agent': 'Europeana data and metadata harvester v1.0',
'From' : 'jolan.wuyts@europeana.eu'
}


#get date of today
today = date.today()
filename = str(today)+".json"

#make directories


#create a function to download image and text file_put_contents
def download(url, fname):
    #check if url contains an image
    if 'image' in url.headers['content-type'].lower():
        print("This is an image! image type: ", url.headers['content-type'])
        #get the extension by guessing it from the content type.
        fileext = guess_extension(url.headers['content-type'].split()[0].rstrip(";"))
        #check if file extension is in the list of allowed extensions
        if fileext in allowed_exts:
            #create file name
            filename = fname+fileext
            print ("filename: ",filename)
            #check if directory already exists, if not create directory. create file in correct directory. This will create folders per dataset
            imgdir = str(today)+"-download/"+filename
            os.makedirs(os.path.dirname(imgdir), exist_ok=True)
            #create image in our image directory
            with open(imgdir, 'wb') as file:
                #write content to file
                print("directory: ",file)
                file.write(url.content)
                print("written to directory!\n")
        else:
            print ("file extension not allowed: ", fileext)
            pass
        #check if url contains text
    elif 'text' in url.headers['content-type'].lower():
        print("This is text! text type: ", url.headers['content-type'])
        #get the extension by guessing it from the content type, strip to cover more bases
        fileext = guess_extension(url.headers['content-type'].split()[0].rstrip(";"))
        if fileext in allowed_exts:
            #create file name
            filename = fname+fileext
            print ("filename: ",filename)
            #check if directory already exists, if not create directory. create file in correct directory. This will create folders per dataset
            imgdir = str(today)+"-download/"+filename
            os.makedirs(os.path.dirname(imgdir), exist_ok=True)
            #create file in directory
            with open(imgdir, 'wb') as file:
                #write content to file
                print("directory: ",file)
                file.write(url.content)
                print("written to directory!\n")
        else:
            print ("file extension not allowed: ", fileext)
            pass
    elif 'application' in url.headers['content-type'].lower():
        print("This is an application! app type: ", url.headers['content-type'])
        #get the extension by guessing it from the content type, strip to cover more bases
        fileext = guess_extension(url.headers['content-type'].split()[0].rstrip(";"))
        if fileext in allowed_exts:
            #create file name
            filename = fname+fileext
            print ("filename: ",filename)
        #check if directory already exists, if not create directory. create file in correct directory. This will create folders per dataset
            imgdir = str(today)+"-download/"+filename
            os.makedirs(os.path.dirname(imgdir), exist_ok=True)            #create file in directory
            with open(imgdir, 'wb') as file:
                #write content to file
                print("directory: ",file)
                file.write(url.content)
                print("written to directory!\n")

        else:
            print ("file extension not allowed: ", fileext)
            pass
    else:
        print("this ain't image or text")
        pass

#make the request
print ("Making request for query: ", query)
with open(filename, 'w') as outfile:
    while records=='' or (records!=0 and fetchedrecords<=records and fetchedrecords<=limit) and cursor !='':
        r=requests.get("https://www.europeana.eu/api/v2/search.json?wskey="+apikey+"&query="+query+"&rows="+str(rows)+"&profile="+profile+"&cursor="+cursor+"&reusability="+reusability)
    #return request status
        print ("request status: ", r.status_code)
    #if JSON request succeeds
        if r.raise_for_status() == None:
            #get JSON data
            data = r.json()
            print ("request successful!\n")
            #if the responded JSON has 'true' as its success parameter
            if data["success"] == True:
                print("response successful!\n")
                #change records to the totalResults amount
                records = data["totalResults"]
                #if the search returned hits
                if records !=0:
                    print("total results: ",records,"\n")
                    print("downloading images and writing JSON of ",fetchedrecords+1,"-",fetchedrecords+rows+1)
                    #write metadata to json file
                    cursor = data["nextCursor"]
                    json.dump(data["items"], outfile)
                    print ("wrote json to file.")
                    #add the amount of records to fetchedrecords
                    fetchedrecords+=rows
                    #for every record in this API call
                    for i in range(data["itemsCount"]):
                        #check if the record has an isshownby
                        if 'edmIsShownBy' in data['items'][i]:
                            #get the HTTP link to the image
                            imgurl = data['items'][i]['edmIsShownBy'][0]
                            fname = data['items'][i]['id']
                            print ('fname: ',fname)
                            try:
                                imgr = requests.get(imgurl, allow_redirects=True, headers=headers, timeout=2)
                                #call 'download' function to download the edmIsShownBy
                                if imgr.status_code == 200:
                                    download(imgr, fname)
                                elif imgr.status_code == 429:
                                    download(imgr, fname)
                                    print("HTTP error 429, retry after: ", imgr.headers['Retry-After'], " seconds")
                                else:
                                    print ("image status: ",imgr.status_code)
                                    skippedrecords+=1
                            #handle exceptions by printing the exception, adding one to skippedrecords, and moving on
                            #except requests.exceptions.Timeout:
                            #    sleep(1)
                            #    print("sleeping because of Timeout")
                            #    pass
                            except requests.exceptions.RequestException as e:
                                print (e)
                                skippedrecords+=1
                                pass
                        elif 'edmObject' in data['items'][i]:
                            #get the HTTP link to the image
                            imgurl = data['items'][i]['edmObject'][0]
                            fname = data['items'][i]['id'][0]
                            try:
                                imgr = requests.get(imgurl, allow_redirects=True, headers=headers, timeout=2)
                                #call 'download' function to download the edmObject
                                if imgr.status_code == 200:
                                    download(imgr, fname)
                                elif imgr.status_code == 429:
                                    download(imgr, fname)
                                    print("HTTP error 429, retry after: ", imgr.headers['Retry-After'], " seconds")
                                else:
                                    print ("image status: ",imgr.status_code)
                                    skippedrecords+=1
                            #handle exceptions by printing the exception, adding one to skippedrecords, and moving on
                            except requests.exceptions.RequestException as e:
                                print (e)
                                skippedrecords+=1
                                pass
                        else:
                            print ("no edm:IsShownBy or edm:Object")
                            skippedrecords+=1
                            pass
                    print("fetching next API response")
                else:
                    print ("Search returned no hits, exiting.")
                    break
            else:
                print("JSON responded with  success = False.\n")
                break
        else:
            print ("request returned an error, code: ",r.status_code)
            pass
    print ("amount of non-downloaded records: ", skippedrecords, "\n Amount of downloaded records: ", fetchedrecords)

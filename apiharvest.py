# this script was written by Jolan Wuyts for Europeana. It was primarily developed to download datasets for the V4Design European project. It is a python 3 script that uses a few minor libraries, of which the requests library is used the most extensively.

#this script allows a user to download a json file of records from the response of the Europeana Search API to a query. The user inputs the query, the requested reusability, and the requested maximum amount of records to fetch. It uses cursor-based pagination to make it possible to get more than 960 items, as is the limit on Europeana Collections

#Secondly, this script also download all files that are in the allowed list of extensions and are referenced in the edm:IsShownBy or the edm:Object fields of the records.

# import stuff
import getpass
import requests
from datetime import date
import json
import os
from mimetypes import guess_extension
from time import sleep
from urllib import parse

#query parameters
apikey = getpass.getpass('enter your API key (you can get it at pro.europeana.eu/get-api ): \n')
query = input('enter your query:  \n')

class vars:
    fetchedrecords=0

rowcount=0
rows=100
records=''
limit=int(input("maximum amount of records to fetch:  \n"))
cursor='*'
profile= 'rich'
reusability=input("enter reusability: \n")
start=500
skippedrecords=0
reusabilitycount={}

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
                #add 1 to fetchedrecords
                vars.fetchedrecords+=1
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
                #add 1 to fetchedrecords
                vars.fetchedrecords+=1
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
                #add 1 to fetchedrecords
                vars.fetchedrecords+=1
        else:
            print ("file extension not allowed: ", fileext)
            pass
    else:
        print("this ain't image or text")
        pass

#make the request
print ("Making request for query: ", query)
with open(filename, 'w') as outfile:
    #when we are just starting (records='') OR we have downloaded records but not all (fetchedrecords is smaller than records) AND we haven't reached our record limit (fetchedrecords is smaller than limit) AND our cursor value is not empty (cursor is not '')
    while records=='' or (records!=0 and vars.fetchedrecords<=records and vars.fetchedrecords<=limit) and cursor !='':
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
                    print("downloading images and writing JSON of ",rowcount+1,"-",rowcount+rows+1)
                    #get nextCursor value to feed back into the next API call. urlencode the value using the urllib parse module
                    try:
                         cursor = parse.quote_plus(data["nextCursor"])
                    except KeyError:
                         print(KeyError())
                         break
                    #write metadata to json file
                    json.dump(data["items"], outfile)
                    print ("wrote json to file.")
                    #add the amount of records to fetchedrecords
                    rowcount+=rows
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
                                    #get rights statement of the item, add it to the rights statements directory
                                    if data['items'][i]['rights'][0] in reusabilitycount:
                                        reusabilitycount[data['items'][i]['rights'][0]]+=1
                                    else:
                                        reusabilitycount[data['items'][i]['rights'][0]]=1
                                elif imgr.status_code == 429:
                                    download(imgr, fname)
                                    #get rights statement of the item, add it to the rights statements directory
                                    if data['items'][i]['rights'][0] in reusabilitycount:
                                        reusabilitycount[data['items'][i]['rights'][0]]+=1
                                    else:
                                        reusabilitycount[data['items'][i]['rights'][0]]=1
                                        #this is unfinished: if status code is 429, you should try to download anyway. If you can't download, print this error. Now it calls the download function anyway and also shows this message, regardless of if it downloaded or not. future feature: if the download function fails, reqeue these images
                                    print("HTTP error 429, retry after: ", imgr.headers['Retry-After'], " seconds")
                                else:
                                    print ("image status: ",imgr.status_code)
                                    skippedrecords+=1
                            #handle exceptions by printing the exception, adding one to skippedrecords, and moving on
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
                                    #get rights statement of the item, add it to the rights statements directory
                                    if data['items'][i]['rights'][0] in reusabilitycount:
                                        reusabilitycount[data['items'][i]['rights'][0]]+=1
                                    else:
                                        reusabilitycount[data['items'][i]['rights'][0]]=1

                                elif imgr.status_code == 429:
                                    download(imgr, fname)
                                    #get rights statement of the item, add it to the rights statements directory
                                    if data['items'][i]['rights'][0] in reusabilitycount:
                                        reusabilitycount[data['items'][i]['rights'][0]]+=1
                                    else:
                                        reusabilitycount[data['items'][i]['rights'][0]]=1
                                    #this is unfinished: if status code is 429, you should try to download anyway. If you can't download, print this error. Now it calls the download function anyway and also shows this message, regardless of if it downloaded or not. future feature: if the download function fails, reqeue these images
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
    print ("Total amount of records with downloaded metadata: ",skippedrecords+vars.fetchedrecords,"\nAmount of non-downloaded objects: ", skippedrecords, "\nAmount of downloaded objects: ", vars.fetchedrecords)
    print ("\n\n Please be aware that, depending on which reusability filter you chose, you may have to make sure you correctly attribute objects when reusing them, follow the guidelines for reuse set out by the copyright statements attached to the objects, or make sure you do not reuse the object at all if that is explicitly stated.\n")
    if reusability == "open":
        print ("You've chosen an open reusability filter. This means all of the objects that you have downloaded are free to re-use. You might still have to attribute the owner of the object if the object's rights statement is CC BY or CC BY-SA. You must redistribute any new content you create with objects with a CC BY-SA rights statement with a Creative Commons license as well. For more information, please visit rightsstatements.org and creativecommons.org\n")
        print("the rights statements attached to the objects you've downloaded are: ", reusabilitycount)
    elif reusability == "restricted":
        print ("You've chosen a restricted reusability filter. This means that, at the very least, correct attribution is needed when you reuse the objects you've downloaded, as well as compliance to the restrictions on reuse of those objects. Some objects might have a non-derivative clause attached to them (CC BY NC-ND, CC BY-ND, CC OOC-NC). Other objects might expressly state they cannot be used for commercial purposes (CC BY-NC, CC BY-NC-SA, NoC-NC,...) For more information, please visit rightsstatements.org and creativecommons.org")
        print("the rights statements attached to the objects you've downloaded are: ", reusabilitycount)
    elif reusability == "permission":
        print ("You've chosen a 'permission needed' reusability filter. This means the objects cannot be reused when express permission has not been given by the copyright holder of the object (Rs InC). It is also possible that the copyright of objects in this category is unkown (Unknown), not evaluated (RS CNE), or the object is an EU orphan work (RS InC-OW-EU). For more information, please visit rightsstatements.org and creativecommons.org")
        print("the rights statements attached to the objects you've downloaded are: ", reusabilitycount)
    else:
        print("you were not supposed to enter the reusability filter you entered, and for some reason this error wasn't caught by our input checker. weird. Anyway. Did you know a group of ferrets is referred to as a business? You seemed to have weaseled your way into a place that is none of your business.")
        print("the rights statements attached to the objects you've downloaded are: ", reusabilitycount)

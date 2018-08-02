# encountered errors while running the script:

##error encountered 2.08.2018 at 11:25CEST:

File "/Users/jolanwuyts/anaconda/envs/py36/lib/python3.6/site-packages/urllib3/connection.py", line 150, in new_conn
self, "Failed to establish a new connection: %s" % e)
urllib3.exceptions.NewConnectionError: <urllib3.connection.VerifiedHTTPSConnection object at 0x111d37630>: Failed to establish a new connection: [Errno 60] Operation timed out

raise MaxRetryError(pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='www.europeana.eu', port=443): Max retries exceeded with url: /api/v2/record/91643/SMVK_OM_objekt_108108.json?profile=rich&wskey=****** (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x111d37630>: Failed to establish a new connection: [Errno 60] Operation timed out',))

raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPSConnectionPool(host='www.europeana.eu', port=443): Max retries exceeded with url: /api/v2/record/91643/SMVK_OM_objekt_108108.json?profile=rich&wskey=***** (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x111d37630>: Failed to establish a new connection: [Errno 60] Operation timed out',))

##error encountered 2.08.2018 at 11:48AM CEST:

File "apiharvest.py", line 197, in <module>
    if recordr.raise_for_status() == None:
  File "/Users/jolanwuyts/anaconda/envs/py36/lib/python3.6/site-packages/requests/models.py", line 935, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 500 Server Error: Internal Server Error for url: https://www.europeana.eu/api/v2/record/91643/SMVK_OM_objekt_112105.json?profile=rich&wskey=****

##error encountered 2.08.2018 at 3:46 PM CEST:
### => error 401 is raised when the wrong API key is entered.

401
Traceback (most recent call last):
 File "apiharvest.py", line 130, in <module>
   if r.raise_for_status() == None:
 File "/Users/jolanwuyts/anaconda/envs/py36/lib/python3.6/site-packages/requests/models.py", line 935, in raise_for_status
   raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 401 Client Error: Unauthorized for url: https://www.europeana.eu/api/v2/search.json?wskey=****&query=proxy_dcterms_isPartOf%3A%22collectie%3A%20ornamentprenten%22%20AND%20(%22vaas%22%20OR%20%22kan%22)&rows=100&profile=rich&cursor=\*&reusability=open
(py36) Jolans-Typewriter:Europeanaharvest jolanwuyts$ python apiharvest.py
enter your API key (you can get it at pro.europeana.eu/get-api ):

## error encountered 2.08.2018 at 5:09PM:
### => this error occurs when the code makes an API call even though there are no more items to call.

Traceback (most recent call last):
  File "apiharvest.py", line 155, in <module>
    for i in range(data["itemsCount"]):
KeyError: 'itemsCount'
(py36) Jolans-Typewriter:Europeanaharvest jolanwuyts$ 

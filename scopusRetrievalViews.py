import requests
import json
              
#Scopus Author Retrieval API
#This method allows you to choose which attribute you wish to retrieve based on the author retrieval views from Elsevier Developers
def getAuthorInfo():
    url = ("https://api.elsevier.com/content/author/author_id/36629511500?field=h-index,document-count,cited-by-count,citations-count,coauthor-count,surname,given-name,affiliation-name,prism:coverDate" )
    resp =  requests.get(url, headers= {'Accept' : 'application/json',
                                          'X-ELS-APIKEY': '27e18faa69686d68b0e5878262f218c8' })
    print(json.loads(resp.text.encode('utf-8')))

    # with open("scopus_author_data_36629511500.json", "w") as write_file:
    #     json.dump(resp.json(), write_file)

    return json.loads(resp.text.encode('utf-8'))

getAuthorInfo()
import requests
import json

#Swap the author ID with the unique scopus ID collected
#This method returns all of the author retrieval views

resp = requests.get("http://api.elsevier.com/content/author?author_id=55537160300&view=metrics",
                    headers={'Accept':'application/json',
                             'X-ELS-APIKey': 'e168a6b5ee3d66abd8e6351c31b38be2'})

print (json.dumps(resp.json(),
                 sort_keys=True,
                 indent=4, separators=(',', ': ')))

#Rename each of the file individually
with open("Tan Chun Yuan 55537160300 male.json", "w") as write_file:
    json.dump(resp.json(), write_file)
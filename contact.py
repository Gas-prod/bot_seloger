import requests
import json
import os

def contact(url, email, msg, name, phone):
    id = url.split(".htm")
    id = id[0].split("/")
    id = int(id[-1])

    s = requests.Session()

    s.headers.update({
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    })
    
    params = {
        "email": email,
        "listingId": id,
        "listingPublicationId": 3006087,
        "message": msg,
        "name": name,
        "phone": phone
    }

    res = s.post("https://www.seloger.com/annoncesbff/2/Contact", json=params)
    
    return res.content

print(contact("https://www.seloger.com/annonces/locations/appartement/paris-4eme-75/saint-merri/193939295.htm?&cmp=AL-SLG-Boost-new&utm_source=email_ali&utm_medium=B2C_SL_Service_Email_AlerteImmoBoost&utm_campaign=163434819_20221116&utm_term=annclass&pvd=SLG", os.getenv("PHONE"), "ceci est un test à ignorer", os.getenv("NAME"), os.getenv("PHONE")))
import os
import requests

def contact(url, email, msg, name, phone):
    id = url.split(".htm")
    id = id[0].split("/")
    id = int(id[-1])

    s = requests.Session()

    s.headers.update({
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    })
    
    payload = {
        "email": email,
        "listingId": id,
        "listingPublicationId": 1,
        "message": msg,
        "name": name,
        "phone": phone
    }

    res = s.post("https://www.seloger.com/annoncesbff/2/Contact", json=payload)
    
    return res.content
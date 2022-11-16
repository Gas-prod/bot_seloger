import email_listener
import os
from bs4 import BeautifulSoup

# Set your email, password, what folder you want to listen to, and where to save attachments
email = os.getenv("FROM_EMAIL") + "@gmail.com"
app_password = os.getenv("FROM_PWD")
folder = "Inbox"
attachment_dir = "test"
el = email_listener.EmailListener(email, app_password, folder, attachment_dir)

#fonction appelée pour chaque mail non lu à traiter
def test(self, msgs):
    #msgs est un dictionnaire
    
    for i in msgs:
        author = i.split("_", 1)[1]
        msg = msgs[i]
        
        if author == "seloger@a.seloger.com":
            
            #enlever les caractères bizarres du mail
            txt = msg["HTML"].replace("&amp;", "&")
            txt = txt.replace("=\r\n", "")
            txt = txt.replace("3D", "")
            txt = txt.replace("=2E", ".")
            
            soup = BeautifulSoup(txt, features="html5lib") #convertir le mail en html

            links = []

            #recuperer tous les liens du mail
            for link in soup.find_all('a'):
                href = link.get('href')
                href = href[3:len(href) - 3] #encore enlever des caractères bizarres au debut et a la fin
                
                links.append(href)

            #recuperer que les liens d'annonces de logement
            links = [i for i in links if i.startswith("https://www.seloger.com/annonces/")]
            tmp_list = []
            final_list = []

            #enlever les doublons
            for i in links:
                link = i.split(".htm")[0] #recuperer que le debut du lien
                
                if link not in tmp_list: 
                    tmp_list.append(link)
                    final_list.append(i)
                    print(link)

            links = final_list #liste final des liens d'annonces sans doublons

# Log into the IMAP server
el.login()

# Get the emails currently unread in the inbox
messages = el.scrape()

# Start listening to the inbox and timeout after an hour
timeout = 60
el.listen(timeout, test)
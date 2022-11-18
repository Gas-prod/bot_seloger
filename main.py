import email_listener
import os
from bs4 import BeautifulSoup
from contact import contact

# Set your email, password, what folder you want to listen to, and where to save attachments
email = os.getenv("FROM_EMAIL") + "@gmail.com"
app_password = os.getenv("FROM_PWD")
folder = "Inbox"
attachment_dir = ""
el = email_listener.EmailListener(email, app_password, folder, attachment_dir)

#fonction appelée pour chaque mail non lu à traiter
def on_email(self, msgs):
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
            
            print(msg["Subject"])

            if msg["Subject"] != "Votre demande de contact !":
            
                soup = BeautifulSoup(txt, features="html5lib") #convertir le mail en html
    
                links = []
    
                #recuperer tous les liens du mail
                for link in soup.find_all('a'):
                    href = link.get('href')
                    href = href[3:len(href) - 3] #encore enlever des caractères bizarres au debut et a la fin
                    
                    links.append(href)
    
                #recuperer que les liens d'annonces de logement
                links = [i for i in links if i.startswith("https://www.seloger.com/annonces/")]
    
                #enlever les doublons
                tmp_list = [] #liste des liens coupes
                final_list = [] #liste des liens
                for i in links:
                    link = i.split(".htm")[0] #recuperer que le debut du lien
                    
                    if link not in tmp_list: 
                        tmp_list.append(link)
                        final_list.append(i)
                        print(i)
    
                links = final_list #liste final des liens d'annonces sans doublons

                for link in links:
                    print(contact(link, email, "ceci est un test à ignorer", os.getenv("NAME"), os.getenv("PHONE")))

# Log into the IMAP server
el.login()

# Start listening to the inbox and timeout after an hour
timeout = 60
el.listen(timeout, on_email, unread=True)
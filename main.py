import email_listener
import os
from bs4 import BeautifulSoup
from contact import contact

# Set your email, password, what folder you want to listen to, and where to save attachments
email = os.getenv("FROM_EMAIL") + "@gmail.com"
app_password = os.getenv("FROM_PWD")
folder = "test"
attachment_dir = ""
el = email_listener.EmailListener(email, app_password, folder, attachment_dir)
contact_message = "Je ne suis interressé par aucun appartement, je fais simplement des tests, merci d'ignorer ma demande, désolé pour l'éventuel dérangement."
name = os.getenv("NAME")
phone = os.getenv("PHONE")

#fonction appelée pour chaque mail non lu à traiter
def on_email(self, msgs):
    #msgs est un dictionnaire
    
    for i in msgs:
        msg = msgs[i]

        #enlever les caractères bizarres du mail
        txt = msg["HTML"].replace("&amp;", "&")
        txt = txt.replace("=\r\n", "")
        txt = txt.replace("3D", "")
        txt = txt.replace("=2E", ".")

        #vérifier que le mail est pas une pub ou retour de contact
        if msg["Subject"] != "Votre demande de contact !" and "annonce" in msg["Subject"]:
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
            
            for i in links:
                cut_link = i.split(".htm")[0] #recuperer que le debut du lien
                
                if cut_link not in tmp_list: 
                    tmp_list.append(cut_link)
                    print(link, "\n")
                    print(contact(i, email, contact_message, name, phone), "\n")

# Log into the IMAP server
el.login()

#Traiter les mails non lu reçus avant le démarrage du bot
messages = el.scrape()
on_email(1, messages)

# Start listening to the inbox and timeout after an hour
timeout = 60
el.listen(timeout, on_email)
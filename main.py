import email_listener
import os
from bs4 import BeautifulSoup
from contact import contact

# Set your email, password, what folder you want to listen to, and where to save attachments
email = os.getenv("FROM_EMAIL")
app_password = os.getenv("FROM_PWD")
folder = os.getenv("FOLDER")
attachment_dir = ""
el = email_listener.EmailListener(email, app_password, folder, attachment_dir)
contact_message = os.getenv("MESSAGE")
name = os.getenv("NAME")
phone = os.getenv("PHONE")

if None in [email, app_password, folder, contact_message, name, phone]:
    raise ValueError("Vous devez bien creer toutes les variables d'environnements pour que le bot fonctionne. voire variables_a_creer.tkt")

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
            links = [x for x in links if x.startswith("https://www.seloger.com/annonces/")]

            #enlever les doublons
            tmp_list = [] #liste des liens coupes
            
            for i in links:
                link = i.split(".htm")[0] #recuperer que le debut du lien
                
                if link not in tmp_list and not "cta_recommandation_annonce" in link: 
                    tmp_list.append(link)
                    print(i, "\n")
                    #envoyer la requête pour contacter l'agence
                    print(contact(link, email, contact_message, name, phone).decode("utf-8"), "\n")

# Log into the IMAP server
el.login()

#Traiter les mails non lu reçus avant le démarrage du bot
messages = el.scrape()
on_email(1, messages)

# Start listening to the inbox and timeout after an hour
timeout = 60
el.listen(timeout, on_email)
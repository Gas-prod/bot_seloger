import email_listener
import os
from bs4 import BeautifulSoup

# Set your email, password, what folder you want to listen to, and where to save attachments
email = os.getenv("FROM_EMAIL") + "@gmail.com"
app_password = os.getenv("FROM_PWD")
folder = "Inbox"
attachment_dir = "test"
el = email_listener.EmailListener(email, app_password, folder, attachment_dir)

def test(self, msgs):
    for i in msgs:
        author = i.split("_", 1)[1]
        msg = msgs[i]

        if author == "seloger@a.seloger.com":
            txt = msg["HTML"].replace("&amp;", "&")
            txt = txt.replace("=\r\n", "")
            txt = txt.replace("3D", "")
            txt = txt.replace("=2E", ".")
            
            soup = BeautifulSoup(txt, features="html5lib")

            links = []
            
            for link in soup.find_all('a'):
                href = link.get('href')
                href = href[3:len(href) - 3]
                
                links.append(href)

            links = list(set(links))
            
            print(links)

# Log into the IMAP server
el.login()

# Get the emails currently unread in the inbox
messages = el.scrape()

# Start listening to the inbox and timeout after an hour
timeout = 60
el.listen(timeout, test)
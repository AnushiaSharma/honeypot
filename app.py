import threading
from ssh_honeypot import start_honeypot
from web_honeypot import start_web

t1 = threading.Thread(target=start_honeypot)
t2 = threading.Thread(target=start_web)

t1.start()
t2.start()
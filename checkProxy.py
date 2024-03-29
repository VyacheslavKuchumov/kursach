import threading
import queue

import requests


q = queue.Queue()
validProxies = []

with open("validProxies.txt", "w") as f:
    f.write("")

with open("proxyList.txt", "r") as f:
    proxies = f.read().split("\n")

    for p in proxies:
        q.put(p)


def check_proxies():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("http://ipinfo.io/json",
                               proxies={
                                   "http": proxy,
                                   "https": proxy
                               })
        except:
            continue
        if res.status_code == 200:
            print(proxy)
            with open("validProxies.txt", "a") as f:
                f.write(proxy+"\n")


for _ in range(10):
    threading.Thread(target=check_proxies).start()

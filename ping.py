import urllib.request
try:
    urllib.request.urlopen("http://localhost:3000/")
except Exception as e:
    print(e)

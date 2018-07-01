# A robots.txt based Info Gathering Crawler

import requests

def connect(url):
  try:
    if url[-1] != '/':
      url += '/'
    req = requests.get(url + 'robots.txt')
    if req.status_code == 200:
      return req.text
    else:
      exit('robots.txt unavailable')
  except requests.exceptions.RequestException as e:
    print('Error: %s' % e)
    exit(1)

def getRobots(request):
  None

if __name__ == '__main__':
  None

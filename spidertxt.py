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

def tryRobotsLines(robots, url):
  if url[-1] != '/':
    url += '/'
  for item in robots:
    if item[-1] != '/':
      item += '/'
    if item.startswith('Disallow'):
      firstIndex = int(item.index('/'))
      lastIndex = int(item.rindex('/'))
      item = item[firstIndex+1:lastIndex]
      req = requests.get(url + item)
      print(f'{url + item} - {req.status_code}')
 

def getRobots(request):
  if request:
    robots = [line for line in filter(None, request.split("\n"))]
    print(robots)
    return robots
  else:
    exit('robots.txt unavailable')

if __name__ == '__main__':
  robots = getRobots(connect('https://hackingu.net'))
  print()
  tryRobotsLines(robots, 'https://hackingu.net')

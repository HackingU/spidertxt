# A robots.txt based Info Gathering Crawler

import requests
import sys

def getUrl(args):
    if len(args) > 1:
        return args[1]
    else:
        exit('No URL found.\nPlease specify a valid URL.')

def fixUrl(url):
    if url[-1] != '/':
        url += '/'
    if not url.startswith('http://'):
        url = 'http://' + url
    return url

def connect(url):
    try:
        req = requests.get(url + 'robots.txt')
        # print(req.history[0].headers['Location'])
        if req.status_code == 200:
            return req.text
        else:
            exit('robots.txt unavailable')
    except requests.exceptions.RequestException as e:
        print('Error: %s' % e)
        exit(1)

def tryRobotsLines(robots, url):
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


def main():
    url = getUrl(sys.argv)
    url = fixUrl(url)
    robots = getRobots(connect(url))
    tryRobotsLines(robots, url)


if __name__ == '__main__':
    main()

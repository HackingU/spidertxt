# A robots.txt based Info Gathering Crawler

import requests
import sys
from os import system, name


def getUrl(args):
    if len(args) > 1:
        return args[1]
    else:
        exit('No URL found.\nPlease specify a valid URL.')


def fixUrl(url):
    if url[-1] != '/':
        url += '/'
    if not url.startswith('http://') and url.startswith('https://'):
        url = url.replace('https://', '')
        url = 'http://' + url
    return url


def connect(url):
    try:
        req = requests.get(url + 'robots.txt')
        if req.status_code == 200:
            return req.text
        else:
            exit('robots.txt unavailable')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        exit(1)


def tryRobotsLines(robots, url):
    for robot in robots:
        if robot[-1] != '/':
            robot += '/'
        if robot.startswith('Disallow'):
            firstIndex = int(robot.index('/'))
            lastIndex = int(robot.rindex('/'))
            robot = robot[firstIndex+1:lastIndex]
            req = requests.get(url + robot)
            print(f'Item: {url + robot} - Status code: {req.status_code}')

            # Not necessary to show history because can't fix http/https bug
            # if (req.history) and (req.history[0].status_code == 301 or req.history[0].status_code == 302):
            # 	print(f"Redirected from: {req.history[0].headers['Location']} - Status code: {req.history[0].status_code}")
            content = req.text
            title = everything_between(content, '<title>', '</title>')
            if title.startswith('Index of '):
                listIndexOfContent(url + robot)


def getRobots(request):
    if request:
        robots = [line for line in filter(None, request.split("\n"))]
        print(f'{robots}\n')
        return robots
    else:
        print('robots.txt unavailable')


def everything_between(content, begin, end):
    idx1 = content.find(begin)
    idx2 = content.find(end, idx1)
    return content[idx1+len(begin):idx2].strip()


def listIndexOfContent(url):
    req = requests.get(url)
    req_text = req.text
    tag_begin = '<a href="'
    tag_end = '">'
    req_text_lines = req_text.split('\n')
    for line in req_text_lines:
        line = line.strip()
        if tag_begin in line:
            item = everything_between(line, tag_begin, tag_end)
            print(f'{item}')


def main():
    url = getUrl(sys.argv)
    url = fixUrl(url)
    print(f'URL: {url}\n')
    robots = getRobots(connect(url))
    tryRobotsLines(robots, url)


if __name__ == '__main__':
    main()

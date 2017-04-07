import google
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import subprocess

from http.server import SimpleHTTPRequestHandler
import socketserver
import urllib
from urllib.parse import urlparse, parse_qs

from Imagify import Imagify
import os
import requests,json
from bs4 import BeautifulSoup
import time

BASE_URL = "http://farzeen.hopto.org/"



class S(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("got get request %s" % (self.path))
        print("curdir %s "%os.getcwd())
        if self.path == '/':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        if self.path.startswith('/share'):
            return SimpleHTTPRequestHandler.do_GET(self)
        if self.path.startswith('/imagifycache'):
            print(self.path)
            return SimpleHTTPRequestHandler.do_GET(self)

        get_vars = parse_qs(urlparse(self.path).query)

        if self.path.startswith('/imagify'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(Imagify('imagifycache').render_page(get_vars),'utf-8'))
            return
        if self.path.startswith('/links'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            url = get_vars['url'][0]
            content = "<html><body><u>Links at {}</u>".format(url)
            html_page = urllib.request.urlopen(url)
            soup = BeautifulSoup(html_page)
            for link in soup.findAll('a'):
                link_url = urllib.parse.urljoin(url,link.get('href'))
                content += "<a href='/imagify?url={}'>{}</a><br>\n"\
                        .format(link_url,link.string)
            content+="</body></html>"
            self.wfile.write(bytes(content,'utf-8'))
            return


        if self.path.startswith('/google'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes('<html>\n\t<body>\n','utf-8'))
            for url in google.search(get_vars['q'][0],stop=5):
                if url.startswith('https://'):
                    url = url.replace('https://','http://',1)
                if url.startswith('http://en.wikipedia'):
                    url = url.replace('en.wiki','en.m.wiki',1)
                self.wfile.write(bytes('\t\t<br><a href=\'/imagify?url={}\'>{}</a>\n'.format(url,url),'utf-8'))
            self.wfile.write(bytes('\t</body>\n</html>','utf-8'))
            return
        if self.path.startswith('/trains'):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(\
                bytes("<html><body><h1>Live Train Status<h1><br>{}"\
                        .format(time.strftime("%H:%M %d/%m/%Y"))
                      ,'utf-8'))
            stations = ['CAN','TLY','CLT','TIR']
            for station in stations:
                r = requests.post('http://www.hgapis.com/railapi/v1/livestn',
                                  {'stn_code':station,
                                   'api_key':api_keys[station],
                                   'app_version':'1.0'})
                trains = json.loads(r.content.decode('utf-8'))['trains']
                self.wfile.write(bytes("<h1>{}</h1>".format(station),'utf-8'))
                for t in trains:
                    self.wfile.write(bytes("<h2>{}:{}</h2> Route:{} Arrival:{}({}) Departure:{}({}) PF:{} <br>".format(t['train_num'],t['train_name'],t['route'],t['exp_arr'],t['del_arr'],t['exp_dep'],t['del_dep'],t['exp_pf']),'utf-8'))

############################

def run(port=8080):
    httpd = socketserver.TCPServer(("",port),S)
    print("Serving at {}".format(port))
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

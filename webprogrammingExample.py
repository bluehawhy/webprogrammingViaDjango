
# 2.2.1. urlparse module
def module_urlparsing():
    from urllib.parse import urlparse
    url ="http://www.python.org:80/guido/pyton/html;philosophy?overall=3#n10"
    print(urlparse(url))
    
# 2.2.2 urllib module
def module_urllibByGet():
    from urllib import request
    url ='http://www.example.com/'
    f = request.urlopen(url)
    print(f.read(500).decode('utf-8'))

def module_urllibByPost():
    from urllib import request, parse
    url ='http://www.example.com'
    # need parsing and data should be dict
    data = parse.urlencode({"query":"python"}).encode()
    f = request.urlopen(url,data)
    print(f.read(500).decode('utf-8'))

def module_setHeader():
    from urllib import request, parse
    url ='http://www.example.com'
    req = request.Request(url)
    req.add_header('Content-Type','text/plain')
    req.data = parse.urlencode({"query":"python"}).encode()
    f = request.urlopen(req)
    print(f.read(500).decode('utf-8'))

def module_authRequest():
    from urllib import request
    #HTTPBasicAuthHandler instance created for Authentication
    auth_handler = request.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='PDQ Application',
    uri = 'https://mahler:8092/site-updates.py',
    user='klem',
    passwd='kadidd!ehopper'
    )

    #opener build
    opener = request.build_opener()

    #opener install
    request.install_opener(opener)
    url ='http://www.example.com/login.html'
    f = request.urlopen(url)
    print(f)

# 2.2.3 urllib module example
def example_urllib():
    from urllib import request, parse
    from html.parser import HTMLParser
    class ImageParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag != 'img':
                return
            if not hasattr(self,'result'):
                self.result = []
            for name, value in attrs:
                if name == 'src':
                    self.result.append(value)
    def parseImage(data):
        parse = ImageParser()
        parse.feed(data)
        dataSet = set(x for x in parse.result)
        print('\n'.join(sorted(dataSet)))
    def main():
        url = 'http://google.co.kr'
        f = request.urlopen(url)
        charset = f.headers.get_content_charset()
        data = f.read().decode(charset)
        f.close()
        print('\n >>>>>> Fetch Images from', url)
        parseImage(data)
    main()

# 2.2.4 httplib module
class module_httplib(): 
    def get():
        import http.client as hc
        url ='www.example.com'
        conn = hc.HTTPConnection(url)
        conn.request('GET', '/index.html')
        r1 = conn.getresponse()
        print("status code : %s, reason: %s" %(r1.status, r1.reason))
        data1 = r1.read()
        conn.request('GET', '/parrot.spam')
        r2 = conn.getresponse()
        print("status code : %s, reason: %s" %(r2.status, r2.reason))
        data2 = r2.read()
        conn.close()
    
    def head():
        import http.client as hc
        url ='www.example.com'
        conn = hc.HTTPConnection(url)
        conn.request('HEAD', '/index.html')
        res = conn.getresponse()
        print("status code : %s, reason: %s" %(res.status, res.reason))
        data = res.read().decode('utf-8')
        print(data)
        print(len(data))
        print(data =='')

    def post():
        import http.client as hc
        from urllib import request, parse
        params = parse.urlencode({'@number':12524, '@type':'issue','@action':'show'}).encode()
        headers = {'Content-type':'application/x-www-form-unlencoded',
        'Accept':'text/plain'}
        url ='bugs.python.org'
        conn = hc.HTTPConnection(url)
        conn.request("POST",'',params,headers)
        res = conn.getresponse()
        print("status code : %s, reason: %s" %(res.status, res.reason))
        data = res.read()
        print(data)
        conn.close()
    def put():
        import http.client as hc
        BODY = '***filecontents***'
        conn = hc.HTTPConnection('localhost',8888)
        conn.request('PUT','/file',BODY)
        res = conn.getresponse()
        print("status code : %s, reason: %s" %(res.status, res.reason))

# 2.2.5 httplib example
def example_httplib():
    import http.client as hc
    from urllib import request, parse
    from html.parser import HTMLParser
    import os

    class ImageParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag != 'img':
                return
            if not hasattr(self,'result'):
                self.result = []
            for name, value in attrs:
                if name == 'src':
                    self.result.append(value)
    
    def downloadImage(srcUrl,data):
        download_path_name = 'DOWNLOAD'
        if not os.path.exists(download_path_name):
            os.makedirs(download_path_name)
        
        imgparser = ImageParser()
        imgparser.feed(data)
        resultSet = set(x for x in imgparser.result)

        for x in sorted(resultSet):
            src = parse.urljoin(srcUrl,x)
            basename = os.path.basename(src)
            targetFile = os.path.join(download_path_name,basename)

            print( 'Downloading.....', src)
            request.urlretrieve(src, targetFile)

    def main():
        url = 'www.google.co.kr'
        conn = hc.HTTPConnection(url)
        conn.request('GET','')
        res = conn.getresponse()
        charset = res.headers.get_content_charset()
        data = res.read().decode(charset)
        conn.close()

        print('\n >>>>>>> Download Images from ', url)
        url = parse.urlunparse(('http',url,'','','',''))
        #url = parse.urlparse('http',url)
        downloadImage(url,data)
    
    main()


#2.3 simple webserver example
def example_basicWebServer():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    
    class MyHandler(BaseHTTPRequestHandler):
        def _set_response(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            self._set_response()
            self.wfile.write("welcome to minsu's page".encode())
            print('someone take my page')
    
    def main():
        ip ='localhost'
        port = 8888
        server = HTTPServer((ip,port),MyHandler)
        print('Start webserver %s %d' %(ip,port))
        print('Press ^C to quit webserver')
        server.serve_forever()

    main()

# 2.4.4 wsgiref,simple_server module

def module_wsgiref():
    def my_app(environ, start_response):
        status ="200 OK"
        headers = [('Content-Type','text/plain')]
        start_response(status,headers)
        return ['this is a sample WSGI App'.encode()]

    def main():
        ip ='localhost'
        port = 8888
        from wsgiref.simple_server import make_server
        print('started WSGI server on %s %d....' %(ip,port))
        server = make_server(ip,port,my_app)
        server.serve_forever()
    
    main()

if __name__ == "__main__":
    module_wsgiref()
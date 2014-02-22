import urllib.request
from html.parser import HTMLParser

counter = 0
Output = []

class MyHTMLParser(HTMLParser):          
    '''
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)
    '''
    def handle_data(self, data):        
        global counter
        global Output       
        
        Output.append(data)
        counter += 1
                                          
        if counter == 3:
            print(Output)
            s = set(Output)
            counter = 0
            Output.clear()
        
a = '<tr class="all_space1">'
b = '</table>'
x = 0

urlx = "http://twblg.dict.edu.tw/holodict_new/result.jsp?radiobutton=1&limit=200&querytarget=2&sample=^%E4%BB%96%24&submit.x=35&submit.y=23"
sock = urllib.request.urlopen(urlx)
parser = MyHTMLParser(strict=False)

for i in sock.read().decode("utf8").split('\n')[1:]:
        i = i.strip()        
        
        if i == a or x >0:
            x = 1                        
            parser.feed(i)
                                    
        if i == b:          
            x = 0
            
        
            
            
            
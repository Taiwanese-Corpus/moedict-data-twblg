import urllib.request
from html.parser import HTMLParser

counter = 0
Output = []

class MyHTMLParser(HTMLParser):        
      
    def handle_data(self, data):       
        global counter
        global Output 
        Output.append(data)
        final = list(set(Output))
        final.sort(key=Output.index)
        print("final=:")
        print(final)
        counter += 1

urlx = "http://twblg.dict.edu.tw/holodict_new/searchSuggest.jsp?sample=%E8%A8%B1&querytarget=2"
sock = urllib.request.urlopen(urlx)
parser = MyHTMLParser(strict=False)

        
parser.feed(sock.read().decode("utf8").strip() )
   

            
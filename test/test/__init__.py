import urllib.request
from html.parser import HTMLParser

counter = 0
Output = []

class MyHTMLParser(HTMLParser):          
    
    def handle_data(self, data):        
        global counter
        global Output       
        
        Output.append(data)
        counter += 1
                                          
        if counter == 3:
            print(Output)          
            counter = 0
            Output.clear()
        
a = '<tr class="all_space1">'
b = '</table>'
x = 0
全部國語詞 = ['其', '其中', '其他', '其他地方', '其實', '其次']
for i in 全部國語詞:
    print(i+":")
    w = urllib.request.quote(i)
    urlx = "http://twblg.dict.edu.tw/holodict_new/result.jsp?radiobutton=0&limit=20&querytarget=2&sample="+w+"&submit.x=42&submit.y=14"
    sock = urllib.request.urlopen(urlx)
    parser = MyHTMLParser(strict=False)

    for i in sock.read().decode("utf8").split('\n'):
        i = i.strip()        
        
        if i == a or x >0:
            x = 1                        
            parser.feed(i)
                                    
        if i == b:          
            x = 0
            
        
            
            
            
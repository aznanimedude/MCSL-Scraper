import html.parser

class MyHTMLParser(html.parser.HTMLParser):

    isQV = False
    countdown = 0
    
    def handle_starttag(self, tag, attrs):
        if self.isQV:
            print("Encountered a start tag:", tag)
#            for attr in attrs:
#                print("     attr:",attr)
        
    
    def handle_endtag(self, tag):
        if self.isQV:
            if self.countdown == 0:
                print("DETECTED END OF QV DATA")
                print("Encountered an end tag: ", tag)
            #else:
            #    self.countdown = self.countdown - 1
            #    print(self.countdown)
            
        
    
    def handle_data(self, data):
        
        print("Encountered some data: ", data)

        if data.endswith("(QV)"):
            print("GO MARLINS")
            self.isQV = True
            self.countdown = 0
        
        if data == "QUAIL VALLEY":
            print("GO MARLINS")
            print("Detected Relay Data")
            self.countdown = 3
            #print(self.countdown)
            self.isQV = True

        if self.isQV == True:
            if self.countdown == 0:
                print("DETECTED QV DATA")
                print("Encountered some data: ", data)
                self.isQV = False
            else:
                self.countdown = self.countdown - 1
                print(self.countdown)

        

with open(input("Enter html file name: ") + ".html") as myfile:
    content = myfile.read()

print(content)

parser = MyHTMLParser()
parser.feed(content)
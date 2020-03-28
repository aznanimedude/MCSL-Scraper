import html.parser
import requests

class MyHTMLParser(html.parser.HTMLParser):

    isQV = False
    relayCountdown = 0
    teamData = {}
    times = []
    currentName = ''
    currentEvent = ''
    def handle_starttag(self, tag, attrs):
        if self.isQV:
            print("Encountered a start tag:", tag)
#            for attr in attrs:
#                print("     attr:",attr)


    def handle_endtag(self, tag):
        if self.isQV:
            if self.relayCountdown == 0:
                print("DETECTED END OF QV DATA")
                print("Encountered an end tag: ", tag)
            #else:
            #    self.countdown = self.countdown - 1
            #    print(self.countdown)



    def handle_data(self, data):

        #print("Encountered some data: ", data)

        if data.startswith("Event"):
            self.currentEvent = data
            print("Found event", self.currentEvent)
            self.teamData[self.currentEvent] = {}

        if data.endswith("(QV)"):
            print("GO MARLINS")
            print("Start of QV data")
            self.isQV = True
            self.currentName = data
            print(self.currentEvent, self.currentName)
            self.times = []
            self.teamData[self.currentEvent][self.currentName] = self.times
            self.relayCountdown = 3
            print("added new swimmer to event", self.currentEvent)


        if data == "QUAIL VALLEY":
            print("GO MARLINS")
            print("Detected Relay Data")
            print("Start of QV data")
            self.relayCountdown = 3
            #print(self.countdown)
            self.isQV = True
            self.currentName = data
            self.times = []
            self.teamData[self.currentEvent][self.currentName] = self.times
            return


        if self.isQV == True:
            if self.relayCountdown == 0:
                print("DETECTED QV DATA")
                print("Encountered some data: ", data)
                self.teamData[self.currentEvent][self.currentName] = self.times
                self.isQV = False
            else:
                self.relayCountdown = self.relayCountdown - 1
                if data.endswith("(QV)") == False:
                    self.times.append(data)
                    #print(self.countdown)


    def getData(self):
        return self.teamData


#BEGIN SCRIPTING CODE

URL = "http://www.mcsl.org/Results/2019/week2/QVvCTC.html"
content = requests.get(URL)
print(content.text)
parser = MyHTMLParser()
parser.feed(content.text)
data = parser.getData()

print("------------------------------")
print("STARTING PRINTOUT")
#print(data)
for i in data:
    print(i)
    print(data[i])
    for j in data[i]:
        continue
"""
with open("output.txt","a") as outputfile:
    for i in data:
        outputfile.write(i)
        outputfile.write("\n")
        #for j in data[i]:
         #   outputfile.write(j)
          #  outputfile.write("\n")
"""

exit()
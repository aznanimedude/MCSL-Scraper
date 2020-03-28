import html.parser
import requests

class MyHTMLParser(html.parser.HTMLParser):

    isQV = False
    isRelay = False
    relayCountdown = 0
    teamData = {}
    times = []
    currentName = ''
    currentEvent = ''

    # generic starting tag handler, just prints if within a QV-related data portion
    def handle_starttag(self, tag, attrs):
        if self.isQV:
            print("Encountered a start tag:", tag)
#           for attr in attrs:
#               print("     attr:",attr)

    # generic starting tag handler, just prints if within a QV-related data portion
    def handle_endtag(self, tag):
        if self.isQV:
            if self.relayCountdown == 0:
                print("DETECTED END OF QV DATA")
                print("Encountered an end tag: ", tag)
            #else:
            #    self.countdown = self.countdown - 1
            #    print(self.countdown)


    # main portion, populates a nested dictionary based on the parsed data
    def handle_data(self, data):

        #print("Encountered some data: ", data)

        # read the Event data portion to indicate which event we're in
        # creates a dictionary key entry with the Event string as the index
        if data.startswith("Event"):
            self.currentEvent = data
            print("Found event", self.currentEvent)
            self.teamData[self.currentEvent] = {}

        # if the data ends in (QV), create a dictionary entry within the event dictionary with the format
        # {Swimmer name: [Seed Time, Actual Race Time]}
        if data.endswith("(QV)"):
            print("GO MARLINS")
            print("Start of QV data")
            self.isQV = True #set the isQV flag true
            self.currentName = data
            print(self.currentEvent, self.currentName)
            self.times = []
            self.teamData[self.currentEvent][self.currentName] = self.times # create nested dictionary entry
                                                                            # within event dictionary entry
            self.relayCountdown = 3 # counter to know how many subsequent entries to parse for the relevant data
            # print("added new swimmer to event", self.currentEvent)

        # format preceding a data entry for Relay times
        if data == "QUAIL VALLEY":
            print("Detected Relay Data")

            self.relayCountdown = 3
            #print(self.countdown)
            self.isQV = True
            self.isRelay = True
            #self.currentName = data
            self.times = []
            #self.teamData[self.currentEvent][self.currentName] = self.times
            return


        if self.isQV == True:
            if self.relayCountdown == 0:
                if self.isRelay:
                    self.currentName = self.times.pop()
                    print(self.currentName)
                print("DETECTED QV DATA")
                print("Encountered some data: ", data)
                self.teamData[self.currentEvent][self.currentName] = self.times
                self.isQV = False
                self.isRelay = False
#            elif self.isRelay:
#                self.relayCountdown = self.relayCountdown - 2
#                return
#                self.relayCountdown = self.relayCountdown - 1
            else:
                if data.endswith("(QV)") == False:
                    self.times.append(data)
                    self.relayCountdown = self.relayCountdown - 1
                    #print(self.times)
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

#    print(data[i])
    for j in data[i]:
        print(i, j, data[i][j][0], data[i][j][1])
#        print(j)
#       print(data[i][j][0])
#        print(data[i][j][1])
        continue

with open("output.txt","w") as outputfile:
    for i in data:
        outputfile.write(i)
        outputfile.write("\n")
        for j in data[i]:
            outputfile.write(str.join(" ", ("\t-\t",j, data[i][j][0], data[i][j][1])))
            outputfile.write("\n")
        #for j in data[i]:
         #   outputfile.write(j)
          #  outputfile.write("\n")


exit()
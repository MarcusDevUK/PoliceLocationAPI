import requests
import time
from matplotlib import pyplot
import tkinter as tk

key = open("key.txt","r").read() # KEY FOR PROGRAM

areasChosen = [[],[],[]] # 2D LIST
count = 0
for i in range(0,3):
    location = input("Enter a postcode (Remember a space): ")
    locationURL = "https://us1.locationiq.com/v1/search.php?key="+key+"&q="+location+"&format=json"
    response = requests.get(locationURL)
    areaData = response.json()
    if response.status_code == 200:
        lat = areaData[0]["lat"] # Latitude
        lng = areaData[0]["lon"] # Longitude
        areasChosen[count].append(lat) # Appending to the area chosen list
        areasChosen[count].append(lng)
        count+=1
    else:
        print("Error - Status code is not 200, Status code:"+str(response.status_code)+"\n Reload the application and try again.")
        time.sleep(4) # ^ Error Message
        exit()
print(areasChosen)


date = str(input("Enter a Year (YYYY)")) # Year input
month = str(input("Enter a Month (MM)")) # Month input

url = "https://data.police.uk/api/crimes-street/all-crime?poly="+areasChosen[0][0]+","+areasChosen[0][1]+":"+areasChosen[1][0]+","+areasChosen[1][1]+":"+areasChosen[2][0]+","+areasChosen[2][1]+"&date="+date+"-"+month
print(url) # ^ URL
currentResponse = requests.get(url) # Response (Status code) of url

data = currentResponse.json() # data from the request - /| Sometimes Throws up error if no data found |\
print(currentResponse)
feedback = ""
for x in data:
    
    if x["outcome_status"] is not None: # only output if data is available
        feedback += "Crime Type: "+ str(x["category"]) + ", Outcome Status:" + str(x["outcome_status"]) + "\n"
        
#    else:
#        feedback += "Crime Type: "+ str(x["category"]) + "- Outcome Status:" + str(x["outcome_status"]["category"]) + "\n"
print(feedback)
output = open("output.txt","w")
output.write(feedback)
output.close()

#--------------------------------------------------------------------------
def viewData(crimes): # Views Data and separates data via "," and strips out the "\n"
    crimes=0 # Amount of crimes
    specific=0 # Amount of specific crime
    i = 0
    for i in range(0,len(valuableData)):
        if data[i][0] == crime: # Checking list for data specified in the 2D list.
            specific+=1
        i+=1

    labels = "Crimes","Specific-Crime"
    genderData = [crimes,specific]
    pyplot.pie(genderData,labels=labels,autopct='%1.1f%%') # Plotting Pie chart with data of Crimes
    pyplot.show()


dataWindow = tk.Tk() # creating the window
dataWindow.title("Data Charts")
dataWindow.geometry("300x200")
colour = "#ffffff"
dataWindow.configure(bg=colour)

dataView = open("output.txt","r") # Reading data from the file
valuableData = []
for i in dataView:
    i=i.strip("\n")
    i=i.split(",")
    i=i.split(":")
    valuableData.append(i)
dataView.close()
print(valuableData)

for i in range(0,len(dataView)): # Giving a list of specific crimes
    print(dataView[i][0])
crime = str(input("Enter a specific crime"))
viewData(crime)

# https://data.police.uk/docs/method/crimes-at-location/
# https://data.police.uk/docs/method/crime-street/
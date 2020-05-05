from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "<br><h1 style='text-align:center;color:#404040;'>No target.</h1><br><hr style='color:#bfbfbf'><br>" + datetime.datetime.today().strftime("%m-%d-%Y at %X")




calander = []

def createEvent(time, len, mast, room, note): # create new timeslot # could refrence room index instead of new instantiation of room object
    if checkAvail(time, len, room) == True:
        calander.append(timeslot(time, len, mast, room, note))
        print("Room avalable. Reservation created.") # debug
        return True
    else:
        print("Room not avalable. Reservation not created") # debug
        return False

def checkAvail(time, leng, room): # if timeslot is avalable return true
    # check if time is out of bounds
    print("checkAvail(time)", time, "  ", leng) # debug
    # return false if time overlap of time occurs

    """
    # check if reservation is too far in future
    # NOT TESTED
    if time > datetime.datetime.now() + timedelta(days = 60):
        return False
    """
    
    # length of reservation between 30 and 60 minutes
    if (leng < 30 or leng > 60) or not (time >= datetime.datetime(time.year, time.month, time.day, 8, 0) and endTime(time, leng) <= datetime.datetime(endTime(time, leng).year, endTime(time, leng).month, endTime(time, leng).day, 14, 40)): # make sure length of reservation is within bounds AND make sure reservation times are within bounds
        #print("ERROR: reservation length is not in bounds OR reservation time is not within bounds.  ", time, endTime(time, leng), "   ", time >= datetime.datetime(time.year, time.month, time.day, 8, 0), "   ", endTime(time, leng) <= datetime.datetime(endTime(time, leng).year, endTime(time, leng).month, endTime(time, leng).day, 14, 40), "    ", time >= datetime.datetime(time.year, time.month, time.day, 8, 0) and endTime(time, leng) <= datetime.datetime(endTime(time, leng).year, endTime(time, leng).month, endTime(time, leng).day, 14, 40))
        return False # length is out of bounds 
    i = 0
    while i < len(calander): # loop through the existing list of timeslots in calander and see if there are any conflicts of time and room reservation
        # print("Iteration #", i) # debug
        if room == calander[i].room: # seperate if statement for efficancy
            if (time >= calander[i].time and time <= endTime(calander[i].time, calander[i].length)) or (endTime(time, leng) >= calander[i].time and endTime(time, leng) <= endTime(calander[i].time, calander[i].length)):
                return False
        i += 1
    return True

def endTime(time, leng):
    return time + datetime.timedelta(minutes=leng)
    """

    # *** NOTE: I did not realise timedelta function existed for datetime objects and completed the function of the below code with the single above statement. ***



    #return time + datetime.timedelta(minutes=leng) # need to test
    # create and return a datetime object at the time the reservation expires 
        # BUGS: day overlap if hour is added at 23 hours day does stays same  # more than double 60 min 
        # NOTE: not top priority, if program is given good data current code should work fine
    tmp = time
    if tmp.minute + leng < 60:
        tmp = datetime.datetime(tmp.year, tmp.month, tmp.day, tmp.hour, tmp.minute + leng)
    elif tmp.minute + leng >= 60:
        if tmp.hour < time.hour: # <= 23 check hour
            if tmp.day < time.day: # check day
                if tmp.month < time.month: # check month
                    if tmp.year < time.year: # check year
                        print()
                print()
            print()
        else:
            tmp = datetime.datetime(tmp.year, tmp.month, tmp.day, tmp.hour + 1, tmp.minute + leng - 60)
    else:
        print("wat")
        return -1
    print("Original: ", time, " Length: ", leng)
    print("One Line: ", time + datetime.timedelta(minutes=leng))
    print("Twenty Line: ", tmp)
    return tmp
    
def saveData():
    with open('roomList.txt', 'w') as filehandle:
        json.dump(roomList, filehandle)"""

class room:
    def __init__(self, i, n, s, t, a):
        self.roomnumber = i # room number or identifier 
        self.name = n # name of room (string)
        self.seating = s # how many people can the room hold (int)
        self.television = t # does the room have a television (boolean)
        self.additional = a # additional detales (string)
    
    def __str__(self):
        return "Room #: %s, Name: %s, Seating: %s, Television: %s, Additional information/details: %s" % (self.roomnumber, self.name, self.seating, self.television, self.additional)

    def shortList(self):
        return [self.roomnumber, self.name]

class timeslot:
    # start 8:00 end 2:40  30 min to 60 min reservations
    # time = datetime.datetime(2020, 1, 1, 8, 0)
    # time.year, time.month, time.day, time.hour, time.minute
    def __init__(self, t, len, mast, r, n):
        self.time = t
        self.length = len
        self.endTime = endTime(self.time, self.length)
        self.isMAST = mast
        self.room = r
        self.notes = n
    
    def __str__(self):
        return "Start time: %s, Length: %s, End time: %s, MAST day: %s, Room: %s, Notes: %s" % (self.time, self.length, self.endTime, self.isMAST, self.room.name, self.notes) # NOTE: room field only returns room name not entire room object
    
    def addNotes(self, note):
        self.notes = note

#load preset list of rooms from file
roomList = [ room("2000", "Room 1", 8, True, "Additional room information"), room("2001", "Room 2", 4, False, "Some more different room information") ] # predefined list of avalable rooms and amenities

def getDayEvents(day):
    eventlist = []
    i = 0
    for x in calander:
        if day.year == calander[i].time.year and day.month == calander[i].time.month and day.day == calander[i].time.day:
            eventlist.append(x)
        i += 1
    return eventlist


# allow loading of preset reservations/events from file
createEvent(datetime.datetime(2020, 4, 24, 8, 45), 59, False, roomList[0], "Reservation notes") # testing and demonstration: sample reservation
createEvent(datetime.datetime(2020, 4, 24, 11, 30), 59, False, roomList[0], "Additional reservation details") # testing and demonstration: sample reservation


# make error page template instad of one line
@app.route("/viewday/<rawday>") # view all events that occur on the passed date
def viewday(rawday):
    rawday.replace("-", "")
    if rawday == "MMDDYYYY" or rawday == "mmddyyyy": # check if input feild is left blank
        return "ERROR: Please enter date as format MMDDYYYY"
    day = datetime.datetime(int(rawday[4+2:8+2]), int(rawday[0:2]), int(rawday[2+1:4+1])) # convert string to datetime object
    if day < datetime.datetime.today() + datetime.timedelta(days=-1):
        return "ERROR: Can not make reservations for passed dates."
    if day.weekday() > 4:
        return "ERROR: Can not make reservations on weekends."
    rl = []
    for i in roomList:
        rl.append(i.shortList())
    return render_template('viewday.html', day=day.strftime("%m-%d-%Y"), eventlist=getDayEvents(day), mast=("checked" if day.weekday() == 2 else ""), rooms=rl, roomlist=roomList)

# add more data to individual day tiles ie. number of unreserved minutes left in that day
@app.route("/calander")
def webpage():
    weeklist = [["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],[],[],[],[]]
    weekno = 1
    while weekno < len(weeklist):
        c = 0
        day = datetime.datetime.today()
        if day.weekday() == 5:
            day = day + datetime.timedelta(days=2)
        if day.weekday() == 6:
            day = day + datetime.timedelta(days=1)
        if weekno == 1:
            while len(weeklist[weekno]) < day.weekday():
                print(day.weekday())
                weeklist[weekno].append("") # ten chars is length of regular timestamp
            while len(weeklist[weekno]) < len(weeklist):
                weeklist[weekno].append((day + datetime.timedelta(days=c,weeks=weekno-1)).strftime("%m-%d-%Y"))
                c += 1
        while len(weeklist[weekno]) < len(weeklist):
            weeklist[weekno].append((day + datetime.timedelta(days=c-day.weekday(),weeks=weekno-1)).strftime("%m-%d-%Y"))
            c += 1
        weekno += 1
    return render_template('calander.html', caltable=weeklist, roomlist=roomList)

@app.route('/reservation', methods=['POST', 'GET'])
def reservation():
    if request.method == 'POST':
        date = request.form['date']
        starttime = request.form['start']
        length = int(request.form['len'])
        isMAST = False
        if "isMAST" in request.form:
            if "on" == request.form['isMAST']:
                isMAST = True
        roomidx = int(request.form['room']) - 1
        notes = request.form['notes']
        stat = createEvent(datetime.datetime(int(date.replace("-", "")[-4:]), int(date.replace("-", "")[:2]), int(date.replace("-", "")[2:4]), int(starttime.replace(":", "")[:-2]), int(starttime.replace(":", "")[-2:])), length, isMAST, roomList[roomidx], notes)
        #createEvent(datetime.datetime(int(request.form['date'].replace("-", "")[-4:]), int(request.form['date'].replace("-", "")[:2]), int(request.form['date'].replace("-", "")[2:4]), int(request.form['start'].replace(":", "")[:-2]), int(request.form['start'].replace(":", "")[-2:]), request.form['len'], request.form['mast'], roomList[request.form['room']], request.form['notes']) # room is index of room on array
        """
        for i in calander: # clean up passed timeslots
            if i.time < datetime.datetime.today() - datetime.timedelta(days=-1):
                del calander[i]
        """
        return render_template('reservation.html', status="Sucess" if stat == True else "Fail", day=date)
    else:
        return "ERROR: used GET instead of POST?"

# create entire utility page
# delete/edit reservations & rooms
@app.route("/cleanup")
def cleanup():
    oldlen = len(calander)
    for i in calander:
        if i.time < datetime.datetime.today() - datetime.timedelta(days=-1):
            del calander[i]
    return "<title>Cleanup</title><p style='font-family: monospace;'>Cleaned up passed reservations. <br>Number of reservations before: " + str(oldlen) + " <br>Number of reservations now: " + str(len(calander)) + "</p>"
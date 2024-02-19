import datetime

import utils

def resetTimetable(timetable):
    for slot in timetable:
        if len(slot.customerList) == 0:
            slot.isFree = True
        else:
            slot.isFree = False
    return timetable

def getSlotLength(slot):
    date = datetime.date(1, 1, 1)
    start = datetime.datetime.combine(date, slot.start)
    end = datetime.datetime.combine(date, slot.end)
    slotLength = end - start
    return slotLength

def getDiffTime(datetime1, datetime2):
    if datetime1 < datetime2:
        delta = datetime2-datetime1
    else:
        delta = datetime1-datetime2
    return delta

def getMostSuitableSlot(customer, timetable):
    print(f"INFO: Get mostSuitableSlot for Customer {customer.id}.")
    mostSuitableSlot = []
    for window in customer.deliveryWindows:
        for slot in timetable:
            if window[0] <= slot.start and window[1] >= slot.end:
                if slot.isFree:
                    datetimeSlot = datetime.datetime.combine(customer.date, slot.start)
                    datetimeCust = datetime.datetime.combine(customer.date, customer.time)
                    diffToSlot = getDiffTime(datetimeSlot, datetimeCust)
                    if mostSuitableSlot:
                        dateTimeMostSuit = datetime.datetime.combine(customer.date, mostSuitableSlot.start)
                        diffToMostSuit = getDiffTime(dateTimeMostSuit, datetimeCust)
                        if diffToSlot < diffToMostSuit:
                            mostSuitableSlot = slot
                    else:
                        mostSuitableSlot = slot
    return mostSuitableSlot

def createSpecificTimetable(customer, timetable):
    for slot in timetable:
        if slot.customerList and len(slot.customerList) < 2:
            distance = utils.calculateDistance((slot.customerList[0].xCoord, slot.customerList[0].yCoord), (customer.xCoord, customer.yCoord))
            if distance <= 3:
                slot.isFree = True
                slot.price = "cheap"
                index = timetable.index(slot)
                if timetable[index-1]:
                    timetable[index-1].price = "cheap"
                if timetable[index+1]:
                    timetable[index+1].price = "cheap"
    return timetable

def insertIntoTimetable(customer, timetable): #needed for every variation
    print(f"INFO: Customer {customer.id} operating order!!")
    timetable = createSpecificTimetable(customer, timetable)
    preferredSlot = [slot for slot in timetable if slot.start == customer.time][0]
    if preferredSlot.isFree:
        print(f"INFO: Customer {customer.id} got its preferred slot.")
        customer.sReason = "Prefered Slot"
        customer.orderPrice = preferredSlot.price
        preferredSlot.customerList.append(customer)
    else:
        customer.satisfaction = "Dissatisfied"
        customer.sReason = "Not willing to wait and canceled order"
        print(f"INFO: Customer {customer.id} was not willing to wait and canceled the order.")
    timetable = resetTimetable(timetable)
    return timetable
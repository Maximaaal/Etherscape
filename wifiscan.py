# -*- coding: utf-8 -*-

import wifi
import time
from oscpy.client import OSCClient

#address = "192.168.0.141"
address = "127.0.0.1"
port = 8000
mainWifilist = []

def myFunc(e):
  return int(e['signal'])

def Search():
    wifilist = []

    cells = wifi.Cell.all('wlan0')

    for cell in cells:
        # print(cell.ssid)
        entry = {'ssid': cell.ssid, 'signal':cell.signal }
        wifilist.append(entry)
    # print(wifilist)
    wifilist.sort(key=myFunc, reverse=True)
    return wifilist


def FindDiffFromSearchList(wifilist1,wifilist2):
    # wifilist = Search()

    wifiDiff = []
    for cell_og in wifilist1:
        flag = False
        for cell in wifilist2:
            if cell_og['ssid'] == cell['ssid']:
                flag = True
        if (flag == False):
            wifiDiff.append(cell_og)
    return wifiDiff


def FindFromSavedList(ssid):
    cell = wifi.Scheme.find('wlan0', ssid)

    if cell:
        return cell

    return False


def Connect(ssid, password=None):
    cell = FindFromSearchList(ssid)

    if cell:
        savedcell = FindFromSavedList(cell.ssid)

        # Already Saved from Setting
        if savedcell:
            savedcell.activate()
            return cell

        # First time to conenct
        else:
            if cell.encrypted:
                if password:
                    scheme = Add(cell, password)

                    try:
                        scheme.activate()

                    # Wrong Password
                    except wifi.exceptions.ConnectionError:
                        Delete(ssid)
                        return False

                    return cell
                else:
                    return False
            else:
                scheme = Add(cell)

                try:
                    scheme.activate()
                except wifi.exceptions.ConnectionError:
                    Delete(ssid)
                    return False

                return cell
    
    return False


def Add(cell, password=None):
    if not cell:
        return False

    scheme = wifi.Scheme.for_cell('wlan0', cell.ssid, cell, password)
    scheme.save()
    return scheme


def Delete(ssid):
    if not ssid:
        return False

    cell = FindFromSavedList(ssid)

    if cell:
        cell.delete()
        return True

    return False

def printall(wifilist):
    for cell in wifilist:
        ssid = cell.ssid 
        signal = cell.signal
        print(str(ssid) + " SIGNAL " + str(signal))
        
def checkExistingSsid(ssid):
    for cell in mainWifilist:
        if cell['ssid'] == ssid:
            return True
    return False

def getSsid(ssid):
    index = 0
    for cell in mainWifilist:
        if cell['ssid'] == ssid:
            return index
        index = index + 1
    return False
    
def transmitOsc(transmit):
    osc = OSCClient(address, port)
    ssid_list = []
    for index, cell in enumerate(transmit):
        # ce
        signal = cell['signal']
        # ssid = str('/'+ str(index)+'/'+cell['ssid'])
        ssid = str('/'+ str(index))
        ssid_list.append(cell['ssid'])
        arr2 = bytes(ssid, 'ascii')
        osc.send_message(arr2,[signal])
        # osc.send_message(b'/signal', [signal])
    
    return hash(str(ssid_list))
        
def sortAndCut():
    mainWifilist.sort(key=myFunc, reverse=True)
    rest =  mainWifilist[0:10]
    return rest
    
    



while (True):
    time.sleep(4)
    wifilist = Search()
    for i in range(len(wifilist)):
        mainWifilist.append(wifilist[i])
    transmit = sortAndCut()
    print(transmit)
    # if len(transmit) > 1:
    transmitOsc(transmit)
    mainWifilist.clear()
    
    # print(wifilist)
    # print(wifilist2)
    # print(FindDiffFromSearchList(wifilist,wifilist2))
    # wifilist.sort()
    # printall(wifilist)



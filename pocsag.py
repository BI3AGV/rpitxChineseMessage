import os

charString = ""

freq = "152650000"  #Frequency in Hz
rate = "1200"  #POCSAG rate in bps
function = "3"  #function select
repeat = "1" #repeat times

def convertSpecialChar(c):
    #print(c)
    global charString
    if c in [0x22,0x5c,0x60,0x24]: #operate with " \ ` $ ,just add a "\"
        charString += chr(0x5c)
    elif c in [0x25]: #operate with "%" eg. Error:"%Jar" Right:"%%Jar"
        charString += chr(0x25)
    elif len(charString) > 0:
        if charString[-1] == "\\": #handle situation like "\\ar",the right should be "\\\ar"
            charString += chr(0x5c)
    

def sendPocsag(addr,message):
    rawString = list(message.encode('gb2312')) #decode string with gb2312
    global charString
    charString = "" #a string to storge converted bytes
    charset = 'gb2312' #a status flag to determin when to convert chinese and ascii characters
    for c in rawString:
        
        if c >= 128: #the MSB of a byte is 1 means the char is chinese 
            if charset != 'gb2312':
                charString += "\x0e"
                charset = 'gb2312'
            convertSpecialChar(c & 0b01111111)
            charString += chr(c & 0b01111111)
        else:
            if charset != 'ascii':
                charString += "\x0f"
                charset = 'ascii'
            convertSpecialChar(c)
            charString += chr(c)
    cmd = f"printf \"{addr}:{charString}\" | sudo /root/rpitx/pocsag -f {freq} -r {rate} -b {function} -t {repeat}"
    os.system(cmd)
    #print(cmd)
addr = input("呼机地址:")
while True:
    os.system("clear")
    print("--------------------------------------------")
    print("    RPITX 寻呼发射台 MODE:POCSAG1200")
    print("--------------------------------------------")
    msg = input(f"ADDR:{addr}#")
    sendPocsag(addr,msg)

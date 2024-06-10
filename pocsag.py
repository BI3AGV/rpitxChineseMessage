import os
import binascii

def sendPocsag(addr,message):
    rawString = list(message.encode('gb2312')) #decode string with gb2312
    charString = "" #a string to storge converted bytes
    charset = '' #a status flag to determin when to convert chinese and ascii charactors
    for c in rawString:
        
        if c >= 128: #the MSB of a byte is 1 means the char is chinese 
            if charset != 'gb2312':
                charString += "\x0e"
                charset = 'gb2312'
            if c & 0b01111111 in [0x22,0x25,0x5c]: #operate special char like "\
                charString += chr(0x5c)
            charString += chr(c & 0b01111111)
        else:
            if charset != 'ascii':
                charString += "\x0f"
                charset = 'ascii'
            if c in [0x22,0x25,0x5c]:
                charString += chr(0x5c)
            charString += chr(c)
    cmd = f"printf \"{addr}:{charString}\" | sudo /root/rpitx/pocsag -f 152650000 -r 1200 -b 3 -t 1"
    os.system(cmd)
    
addr = input("呼机地址:")
while True:
    os.system("clear")
    print("--------------------------------------------")
    print("    RPITX 寻呼发射台 MODE:POCSAG1200")
    print("--------------------------------------------")
    msg = input(f"ADDR:{addr}#")
    sendPocsag(addr,msg)

import base64

def encodeB64(payloadToEncode):
    return(base64.b64encode(bytes(payloadToEncode,"utf-8")))


def decodeB64(payloadToDecode):
    return(base64.b64decode(payloadToDecode).hex())


def LoRaUnpack(payload):

    binaryPayload = bin(int(payload, 16))[2:].zfill(len(payload) * 4)

    #SonicoNano LoRa Raw Frame
    payloadDict = {
        "Volume" : int(binaryPayload[0:30],2),
        "RemainingBatteryLifetime_Semester" : int(binaryPayload[30:35],2),
        "Meter Medium" : int(binaryPayload[35:37],2),
        "Volume Multiplier" : int(binaryPayload[37:41],2),
        "Meter Serial Number" : int(binaryPayload[41:68],2),
        "Water Temperature" : int(binaryPayload[68:75],2),
        "MET Alarm Malfunction" : bool(int(binaryPayload[75])),
        "MET Alarm Tampering" : bool(int(binaryPayload[76])),
        "MET Alarm Water Leak" : bool(int(binaryPayload[77])),
        "MET Alarm Water Burst" : bool(int(binaryPayload[78])),
        "MET Alarm Air in Pipe" : bool(int(binaryPayload[79])),
        "MET Alarm Empty Pipe" : bool(int(binaryPayload[80])),
        "MET Alarm Reverse Flow" : bool(int(binaryPayload[81])),
        "MET Alarm No Usage" : bool(int(binaryPayload[82])),
        "MET Alarm Battery Low Level" : bool(int(binaryPayload[83])),
        "MET Alarm Water Temperature" : bool(int(binaryPayload[84])),
        "MET Alarm Ambient Temperature" : bool(int(binaryPayload[85])),
        "COM MET Communication Error" : bool(int(binaryPayload[86])),
        "COM Internal Critical Error" : bool(int(binaryPayload[84]))
    }

    return payloadDict
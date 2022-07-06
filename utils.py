import base64

def encodeB64(payloadToEncode):
    return(base64.b64encode(bytes(payloadToEncode,"utf-8")))


def decodeB64(payloadToDecode):
    return(base64.b64decode(payloadToDecode).hex())


def LoRaUnpack(payload):

    #uzupełnianie zer po lewej stronie do pełnych bajtów
    binaryPayload = bin(int(payload, 16))[2:].zfill(len(payload) * 4)

    if len(binaryPayload) == 88:
        return LoRaUnpackRawFrame(binaryPayload)

    else:
        return LoRaUnpackOMSFrame(binaryPayload)


# SonicoNano LoRa Raw Frame
# q42/UgS4TosXIbY=
# FrameCounter 3
# 33420F0000000000906219

def LoRaUnpackRawFrame(binaryPayload):

    return  {
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


# SonicoNano LoRa OMS Frame
# YC5PQEoIcZv4N4OnIkMuqgRgGIX2GUlJ8ZeCLFWQKWY0fDurxI1ubbpcfz+6Gzk=
# FrameCounter 37
# 0411A15A993B441100000000426C244C02FD74000004FD17032C0004913C5E6F0100033933F9310259114202657D0B
def LoRaUnpackOMSFrame(binaryPayload):

    return {"xD" : "lol"}


def ParseDIF(DIFByte):
    pass


def ParseVIF(VIFByte):
    
    if VIFByte[0] == "1":
        isExtended = True
    
    if VIFByte[1:4] == "0010":
        print(coeff = 10 ** (int(VIFByte[5:7],2) - 6))

def ParseVIFE(VIFEByte):
    pass


ParseVIF("00010001")
import base64

def encode(payloadToEncode):
    return(base64.b64encode(bytes(payloadToEncode,"utf-8")))

def decode(payloadToDecode):
    return(base64.b64decode(payloadToDecode).decode("utf-8"))
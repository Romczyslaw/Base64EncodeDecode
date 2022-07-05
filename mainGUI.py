from cgitb import text
import tkinter as tk
import utils
from lora.crypto import loramac_decrypt 

func = utils.decodeB64


def Switch(value):

    global func

    if value == "0":
        btnConvert["text"] = "Decode"
        func = utils.decodeB64
        btnLoRa["state"] = tk.NORMAL

    else:
        btnConvert["text"] = "Encode"
        func = utils.encodeB64
        btnLoRa["state"] = tk.DISABLED


def HandleDecodeEncode():
    try:
        output = func(str(entInput.get())).upper()
            
        entOutput.delete(0,tk.END)
        entOutput.insert(0, output)

    except:
        pass


def HandleLoRaDecrypt():

    try:
        payloadEncryptedList = loramac_decrypt(entOutput.get(), int(entSeqNumber.get()), entAppSessionKey.get(), entDeviceAddress.get())

        payloadEncryptedHexString = ""

        for i in payloadEncryptedList:
            payloadEncryptedHexString += "{:02x}".format(i, "x")

        entOutputLoRa.delete(0, tk.END)
        entOutputLoRa.insert(0, payloadEncryptedHexString.upper())
        
        payloadDict = utils.LoRaUnpack(payloadEncryptedHexString)

        for key in payloadDict:
            txtLoRaUnpacked.insert(tk.END, f"{key} = {payloadDict[key]}\n")
    
    except:
        pass


window = tk.Tk()
window.title("LoRa Payload Encoder/Decoder")
window.columnconfigure(0, weight=1)

lblInput = tk.Label(master=window, text = "Input Data")
entInput = tk.Entry(master=window)
btnConvert = tk.Button(master=window, text="Decode", command=HandleDecodeEncode)
lblOutDecEnc = tk.Label(master=window, text = "Base 64 Decoded/Encoded")
entOutput = tk.Entry(master=window)
scSwitch = tk.Scale(master=window, length=50, from_=0, to=1, orient=tk.HORIZONTAL, showvalue=False, command=Switch)

lblAppSessionKey = tk.Label(master=window, text="App Session Key")
entAppSessionKey = tk.Entry(master=window)

frmAddSeq = tk.Frame(master=window)
lblDeviceAddress = tk.Label(master=frmAddSeq, text="Device Address")
entDeviceAddress = tk.Entry(master=frmAddSeq)
lblSeqNumber = tk.Label(master=frmAddSeq, text="Frame Counter")
entSeqNumber = tk.Entry(master=frmAddSeq)
btnLoRa = tk.Button(master=window, text="Parse Frame", command=HandleLoRaDecrypt)
entOutputLoRa = tk.Entry(master=window)
txtLoRaUnpacked = tk.Text(master=window)

lblInput.grid(row=0, column=0, sticky="ws", padx=5, pady=5)
entInput.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btnConvert.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
scSwitch.grid(row=2, column=1, sticky="ew", padx=5,pady=5)

lblOutDecEnc.grid(row=2, column=0, sticky="ws", padx=5, pady=5)
entOutput.grid(row=3, column=0, sticky="ew", padx=5,pady=5)

lblAppSessionKey.grid(row=4, column=0, sticky="ws", padx=5, pady=5)
entAppSessionKey.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

frmAddSeq.grid(row=6, column=0, sticky="ew", padx=5, pady=5)
lblDeviceAddress.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
entDeviceAddress.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
lblSeqNumber.grid(row=0, column=2, sticky="e", padx=5, pady=5)
entSeqNumber.grid(row=0, column=3, sticky="e", padx=5, pady=5)

entOutputLoRa.grid(row=8, column=0, sticky="ew", padx=5,pady=5)
btnLoRa.grid(row=8, column=1, sticky="ew", padx=5, pady=5)



txtLoRaUnpacked.grid(row=11, column=0, padx=5, pady=5)

entInput.focus()

window.mainloop()
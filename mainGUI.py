import tkinter as tk
from turtle import width
import pyperclip
import b64utils as b64

func = b64.decode

def HandleDecodeEncode(event):
    try:
        output = func(str(entInput.get()))
            
        pyperclip.copy(str(output))
        entOutput.delete(0,tk.END)
        entOutput.insert(0, output)

    except:
        pass


def Switch(value):

    global func

    if value == "0":
        btnConvert["text"] = "Decode"
        func = b64.decode

    else:
        btnConvert["text"] = "Encode"
        func = b64.encode


window = tk.Tk()
window.title("LoRa Payload Encoder/Decoder")
window.columnconfigure(0, weight=1, minsize=50)
window.rowconfigure(0, minsize=30)

entInput = tk.Entry(master=window)
btnConvert = tk.Button(master=window, text="Decode")
entOutput = tk.Entry(master=window)
scSwitch = tk.Scale(master=window, length=50, from_=0, to=1, orient=tk.HORIZONTAL, showvalue=False, command=Switch)
entInput.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btnConvert.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
entOutput.grid(row=1, column=0, sticky="ew", padx=5,pady=5)
scSwitch.grid(row=1, column=1, sticky="e", padx=5,pady=5)

btnConvert.bind("<Button-1>", HandleDecodeEncode)
entInput.focus()

window.mainloop()
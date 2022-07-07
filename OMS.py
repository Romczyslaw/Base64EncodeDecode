from pprint import pprint as pp

class OMSLoRaUplinkFrame():
    """
    Opakowanie danych sparsowanych przez obiekt klasy OMSFrame i połączenie z nazwą obiektu
    """

    def __init__(self, data):

        myFrame = OMSFrame(data)
        myFrame.ParserMachineState()

        self.listOfObjects = myFrame.GetListOfObjects()
        self.dictOfObjects = {}


    def getDictOfObjects(self):
        
        self.dictOfObjects.update(
            ([("Actual Volume", self.listOfObjects[0]),
            ("Accumulated Volume, Due Date", self.listOfObjects[1]),
            ("Local Date, Due Date", self.listOfObjects[2])]))

        self.dictOfObjects.update(self.listOfObjects[3])
        self.dictOfObjects.update(self.listOfObjects[4])
        self.dictOfObjects.update(self.listOfObjects[5])

        self.dictOfObjects.update(
            ([("Actual Flow", self.listOfObjects[6]),
            ("Actual Flow Temperature", self.listOfObjects[7]),
            ("External Temperature", self.listOfObjects[8])]))

        return self.dictOfObjects

    
    def PrintList(self):
        pp(self.dictOfObjects)


class OMSFrame():  
    """
    Założenia pracy klasy parsującej:
        - przy inicjalizacji obiektu klasy do atrybutu data trafia string z danymi w formie binarnej
        - brak DIFE (po DIF od razu idzie VIF)
        - mogą zdarzać się VIFE
        - z góry ustalone kodowania, i typy danych, jakie są przyjmowane
            - nie zrobiono pełnego parsowania, tylko to, co jest obecnie (06.07.22) zdefiniowane jako zawartość ramki LoRa OMS
        - na wyjściu daje listę obiektów "anonimowych" (oprócz tych, które są jasno określone i zdefiniowane przez VIFE)
    """

    def __init__(self, data):
        self.data = data

        self.coeff = 0
        self.tempCoeff = 0
        self.infoInVIFE = 0
        self.isDate = 0
        self.isVIFExtended = 0 
        self.length = 0
        self.objectKey = 0
        self.unit = 0
        self.toLittleEndian = 1
        
        self.listOfObjects = []


    def ParserMachineState(self):

        self.CutDataToBytes()

        while(len(self.listOfBytes) > 0):
            
            self.ParseDIF(self.listOfBytes.pop(0))
            self.ParseVIF(self.listOfBytes.pop(0))

            if self.isVIFExtended:
                self.ParseVIFE(self.listOfBytes.pop(0))

            self.ReadObjectValue()
            self.ClearAfterParse()

        #self.PrintList()
    
    def CutDataToBytes(self):
        #lista stringów 8-znakowych - dane w formie binarnej
        self.listOfBytes = [self.data[i:i+8] for i in range(0, len(self.data),8)]


    def ParseDIF(self, DIFByte):
        self.length = int(DIFByte[4:8], 2)


    def ParseVIF(self, VIFByte):
    
        if VIFByte[0] == "1":
            self.isVIFExtended = True
    
        if VIFByte[1:5] == "0010":
            self.coeff = 10 ** (int(VIFByte[5:8],2) - 6)
            self.unit = " m3"

        if VIFByte[1:8] == "1101100":
            self.isDate = True
            self.toLittleEndian = False

        if VIFByte[0:8] == "11111101":
            self.infoInVIFE = True

        if VIFByte[1:5] == "0111":
            self.coeff = 10 ** (int(VIFByte[5:8],2) - 6)
            self.unit = " m3/h"

        if VIFByte[1:6] == "10110":
            self.tempCoeff = 10 ** (int(VIFByte[6:8],2) - 3)
            self.unit = " ℃"
        
        if VIFByte[1:6] == "11001":
            self.tempCoeff = 10 ** (int(VIFByte[6:8],2) - 3)
            self.unit = " ℃"

        
    def ParseVIFE(self, VIFEByte):
        
        if VIFEByte[1:8] == "1110100":
            self.objectKey = "Remaining Battery Lifetime (days)"

        elif VIFEByte[1:8] == "0010111":
            self.objectKey = "Error Flags"

        elif VIFEByte[1:8] == "0111100":
            self.objectKey = "Actual Backflow Volume"


    def ReadObjectValue(self):

        obj = "".join(self.listOfBytes[:self.length])
        del self.listOfBytes[:self.length]

        if self.toLittleEndian:
            obj = self.ChangeByteOrder(obj, "little")

        if self.isVIFExtended and self.infoInVIFE:
            self.listOfObjects.append({self.objectKey : str(obj)})

        elif self.isVIFExtended and not self.infoInVIFE:
            self.listOfObjects.append({self.objectKey : str(obj * self.coeff) + self.unit})

        elif self.coeff:
            self.listOfObjects.append(str(obj * self.coeff) + self.unit)

        elif self.tempCoeff:
            self.listOfObjects.append(str(obj * self.tempCoeff) + self.unit)

        elif self.isDate:
            self.listOfObjects.append(self.ParseDate(obj))


    def ParseDate(self, dateInBits):
        
        year = "20" + (str(int(dateInBits[0:3] + dateInBits[8:12],2)))
        month = str(int(dateInBits[12:16],2))
        day = str(int(dateInBits[3:8],2))

        return "-".join([day, month, year])


    def ClearAfterParse(self):
        self.coeff = 0
        self.tempCoeff = 0
        self.infoInVIFE = 0
        self.isVIFExtended = 0
        self.isDate = 0
        self.length = 0
        self.objectKey = 0
        self.unit = 0
        self.toLittleEndian = 1


    def GetListOfObjects(self):
        return(self.listOfObjects)


    def ChangeByteOrder(self, obj, order):
        objToInt = int(obj, 2).to_bytes((len(obj) + 7) // 8, byteorder=order) 
        return int.from_bytes(objToInt,"big")


#x = OMSLoRaUplinkFrame('0000010000010001101000010101101010011001001110110100010000010001000000000000000000000000000000000100001001101100001001000100110000000010111111010111010000000000000000000000001111111101000101110000001100101100000000000000010010010001001111000101111001101111000000010000000000000011001110010011001111111001001100010000001001011001000100010100001000000010011001010111110100001011')
#x.getDictOfObjects()
#x.PrintList()
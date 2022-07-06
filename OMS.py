class OMSFrame():
    
    """
    Założenia pracy klasy parsującej:
        - przy inicjalizacji obiektu klasy do atrybutu data trafia string z danymi w formie binarnej
        - brak DIFE (po DIF od razu idzie VIF)
        - mogą zdarzać się VIFE
        - z góry ustalone kodowania, i typy danych, jakie są przyjmowane
            - nie zrobiono pełnego parsowania, tylko to, co jest obecnie (06.07.22) zdefiniowane jako zawartość ramki LoRa OMS
    """

    def __init__(self, data):
        self.data = data


    def ParserMachineState(self):

        self.CutDataToBytes()

        while(len(self.listOfBytes) > 0):
            
            self.ParseDIF(self.listOfBytes.pop())
            self.ParseVIF(self.listOfBytes.pop())

            if self.isVIFExtended:
                self.ParseVIFE(self.listOfBytes.pop())

            

            self.ClearAfterObject()

    
    def CutDataToBytes(self):
        #lista stringów 8-znakowych - dane w formie binarnej
        self.listOfBytes = [self.data[i:i+8] for i in range(0, len(self.data),8)]


    def ParseDIF(self, DIFByte):
        self.length = int(DIFByte[4:8])


    def ParseVIF(self, VIFByte):
    
        if VIFByte[0] == "1":
            self.isVIFExtended = True
    
        if VIFByte[1:5] == "0010":
            self.coeff = 10 ** (int(VIFByte[5:8],2) - 6)

        elif VIFByte[1:8] == "1101100":
            self.isDate = True

        elif VIFByte[0:8] == "11111101":
            self.infoInVIFE = True

        elif VIFByte[1:5] == "0111":
            self.coeff = 10 ** (int(VIFByte[5:8],2) - 6)

        elif VIFByte[1:6] == "10110":
            self.tempCoeff = 10 ** (int(VIFByte[6:8],2) - 3)
        
        elif VIFByte[1:6] == "11001":
            self.tempCoeff = 10 ** (int(VIFByte[6:8],2) - 3)

        
    def ParseVIFE(self, VIFEByte):
        
        if VIFEByte[1:8] == "1110100":
            self.objectKey = "Remaining Battery Lifetime (days)"

        elif VIFEByte[1:8] == "0010111":
            self.objectKey = "Error Flags"

    def ReadObjectValue(self):
        pass

    def ClearAfterObject(self):
        self.coeff = 0
        self.tempCoeff = 0
        self.infoInVIFE = 0
        self.isDate = 0
        self.isVIFExtended = 0 
        self.length = 0
        self.objectKey = 0
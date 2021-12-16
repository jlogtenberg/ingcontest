try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

class DocumentProcessor:

    def retrieveContractNumber(self, filename):
        ocrText = pytesseract \
            .image_to_string(Image.open(filename)) \
            .split('\n')
        _lineWithContractNumber, type = self.__findLineContractNumber(ocrText)
        _contractNumber =  self.__filterContractNumberFromLine(_lineWithContractNumber, type)
        return _contractNumber

    def __findLineContractNumber(self,stringList):
        print("fineLine")
        contract_types = ["contractn", "leningn", "ingn"]
        for line in stringList:
            for type in contract_types:
                if type in line.lower():
                    return line, type

        return "not found"

    def __filterContractNumberFromLine(self,line, type):
        contract_index = line.split()
        for i in range (len(contract_index)):
            if type in contract_index[i].lower():
                if contract_index[i + 1][0] == '0':
                    return contract_index[i + 1].replace("0", "O", 1)
                elif contract_index[i + 1][0] == '2' and len(contract_index) < 9:
                    return contract_index[i + 1].replace('2', 'Z', 1)
                return contract_index[i + 1].strip()
        return line
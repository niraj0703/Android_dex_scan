import binascii
import re
import string
class DexItem:
    def __init__(self):
        self.tag = "Abstract Item"
        self.offset = 0
        self.size = 0
        self.items = []

    def getItems(self):
        return self.items

    def printAllEls(self):
        #print(self.tag)
        #print("[ItemOffset] " + format(self.offset, '08X'))
        #print("[ItemSize]   " + format(self.size, '08X'))
        for i in range(len(self.items)):
            item = self.items[i]
            print (i, item)
            '''string_data = item
            string_data = re.sub(r'\d+', '', str(string_data))
            translator = str.maketrans('','', string.punctuation)
            string_data = string_data.translate(translator)
            string_data=string_data.strip()
            print(string_data)'''
            
            #print(binascii.hexlify(item))
            #print([elem.encode("hex") for elem in item])
            #print('################################################################################################')

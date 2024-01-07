import Dex
import re
import string
import pprint
import hashlib
import os

#RGB and Gray Scale generation of all dex files in given path and save it target with Hash code as name
target_path = "boqx_images/"
sample_dir_path = "Dex_files/boqx_dex_files/"
for root, dir, files in os.walk(sample_dir_path):
        for filename in files:
            sample_files_path = os.path.join(sample_dir_path, filename)
            dex = Dex.Dex(sample_files_path,target_path)          
#dex.getMethods().printAllEls()
#dex.print_dex_header()
#dex.read_header_bytes()
#dex.getStrings().printAllEls()


def stringFeatureFromdex(dex):
    str_data = dex.getStrings().getItems()
    data = []
    for string_data in str_data:    
        string_data = re.sub(r'\d+', '', str(string_data))
        translator = str.maketrans('','', string.punctuation)
        string_data = string_data.translate(translator)
        string_data = re.sub('b +','',string_data)
        string_data = re.sub('bn+','',string_data)
        string_data = re.sub(' +','',string_data)
        string_data = re.sub('^b','',string_data)
        string_data = re.sub('^Landroidx','',string_data)
        string_data = re.sub('^Landroid','',string_data)
        string_data = re.sub('^Lcomgoogleandroid','',string_data)
    
        
        string_data = re.sub(r'\d+', '', str(string_data))
        translator = str.maketrans('','', string.punctuation)
        string_data = string_data.translate(translator)

        data.append(string_data)
    #print(len(data))
    plain_text_dict = {}
    for l_string in data:
        if((l_string is not "") and (len(l_string) > 1)):
            words = l_string.split()
            for word in words:
                value_t = plain_text_dict.get(word)
                if(value_t is not None):
                    plain_text_dict[word] = value_t+1
                else:
                    plain_text_dict.setdefault(word, 1)
    #print(plain_text_dict)
    print("#############Frequencies Greater than 1 #################")
    md5_dict={}
    plain_text_dict_keys = plain_text_dict.keys()

    for k in plain_text_dict_keys:
        #print(k)   
        key_md5 = hashlib.md5(str(k).encode('utf-8'))
        key_md5_byte = key_md5.digest()
        key_md5 = key_md5.hexdigest()


        as_int = ''
        for by in key_md5_byte:
            a = format(by,'#010b')[2:]
            as_int = as_int+a
        #as_int = int(key_md5, 16)
        #as_int = bin(as_int)
        #print(as_int)

        md5_dict[as_int]=plain_text_dict[k]
        #print(len(as_int))
        
        #break

    #print(md5_dict)

    md5_dict_keys = md5_dict.keys()

    sum_list = []
    for i in range(128):
        sum = 0
        for j in md5_dict_keys:
            if j[i] == '1':
                sum = sum + md5_dict[j]
            else:
                sum = sum - md5_dict[j]
        sum_list.append(sum)
            #break
            
        #break
    print(sum_list)

    #print( [md5_dict[i] for i in plain_text_dict_keys if md5_dict[i] > 2])
    #print("#############Frequencies Greater than 1 #################")
    #print( [plain_text_dict[i] for i in plain_text_dict if plain_text_dict[i] > 2])

    #dex.getTypes().printAllEls()
    '''dex.getProtos().printAllEls()
    dex.getFields().printAllEls()
    dex.getMethods().printAllEls()
    dex.getClassDefs().printAllEls()

    classes = dex.getClasses()
    for i in range(len(classes)):
        item = classes[i]
        print( "[#%d] Class" % i)
        item.printAllEl()'''

import subprocess
import os
import sys
import hashlib


def dexfile_md5_calculate(filename):
    md5_hash = hashlib.md5()
    a_file = open(filename, "rb")
    content = a_file.read()
    md5_hash.update(content)

    return (md5_hash.hexdigest())

def get_dexdump(filename):
    md5_str = str(dexfile_md5_calculate(filename))
    print(md5_str)
    args = ("/usr/lib/android-sdk/build-tools/debian/dexdump", "-l", "xml", "-o", md5_str + ".xml", filename )
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    return md5_str +".xml"
    #output = popen.stdout.read()
    #print (output)

def clean_surrogate_escapes(s):
    #return s.encode('utf-16', 'sgsh').decode('utf-16', 'replace')
    return s.encode('utf-16', 'xmlcharrefreplace').decode('utf-16')

import xml.etree.ElementTree as ET
import codecs

def read_variable_from_dexdump(dexdump_xml):
    #dexdump_xml = clean_surrogate_escapes(dexdump_xml)
    #print("1#####")
    #parser = etree.XMLParser(recover=True)
    #with open(dexdump_xml, 'r') as utf8_file:
    #    xml_tree = ET.parse(utf8_file)
    xml_tree = ET.parse(dexdump_xml)
    print("#####")
    root = xml_tree.getroot()
    count = 0
    for element in root:
        count= count +1
        if (count > 5):
            break
        for subelement in element:            
            print(subelement.attrib)

class_name = "classes2.dex"
xml_name = get_dexdump(class_name)
with open(xml_name, 'rb') as f:
     lines = [l.decode('utf8', 'ignore') for l in f.readlines()]
#with open(xml_name, 'w') as out:
    out.writelines(lines)
print("2$$$$$$")
#xml_name = dexfile_md5_calculate("classes2.dex")
read_variable_from_dexdump(xml_name)
#xml_file = open(xml_name, 'r')
#xml_content = xml_file.read()
#xml_content = xml_content.decode('unicode_escape').encode('utf-8')
#xml_content = unicode(xml_content, errors='replace')
#xml_content = lines.split("class #")
print(lines[115512])
#xml_file.close()


import os
import struct
import hashlib
import zlib
from StringItems import StringItems
from TypeItems import TypeItems
from ProtoItems import ProtoItems
from FieldItems import FieldItems
from MethodItems import MethodItems
from ClassDefItems import ClassDefItems
from collections import namedtuple
from Clazz import Clazz
import binascii
from DexTypeHelper import DexTypeHelper
import math
from PIL import Image
#import gabor_filter

class Dex:

    DexHeader = namedtuple("DexHeader", "magic checksum signature file_size header_size endian_tag link_size " +
                           "link_off map_off string_ids_size string_ids_off type_ids_size type_ids_off " +
                           "proto_ids_size proto_ids_off field_ids_size field_ids_off method_ids_size " +
                           "method_ids_off class_defs_size class_defs_off data_size data_off")

    def __init__(self, dex_file_path,target_path):
        dex_file = open(dex_file_path, 'rb')        
        self.mm = dex_file.read() 
        self.target_path =  target_path      
        self.final_pixel = []
        dex_file.close()
        self.classes = []
        self.parse_dex_header()
        self.parse_dex_parts()
        

    def parse_dex_header(self):
        magic = self.mm[0:8]                
        checksum = struct.unpack('<L', self.mm[8:0xC])[0]
        signature = self.mm[0xC:0x20]
        file_size = struct.unpack('<L', self.mm[0x20:0x24])[0]
        header_size = struct.unpack('<L', self.mm[0x24:0x28])[0]
        endian_tag = struct.unpack('<L', self.mm[0x28:0x2C])[0]
        link_size = struct.unpack('<L', self.mm[0x2C:0x30])[0]
        link_off = struct.unpack('<L', self.mm[0x30:0x34])[0]
        map_off = struct.unpack('<L', self.mm[0x34:0x38])[0]
        string_ids_size = struct.unpack('<L', self.mm[0x38:0x3C])[0]
        string_ids_off = struct.unpack('<L', self.mm[0x3C:0x40])[0]
        type_ids_size = struct.unpack('<L', self.mm[0x40:0x44])[0]
        type_ids_off = struct.unpack('<L', self.mm[0x44:0x48])[0]
        proto_ids_size = struct.unpack('<L', self.mm[0x48:0x4C])[0]
        proto_ids_off = struct.unpack('<L', self.mm[0x4C:0x50])[0]
        field_ids_size = struct.unpack('<L', self.mm[0x50:0x54])[0]
        field_ids_off = struct.unpack('<L', self.mm[0x54:0x58])[0]
        method_ids_size = struct.unpack('<L', self.mm[0x58:0x5C])[0]
        method_ids_off = struct.unpack('<L', self.mm[0x5C:0x60])[0]
        class_defs_size = struct.unpack('<L', self.mm[0x60:0x64])[0]
        class_defs_off = struct.unpack('<L', self.mm[0x64:0x68])[0]
        data_size = struct.unpack('<L', self.mm[0x68:0x6C])[0]
        data_off = struct.unpack('<L', self.mm[0x6C:0x70])[0]
       
        #newfunction copied from here
        self.newFunction( string_ids_size, string_ids_off, 
                        file_size, 
                        type_ids_size, type_ids_off,
                        proto_ids_size, proto_ids_off,
                        field_ids_size, field_ids_off,
                        method_ids_size, method_ids_off,
                        class_defs_size, class_defs_off,
                        data_size, data_off)
        if len(self.mm) != file_size:
            print ("ERROR")

        self.dexHeader = self.DexHeader(magic, checksum, signature, file_size, header_size, endian_tag, link_size,
                                        link_off, map_off, string_ids_size, string_ids_off, type_ids_size, type_ids_off,
                                        proto_ids_size, proto_ids_off, field_ids_size, field_ids_off, method_ids_size,
                                        method_ids_off, class_defs_size, class_defs_off, data_size, data_off)

    
    def newFunction(self, string_ids_size, string_ids_off, file_size, type_ids_size, type_ids_off,
                        proto_ids_size, proto_ids_off,
                        field_ids_size, field_ids_off,
                        method_ids_size, method_ids_off,
                        class_defs_size, class_defs_off,
                        data_size, data_off ):
    
        file_hash =  hashlib.md5(self.mm).hexdigest()
        print(file_hash)
        RGB_name = os.path.join(self.target_path, file_hash +"_rgb.png")
        Gray_scale_name = os.path.join(self.target_path, file_hash +"_gray.png")

        if os.path.exists(RGB_name):
            return
        string_id_data = []
        for idx in range(string_ids_size):
            string_id_data.append(hex(struct.unpack('<B', self.mm[string_ids_off+idx:string_ids_off+idx + 1])[0]))
        
        str_rgb_data = self.rgb_clc(string_id_data,file_size)
        self.final_pix(str_rgb_data)
              
        type_id_data = []
        for idx in range(type_ids_size):
            type_id_data.append(hex(struct.unpack('<B', self.mm[type_ids_off+idx:type_ids_off+idx + 1])[0]))
        
        type_id_rgb_data = self.rgb_clc(type_id_data,file_size)
        self.final_pix(type_id_rgb_data)
        

        proto_ids_data = []
        for idx in range(proto_ids_size):
            proto_ids_data.append(hex(struct.unpack('<B', self.mm[proto_ids_off+idx:proto_ids_off+idx + 1])[0]))
        
        proto_rgb_data = self.rgb_clc(proto_ids_data,file_size)
        self.final_pix(proto_rgb_data)

        field_ids_data = []
        for idx in range(field_ids_size):
            field_ids_data.append(hex(struct.unpack('<B', self.mm[field_ids_off+idx:field_ids_off+idx + 1])[0]))
        
        field_rgb_data = self.rgb_clc(field_ids_data,file_size)
        self.final_pix(field_rgb_data)        

        method_ids_data = []
        for idx in range(method_ids_size):
            method_ids_data.append(hex(struct.unpack('<B', self.mm[method_ids_off+idx:method_ids_off+idx + 1])[0]))
        
        method_rgb_data = self.rgb_clc(method_ids_data,file_size)
        self.final_pix(method_rgb_data)

        class_defs_data = []
        for idx in range(class_defs_size):
            class_defs_data.append(hex(struct.unpack('<B', self.mm[class_defs_off+idx:class_defs_off+idx + 1])[0]))
        
        class_rgb_data = self.rgb_clc(class_defs_data,file_size)
        self.final_pix(class_rgb_data)

        data_data = []
        for idx in range(data_size):
            data_data.append(hex(struct.unpack('<B', self.mm[data_off+idx:data_off+idx + 1])[0]))
        
        data_rgb_data = self.rgb_clc(data_data,file_size)
        self.final_pix(data_rgb_data)  


        
        print(RGB_name,Gray_scale_name)
        #print(self.final_pixel)

        self.calc_image(self.final_pixel, RGB_name, Gray_scale_name)


    def final_pix(self,data):
        for idx in data:
            self.final_pixel.append(idx)


    def calc_image(self, rgb_data, RGB_name, Gray_scale_name): 
        print(len(rgb_data)/1024)
        im = Image.new('RGB',(1024,int(len(rgb_data)/1024)))
        im.putdata(rgb_data)
        im.save(RGB_name)
        img = Image.open(RGB_name).convert('LA')
        img.save(Gray_scale_name)
        #print(RGB_name, Gray_scale_name)
    
    def rgb_clc(self,data,file_size):
        pixel = []
        data_chunks = self.chunks(data,1024) 
        s_entr = self.entopy_of_section(data)
        r_channel = (((float(s_entr) * float(s_entr)) % 8) * 255/8)
        data_size = len(data)
        b_channel = ((float(data_size))/file_size)*255
        for item in data_chunks:
            for idx in item:
                pixel.append((int(r_channel),int(idx, 16),int(b_channel )))
        
        return pixel


    def chunks(self,lst,n):
        return_list = []
        for i in range(0,len(lst),n):            
            return_list.append(lst[i:i+n])       
        last_el_ln = len(return_list[-1])
        new_lst = return_list[-1]        
        pad_ln = n - last_el_ln
        if pad_ln > 0:
            for i in range(pad_ln):
                new_lst.append(hex(0))        
        del return_list[-1]
        return_list.append(new_lst)       
        return return_list

    '''def frequency_of_byte(self,lst):
        freq_lst = []
        for item in lst:
            f_lst = []
            p_lst = []
            log_lst = []
            for idx in item:
                f_lst.append(item.count(idx))
            f_lst_ln = len(f_lst)
            for idx in f_lst:
                p_lst.append(float(idx)/f_lst_ln)
            
            print(p_lst)
            freq_lst.append(f_lst)
        return freq_lst'''

    def entopy_of_section(self,lst):
        ent = 0
        for idx in range(256):
            p = float(lst.count(hex(idx)))/len(lst)
            if p > 0:
                ent = ent+p*math.log(p,2)
        return ent
     
    def print_dex_header(self):
        print (self.dexHeader)

    def read_header_bytes(self):
        string_ids_off = 0
        header_size = self.dexHeader.header_size
        for idx in range(header_size):
            off = struct.unpack('<L', self.mm[string_ids_off + (idx * 4):string_ids_off + (idx * 4) + 4])[0]
            utf16_size = (DexTypeHelper.readUnsignedLEB128(self.mm, off))
            if utf16_size <= 0:
                c_char = " "
            else:
                utf16_size_len = DexTypeHelper.CalcDecUnsignedLEB128(utf16_size)
                c_char = self.mm[off + utf16_size_len:off + utf16_size_len + utf16_size]
            print(c_char)

    def parse_dex_parts(self):
        self.string_id_list()
        self.type_id_list()
        self.proto_id_list()
        self.field_id_list()
        self.method_id_list()
        self.class_def_list()
        self.class_data_item()

    def string_id_list(self):
        self.strings = StringItems()
        self.strings.string_id_list(self.mm, self.dexHeader)

    def type_id_list(self):
        self.types = TypeItems()
        self.types.type_id_list(self.mm, self.dexHeader)

    def proto_id_list(self):
        self.protos = ProtoItems()
        self.protos.proto_id_list(self.mm, self.dexHeader)

    def field_id_list(self) :
        self.fields = FieldItems()
        self.fields.field_id_list(self.mm, self.dexHeader)

    def method_id_list(self):
        self.methods = MethodItems()
        self.methods.method_id_list(self.mm, self.dexHeader)

    def class_def_list(self) :
        self.classDefs = ClassDefItems()
        self.classDefs.class_def_list(self.mm, self.dexHeader)

    def class_data_item(self):
        for i in range(self.classDefs.size):
            clazz = Clazz(self.mm, self.classDefs.items[i])
            self.classes.append(clazz)

    def calcSignature(self):
        '''hash = hashlib.sha1()'''
        return hashlib.sha1(self.mm[32:len(self.mm)+1])

    def calcChecksum(self):
        zlib.adler32(self.mm[12:len(self.mm)+1])

    def getStrings(self):
        return self.strings

    def getTypes(self):
        return self.types

    def getProtos(self):
        return self.protos

    def getFields(self):
        return self.fields

    def getMethods(self):
        return self.methods

    def getClassDefs(self):
        return self.classDefs

    def getClasses(self):
        return self.classes

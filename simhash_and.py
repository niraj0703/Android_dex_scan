import simhash
import os
import pprint
import subprocess
#strings_from_app = os.system('strings classes2.dex')
ps = subprocess.run(["strings", "classes2.dex"], stdout=subprocess.PIPE)
#strings_from_app = stream.read()
strings_from_app = ps.stdout.decode()
strings_from_app = "hello\n niraj\n hello\n niraj"
strings_from_app = strings_from_app.splitlines()
#strings_from_app = "hello\n niraj\n hello\n niraj"
#print(strings_from_app[len(strings_from_app) -1])
plain_text = {}
for l_string in strings_from_app:
    temp_str = ""
    #print(l_string)
    for char in l_string:        
        if((ord(char) in range(65,90)) or (ord(char) in range(97,122))):
            temp_str += char
            #print(char)
    #print(temp_str)
    if(temp_str is not ""):
        value_t = plain_text.get(temp_str)
        if(value_t is not None):
            plain_text[temp_str] = value_t+1
        else:
            plain_text.setdefault(temp_str, 1)
          
print(plain_text)


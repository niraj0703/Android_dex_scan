temp_str = "7}7E"
temp_str2 = ""
for char in temp_str:        
    if((ord(char) in range(65,90)) or (ord(char) in range(97,122))):
        temp_str2 += char
print(temp_str2)
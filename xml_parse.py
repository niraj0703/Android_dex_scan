from bs4 import BeautifulSoup as bs
import lxml
with open("text.xml", encoding="latin-1") as fd:
    mystr = fd.read()
 
soup = bs(mystr, "lxml-xml")
f_list = soup.find_all('package')

src_list = [x for x in f_list if "com.src" in x.get("name")]
#print([x in src_li])
for x in src_list:
    class_list = x.find_all("class")
    #print(class_list)
    for item in class_list:
        print(item.get("name"))
#print(src_list[0].children)
# for x in src_list[0].children:
#     print(x.contents)


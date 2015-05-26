# -*- coding: utf-8 -*-
from ghost import Ghost
import codecs

ghost = Ghost()
page, resources = ghost.open('http://www2.ndmctsgh.edu.tw/PatientNo/PatientNoWeb.aspx')
webpage = [unicode(page.content,"utf-8")] 

action = "document.getElementById('rbPOS_1').click();"
page, resources = ghost.evaluate(action, expect_loading=True)
webpage.append(unicode(page.content,"utf-8"))

hospital = (u"內湖",u"汀州")

for num,hos in enumerate(hospital):
    with codecs.open(hos + ".txt", "w", "utf-8") as output:
        output.write(webpage[num])
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import codecs
import json
import time
from threading import Timer
import MySQLdb
from ghost import Ghost

def TGH():
    for second in range(1):

        db = MySQLdb.connect("localhost","root","1991yuyanlo","project_database",charset="utf8" )
        cursor = db.cursor()
        cursor.execute("SELECT VERSION()")
        data = cursor.fetchone()
        print "Database version : %s " % data

        ghost = Ghost()
        page, resources = ghost.open('http://www2.ndmctsgh.edu.tw/PatientNo/PatientNoWeb.aspx')
        webpage = [unicode(page.content,"utf-8")]

        action = "document.getElementById('rbPOS_1').click();"
        page, resources = ghost.evaluate(action, expect_loading=True)
        webpage.append(unicode(page.content,"utf-8"))

        hospital = ("TGH_b1","TGH_b2")

        for num,hos in enumerate(hospital):
            #rFile1 = codecs.open(hos+'.html', 'r')
            with codecs.open(hos + ".html", "w", "utf-8") as output:
                #output.write(webpage[num])
                xmlContent = webpage[num].encode('utf8')

                print xmlContent

                local_file = codecs.open('TGH_results.txt', 'w')
                soup=BeautifulSoup(xmlContent,"lxml")
                print soup.findAll('table',{'id':'GridView1'})

                for article in soup.findAll("table",{"id":"GridView1"}):
                    trIter = iter(article.findAll("tr"))
                    first = next(trIter)
                    firstCol = []

                    for th in first.findAll("th"):
                        firstCol.append(th.contents[0].encode('utf-8'))
                        print th.contents[0].encode('utf-8')

                    for tr in first.findAll("td",{"colspan":"5"}):
                        if tr.findChildren():
                            children = tr.findChildren()
                            for child in children:
                                print child.text
                                local_file.write(child.text)
                        else:
                            print tr.contents[0].encode('utf-8')
                            local_file.write(tr.contents[0].text.encode('utf-8'))

                    for tr in trIter:
                        for counter, td in enumerate(tr.findAll("td")):
                            output = firstCol[counter] + " : "  + td.contents[0].encode('utf-8')
                            print(json.dumps(output).strip('"'))
                            local_file.write(json.dumps("'"+td.contents[0].encode('utf-8')+"',").strip('"'))
                        print '\n'
                        local_file.write('\n')

                    local_file.close()
            #rFile1.close()

        truncateSQL = "truncate table tgh"
        try:
            cursor.execute(truncateSQL)
            db.commit()
        except:
            db.rollback()

        docf = open('TGH_results.txt','r')
        lines = docf.readlines()

        for index in range(0,len(lines)):
            print lines[index].strip(lines[index][-2:])
            v = lines[index].strip(lines[index][-2:])
            if not len(lines[index])==1:
                sql = "INSERT INTO `tgh`(`dept`, `pos`, `doc`, `current`, `branch`) VALUES (%s)"% v
                try:
                    cursor.execute(sql)
                    db.commit()
                    print sql
                    print 'db.commit()'
                except:
                    db.rollback()
                    print 'db.rollback()'
            else:
                continue

        docf.close()
        db.close()
    time.sleep(5)
    TGH()

Timer(5,TGH,()).start()


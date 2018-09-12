# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:35:42 2017
Modified on Wed Sep 12 2018

@author: Jasmine.Jia, Chris.Wang
"""

from random import randint
import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://www.baidu.com/')


def find_contact(fname, sname, company, sleepTime, browser):
    # Linkedin URL
    query = "https://www.linkedin.com/search/results/index/?keywords="+"TEMPFIRSTNAME"+"%20"+"TEMPLASTNAME"+"%20"+"TEMPCOMPANY"+"&origin=GLOBAL_SEARCH_HEADER"
    query = query.replace('TEMPFIRSTNAME', fname).replace('TEMPLASTNAME', sname).replace('TEMPCOMPANY', company)
    browser.get(query)
    time.sleep(5)
    source = browser.page_source
    # print(str(source))
    # Write file
    file = open("newQueries/"+fname+'.'+sname+'.html', "w+")
    file.write(str(source.encode('utf-8').strip()))
    file.close()

    try:
        chunks = source.split('<ul class="search-results__list list-style-none mt2">')[1].split('</ul>')[0]
        urls = []
        for j in chunks.split('href="/in/')[1:]:
            urlChunk = j.split('/"')[0]
            url = 'https://www.linkedin.com/in/' + urlChunk + '/'
            urls.append(url)

        download_page(urls[0], fname+'.'+sname, sleepTime, browser)
        print('This place is executed')
    except:
        print('No profile found')
        time.sleep(20)
        file = open('newFailedScrapes.csv', 'a')
        file.write(fname + ',' + sname + ',' + company + '\n')
        file.close()
        pass


def download_page(link, sname, sleepTime, browser):
    browser.get(link)
    browser.maximize_window()
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('scrolled')
    browser.find_element_by_class_name('pv-skills-section__chevron-icon').click()
    browser.find_element_by_class_name('pv-profile-section__toggle-detail-icon').click()# all the stuff that user liked and shared
    browser.find_elements_by_class_name('pv-profile-section__toggle-detail-icon')[4].click() # languages
    browser.find_element_by_class_name('pv-accomplishment-entity__title').click()

    print('Pausing for ' + str(sleepTime) + ' seconds.')
    time.sleep(sleepTime)
    temp = browser.page_source
    html_file = open("newProfiles/"+str(sname)+'.html', "w")
    html_file.write(temp.encode('utf-8').strip())
    html_file.close()


if __name__ == "__main__":
    browser.get('http://www.linkedin.com')
    time.sleep(60)

    print('browser opeded')

    with open('newClientsRogers.csv', 'r') as myfile:
        data = myfile.read()
    f = open('newFailedScrapes.csv', 'w')
    f.write('firstName,lastName,company'+'\n')
    f.close()

    print('This is the start')

    for i in data.split('\n')[1:]:
        if len(i) > 5:
            fname = i.split(',')[0]
            sname = i.split(',')[1]
            company = i.split(',')[2]
            delaytime = 30+randint(0,30)
            print("Looking for: " + fname + ' ' + sname)
            try:
                find_contact(fname, sname, company, delaytime, browser)
                print('Archived')
            except Exception as e:
                print(str(e))
            print(' ')

    print('this is end')

    browser.quit()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import glob
import sexmachine.detector as gender
d = gender.Detector()

files = glob.glob("*.html")

# # GET LIST OF <h3> TAGS
# def get_h3s(filename,h3_list):
#     # print filename
#     with open(file, 'r') as myfile:
#         data=myfile.read()
#
#     h3s = data.split('<h3>')
#
#     for i in h3s[3:]:
#         try:
#             h3 = i.split('</h3>')[0]
#             if 'People Also Viewed' not in h3:
#                 if 'In Common with' not in h3:
#                     if 'People Similar to' not in h3:
#                         if "How You" not in h3:
#                             # print "<h3>" + h3 + "</h3>"
#                             h3_list.append(h3)
#         except:
#             pass
#     return(h3)
#
# h3 = []
#
# for file in files:
#     get_h3s(file,h3)
#
# for i in set(h3):
#     if '<' not in i:
#         print i


# EXTRACT INFO FROM EDUCATION TAG
def extract_education(filename):
    fname = filename.split('.')[0]
    sname = filename.split('.')[1].split('.html')[0]
    gender = d.get_gender(fname).encode()
    with open(filename, 'r') as myfile:
        data=myfile.read()
    try:
        block_education = data.split('<h3>Education</h3>')[1].split('<h3>')[0]
        degree = '?'
        date1 = '?'
        date2 = '?'
        for i in block_education.split('<a title="More details for this school"'):
            try:
                school = i.split('school-name">')[1].split('</a>')[0]

                try:
                    degree = i.split('"degree">')[1].split('</span')[0]
                except: pass
                try:
                    date1 = i.split('<span class="education-date"><time>')[1].split('</time>')[0]
                except: pass
                try:
                    date2 = i.split('</time><time> – ')[1].split('</time>')[0]
                except: pass
                line = gender +','+fname +','+ sname +','+ school.replace(',','').rstrip() +','+ degree.replace(',','').rstrip() +','+ date1 +','+ date2
                print(line)
                f = open('education.csv','a')
                f.write(line+'\n')
                f.close()
            except: pass
    except:
        pass

# EXTRACT INFO FROM SKILLS TAG
def extract_skills(filename):
    fname = filename.split('.')[0]
    sname = filename.split('.')[1].split('.html')[0]
    gender = d.get_gender(fname).encode()
    with open(filename, 'r') as myfile:
        data=myfile.read()
    try:
        for skill in data.split('<div class="pv-skill-entity__header">')[1:]:
            tempSkill = skill.split('class="tooltip">')[1].split('</div>')[0].strip()
            line = gender +','+ fname + ','+ sname + ',' + tempSkill
            print(line)
            f = open('skills.csv','a')
            f.write(line+'\n')
            f.close()
    except:
        pass

# EXTRACT INFO FROM EXPERIENCE TAG
def extract_experience(filename):
    fname = filename.split('.')[0]
    sname = filename.split('.')[1].split('.html')[0]
    gender = d.get_gender(fname).encode()
    line = fname + ','+ sname
    with open(filename, 'r') as myfile:
        data=myfile.read()
    try:
        block_experience = data.split('<h3>Experience</h3>')[1].split('<h3')[0]
        for i in block_experience.split('<a title="Learn more about this title"')[1:]:
            title = '?'
            company = '?'
            location = '?'
            start ='?'
            title = i.split('mprofile_title">')[1].split('</a>')[0].replace(',',' and')
            company = i.split('company-name">')[1].split('</a>')[0].replace(',','').rstrip()
            try:
                start = i.split('-locale"><time>')[1].split('</time>')[0]
                start = re.sub("[^0-9]", "", start)
            except: pass
            try:
                location = i.split('"locality">')[1].split('</span>')[0].replace(',','').rstrip()
            except: pass
            line = gender +','+ fname + ','+ sname
            line = line +','+title+','+company+','+location+','+start
            print(line)
            f = open('experience.csv','a')
            f.write(line+'\n')
            f.close()
    except:
        pass


# EXTRACT INFO FROM LANGUAGE TAG
def extract_language(filename):
    with open(filename, 'r') as myfile:
        data=myfile.read()
    try:
        title = data.split('<title>')[1].split('|')[0]

        for lang in data.split('>Language name</span>')[1:]:
            foundLang = lang.split('</h4>')[0].strip()
            if len(foundLang) > 2:
                line = '"' + title + '"'
                line = line +','+foundLang
                line = line.replace(',,',',').replace(', ,',',').replace(',  ,',',')
                print(line)
                f = open('language.csv','a')
                f.write(line+'\n')
                f.close()

    except Exception as e: print(str(e))


# EXTRACT INFO FROM VOLUNTEER EXPERIENCE TAG
def extract_volunteer(filename):
    fname = filename.split('.')[0]
    sname = filename.split('.')[1].split('.html')[0]
    gender = d.get_gender(fname).encode()
    line = fname + ','+ sname
    with open(filename, 'r') as myfile:
        data=myfile.read()
    try:
        block_volunteer = data.split('<h3>Volunteer Experience &amp; Causes</h3>')[1].split('<h3')[0]
        for i in block_volunteer.split('vol_exp-org_name">')[1:]:
            volunteer_org = i.split('</a>')[0]
            if 'lazy-load' not in volunteer_org:
                line = gender +','+ fname + ','+ sname +','+ volunteer_org.replace(',','')
                print(line)
                f = open('volunteer.csv','a')
                f.write(line+'\n')
                f.close()
    except:
        pass


# EXTRACT INFO FROM FOLLOWING TAG
def extract_following(filename):
    with open(filename, 'r') as myfile:
        data=myfile.read()
    try:
        fname = data.split('{"firstName":"')[1].split('",')[0]
        sname = data.split('{"lastName":"')[1].split('",')[0]
        gender = d.get_gender(fname).encode()

        temp = data.split('<div id="following-container">')[1]
        block_following = temp.split('<h2>Following</h2>')[1].split('<script type="text/javascript">')[0]
        for i in block_following.split('"auto">')[1:]:
            follow = i.split('</strong')[0]
            if 'span>' not in follow:
                line = gender +','+ fname + ','+ sname +','+ follow.replace(',','')
                print(line)
                f = open('follow.csv','a')
                f.write(line+'\n')
                f.close()
    except Exception as e: print(str(e))

# EXTRACT INFO FROM GROUPS TAG
def extract_groups(filename):
    fname = filename.split('.')[0]
    sname = filename.split('.')[1].split('.html')[0]
    gender = d.get_gender(fname).encode()
    with open(filename, 'r') as myfile:
        data=myfile.read()
    try:
        temp = data.split('<div id="groups-container">')[1].split('<div id="following-container">')[0]
        for i in temp.split('<strong>')[1:]:
            group = i.split('</strong>')[0]
            line = gender +','+ fname + ','+ sname +','+ group.replace(',','')
            print(line)
            f = open('group.csv','a')
            f.write(line+'\n')
            f.close()
    except:
        pass

# EXTRACT INFO FROM INDUSTRY TAG
def extract_industry(filename):
    with open(filename, 'r') as myfile:
        data=myfile.read()
    try:
        title = data.split('<title>')[1].split('|')[0]

        industry = '?'
        try:
            industry = data.split('"industryName":"')[1].split('","')[0]
        except: pass
        line = '"'+ title + '",' + industry.replace(',','')
        print(line)
        f = open('industry.csv','a')
        f.write(line+'\n')
        f.close()
    except Exception as e: print(str(e))


#
# f = open('education.csv','w')
# f.write('gender,firstName,lastName,school,degree,start,finish'+'\n')
# f.close()
#
# f = open('experience.csv','w')
# f.write('gender,firstName,lastName,position,company,location,start'+'\n')
# f.close()
#
# f = open('follow.csv','w')
# f.write('gender,firstName,lastName,follow'+'\n')
# f.close()
#
# f = open('group.csv','w')
# f.write('gender,firstName,lastName,group'+'\n')
# f.close()
#
# f = open('language.csv','w')
# f.write('gender,firstName,lastName,language'+'\n')
# f.close()
#
# f = open('skills.csv','w')
# f.write('gender,firstName,lastName,skill'+'\n')
# f.close()
#
# f = open('volunteer.csv','w')
# f.write('gender,firstName,lastName,volunteer'+'\n')
# f.close()
#
# f = open('industry.csv','w')
# f.write('gender,firstName,lastName,industry'+'\n')
# f.close()


for i in files:
    extract_industry(i)
#     extract_skills(i)
    # extract_language(i)

#     extract_groups(i)
#     extract_following(i)
#     extract_volunteer(i)
#     extract_education(i)
#     extract_experience(i)




# i = '1.html'
# extract_industry(i)
# extract_skills(i)
# extract_language(i)

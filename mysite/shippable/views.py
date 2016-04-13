from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
import time
from datetime import datetime, date
import calendar
import datetime as dt
import re
from glob import glob

proxies = {
    "http": r"http://USERNAME:PASSWORD@IP:PORT",
    "https": r"http://USERNAME:PASSWORD@IP:PORT",
}


class Struct:
    def __init__ (self, *argv, **argd):
        if len(argd):
            # Update by dictionary
            self.__dict__.update (argd)
        else:
            # Update by position
            attrs = filter (lambda x: x[0:7] != "__", dir(self))
            for n in range(len(argv)):
                setattr(self, attrs[n], argv[n])


class Post(Struct):
    title=""
    post_id=""
    user=""
    created_at=""
    updated_at=""
    comments=0
    body=""
    url=""
    
def index(request):
    return render(request,'shippable/home.html')

def process(request):
        first=[]
        second=[]
        third=[]
        fourth=[]
        noOfOpenIssues=0
        noOfOpenIssuesInLast24hr = 0
        noOfOpenIssuesMoreThan24hLessThan7d = 0
        noOfOpenIssuesMoreThan7d = 0
        instancelist = []
        search_id=request.POST.get('textfield',None)
        repositoryName=request.POST.get('textfield2',None)
        accesstoken=request.POST.get('textfield3',None)
        #"cdd25761e5458bf25f257f4164f40a7a5e8d7422"
        url="https://api.github.com/repos/"+search_id+"/"+repositoryName+"?access_token="+str(accesstoken)
        #https://api.github.com/repos/shippable/support
        response = requests.get(url)
        data2 = json.loads(response.content)
        open_issue = data2['open_issues']
        j=0
        delimiters='-:TZ '
        regexPattern = '|'.join(map(re.escape, delimiters))
        noOfOpenIssues=open_issue
        
        for i in range(5):
            url= "https://api.github.com/repos/"+search_id+"/"+repositoryName+"/issues?page="+str(i+1)+"&per_page=100&access_token=cdd25761e5458bf25f257f4164f40a7a5e8d7422"
            response = requests.get(url)
            data = json.loads(response.content)
            #print data
            for all in data:
                j=j+1;
                temp=Post()
                time1 = re.split(regexPattern, str(all['updated_at']))
                time2 = re.split(regexPattern,str(datetime.now()))
                temp.title=all['title']
                temp.user=all['user']['login']
                temp.post_id=all['number']
                temp.created_at=all['created_at']
                temp.updated_at=all['updated_at']
                temp.url=all['url']
                temp.comments=all['comments']
                temp.body=all['body']
                instancelist.append(temp)
                a= dt.datetime((int)(time1[0]),(int)(time1[1]),(int)(time1[2]),(int)(time1[3]),(int)(time1[4]),(int)(time1[5]))
                b= dt.datetime((int)(time2[0]),(int)(time2[1]),(int)(time2[2]),(int)(time2[3]),(int)(time2[4]),(int)((float)(time2[5])))
                dif = ((b-a).total_seconds()/(60*60*24))
                #print j ,time1, time2 ,dif
                if(dif<=1.00):
                    noOfOpenIssuesInLast24hr=noOfOpenIssuesInLast24hr+1
                    second.append(len(instancelist)-1)
                    first.append(len(instancelist)-1)
                if(dif>1.0 and dif <=7.0):
                    noOfOpenIssuesMoreThan24hLessThan7d= noOfOpenIssuesMoreThan24hLessThan7d+1
                    third.append(len(instancelist)-1)
                    first.append(len(instancelist)-1)
                if(dif>7.0):
                    noOfOpenIssuesMoreThan7d = noOfOpenIssuesMoreThan7d+1
                    fourth.append(len(instancelist)-1)
                    first.append(len(instancelist)-1)
        #print noOfOpenIssues, noOfOpenIssuesInLast24hr , noOfOpenIssuesMoreThan24hLessThan7d , noOfOpenIssuesMoreThan7d
        firsttitle =[]
        firstUser=[]
        firstcreatedat=[]
        firstupdatedat=[]
        firstcomments=[]
        firsturl=[]
        secondtitle =[]
        secondUser=[]
        secondcreatedat=[]
        secondupdatedat=[]
        secondcomments=[]
        secondurl=[]
        thirdtitle =[]
        thirdUser=[]
        thirdcreatedat=[]
        thirdupdatedat=[]
        thirdcomments=[]
        thirdurl=[]
        fourthtitle =[]
        fourthUser=[]
        fourthcreatedat=[]
        fourthupdatedat=[]
        fourthcomments=[]
        fourthurl=[]
        for each in second:
            secondtitle.append(instancelist[each].title)
            secondUser.append(str(instancelist[each].user))
            secondcreatedat.append(str(instancelist[each].created_at))
            secondupdatedat.append(str(instancelist[each].updated_at))
            secondcomments.append(str(instancelist[each].comments))
            secondurl.append(str(instancelist[each].url))
        for each in first:
            firsttitle.append(instancelist[each].title)
            firstUser.append(str(instancelist[each].user))
            firstcreatedat.append(str(instancelist[each].created_at))
            firstupdatedat.append(str(instancelist[each].updated_at))
            firstcomments.append(str(instancelist[each].comments))
            firsturl.append(str(instancelist[each].url))
        for each in third:
            thirdtitle.append(instancelist[each].title)
            thirdUser.append(str(instancelist[each].user))
            thirdcreatedat.append(str(instancelist[each].created_at))
            thirdupdatedat.append(str(instancelist[each].updated_at))
            thirdcomments.append(str(instancelist[each].comments))
            thirdurl.append(str(instancelist[each].url))
        for each in fourth:
            fourthtitle.append(instancelist[each].title)
            fourthUser.append(str(instancelist[each].user))
            fourthcreatedat.append(str(instancelist[each].created_at))
            fourthupdatedat.append(str(instancelist[each].updated_at))
            fourthcomments.append(str(instancelist[each].comments))
            fourthurl.append(str(instancelist[each].url))

        print noOfOpenIssues, noOfOpenIssuesInLast24hr , noOfOpenIssuesMoreThan24hLessThan7d , noOfOpenIssuesMoreThan7d
        #return HttpResponse("<h2>HEY!</h2>")
        #,{'content':[noOfOpenIssues,noOfOpenIssuesInLast24hr,noOfOpenIssuesMoreThan24hLessThan7d,noOfOpenIssuesMoreThan7d]}
        return render(request,'shippable/home.html',{'content1':[{'first':[{'title':zip(firsttitle,firstUser,firstcreatedat,firstupdatedat,firstcomments,firsturl)}],'second':[{'title':zip(secondtitle,secondUser,secondcreatedat,secondupdatedat,secondcomments,secondurl)}],'third':[{'title':zip(thirdtitle,thirdUser,thirdcreatedat,thirdupdatedat,thirdcomments,thirdurl)}],'fourth':[{'title':zip(fourthtitle,fourthUser,fourthcreatedat,fourthupdatedat,fourthcomments,fourthurl)}], 'noOfOpenIssues':noOfOpenIssues,'noOfOpenIssuesInLast24hr':noOfOpenIssuesInLast24hr,'noOfOpenIssuesMoreThan24hLessThan7d':noOfOpenIssuesMoreThan24hLessThan7d,'noOfOpenIssuesMoreThan7d':noOfOpenIssuesMoreThan7d}]})

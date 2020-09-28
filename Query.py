#the query may have OR, AND conditions
Query = 'issuetype in ("Competence Area") AND "Competence Area" = "name"  AND ("Planned System Release" = XXXXX OR "Planned System Release" = XXXX2) AND  (cf[29790] = 123 OR cf[29790] = 2843 OR cf[29790] = 654 OR cf[29790] = 2850 OR cf[29790] = 945 OR cf[29790] = 154 )'

#without extension, to save the file later
Filename = 'JIRA_ALL_ITEMS'
Destination = r'C:\Users\Project\{}'.format(Filename)

#your IDs
ID = ""
PW = ""

from jira.client import JIRA
from pandas import DataFrame

#the link may change
options = {'server': 'https://jiradc.ext.net.XXX.com'}
jira = JIRA(options, basic_auth=(ID, PW))

#its the blocks per the JIRA documentation
IsFilter = "0" #Is not a filter
block_size = 1000
block_num = 0
allissues = []

while True:
    start_idx = block_num * block_size
    
    if IsFilter == '1':
        issues = jira.search_issues('filter=' + str(Query), start_idx, block_size)
    else: #is not a filter => Search by JQL
        issues = jira.search_issues(str(Query), start_idx, block_size)
        
    if len(issues) == 0:
        break
    block_num += 1
    
    for issue in issues:
        allissues.append(issue)
        
issues = DataFrame()
#MaxIssues = len(allissues)

#Big loop . May be optimized.
for issue in allissues:
    
    d = {}
    
    try:
        d.update({'key':str(issue.key).strip()})
    except AttributeError:
        d.update({'key':""})

    try:
        d.update({'Description.':issue.fields.customfield_10830})
    except AttributeError:
        d.update({'Description.':""})
            
    try:
        d.update({'Feature Description1':issue.fields.customfield_29891})
    except AttributeError:
        d.update({'Feature Description1':""})

    try:
        
        content=""
        content2 = ""
        content = str(issue.fields.customfield_123456) #.replace("<JIRA CustomFieldOption: value='","")
       
        
#                print("content initial :" , content)
        while content2 != content :
            content2 = content
            content = content.replace("<JIRA CustomFieldOption: value='","")
            content = content.replace("<JIRA CustomFieldOption: value='","")
            content = content.replace(content[content.find("'"):content.find(">")+1],"")
            content = content.replace("[","")
            content = content.replace("]","")
            
        
#                print("content modified :" , content)
        d.update({'PlannedRelease':content})
        
    except AttributeError:
        d.update({'PlannedRelease':""})
#
#    #Text2
#    try:
#        line =""
#        line = str(issue.fields.customfield_38727).strip().replace("\n","")
#        line = line.replace("\r",". ")
#        line = line.replace("\t","")
#        d.update({'Text2':line})
#    except AttributeError:
#        d.update({'Text2':""})
        
        
    try:
#        line =""
#        line = str(issue.fields.customfield_38727).strip().replace("\n","")
#        line = line.replace("\r",". ")
#        line = line.replace("\t","")
        d.update({'Text2':issue.fields.customfield_38727})
    except AttributeError:
        d.update({'Text2':""})
        
 
    try:
        d.update({'TargetFB':issue.fields.customfield_11111})
    except AttributeError:
        d.update({'TargetFB':""})

    try:
        d.update({'SpecificationType':issue.fields.customfield_22222})
    except AttributeError:
        d.update({'SpecificationType':""})

    try:
        d.update({'RiskStatus':issue.fields.customfield_33333})
    except AttributeError:
        d.update({'RiskStatus':""})

    try:
        d.update({'Build':issue.fields.customfield_44444})
    except AttributeError:
        d.update({'Build':""})

    try:
        d.update({'RemainingEstimate':issue.fields.timeestimate})
    except AttributeError:
        d.update({'RemainingEstimate':""})

    #append each item d with all its information to issue list
    issues = issues.append(d, ignore_index=True)

'transform to excel file
issues.to_excel(Destination+".xlsx", index=False)


#end = time.time()
#print(round(end - start,2) , "seconds, i.e" , round((end -start)/60,2), " minutes.")

import json
import urllib2
import os.path

from bs4 import BeautifulSoup

counter = 0
limit = 450
data = []
category_id = {'art': '1', 
               'comics': '3',
               'crafts': '26',
               'dance': '6',
               'design': '7',
               'fashion': '9',
               'film&video': '11',
               'food': '10',
               'games': '12',
               'journalism': '13',
               'music': '14',
               'photography': '15',
               'publishing': '18',
               'technology': '16',
               'theater': '17'}

def dump_data(category, projects):
    fname = category + '_data.json'
    f = open(fname, "w+")
    f.write(json.dumps(projects))
    f.close()
    
def get_project_info(id):
    # needs to use category id for further exploration
    page = 1
    first = True
    projects = [] 
    temp = []
    while ( first or len(temp) > 0 ) and len(projects) < limit:
        first = False  
        temp = []
        tech_url = "https://www.kickstarter.com/discover/advanced?state=successful&category_id=" + id + "&sort=end_date&page=" + str(page)
        print "visitig page " + str(page)
        result = urllib2.urlopen(url=tech_url, timeout=10)
        soup = BeautifulSoup(result)
        for entry in soup.select("div.project-card.relative.successful"):
            project = {}
            name_entry = entry.select("h6.project-title.mobile-center a")[0]
            project['url'] = name_entry['href']
            project['title'] = name_entry.contents[0].strip()
            project['pledged_percentage'] = entry.select("li.first.funded.inline-block.mr1 strong.block.h6")[0].contents[0].strip()
            project['pledged_amount'] = entry.select("li.pledged.inline-block.mr1 strong.block.h6 span.money")[0].contents[0].strip()
            project['end_date'] = entry.select("li.last.successful.inline-block div.deadline time")[0]['datetime']
            temp.append(project)
        projects.extend(temp)
        page += 1
    return projects


if __name__ == '__main__':
    
    for category, id in category_id.iteritems():
        fname = category + '_data.json'
        if not os.path.isfile(fname):
            print "visiting " + category
            projects = get_project_info(id)
            dump_data(category, projects)
    print "done"



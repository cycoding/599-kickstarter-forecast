import json
import os.path
import urllib2
from bs4 import BeautifulSoup

def dump_data(filename, projects):
    fname = filename.split(".")[0] + "_complete." + filename.split(".")[1]
    print fname
    if os.path.isfile(fname):
        os.remove(fname)
    f = open(fname, "w+")
    f.write(json.dumps(projects))
    f.close()

def get_facebook_stats(query_url):
    url = "http://api.facebook.com/restserver.php?method=links.getStats&urls="+ query_url + "&format=json"
    response = urllib2.urlopen(url, data=None, timeout=10)
    data = json.load(response)[0]
    print "====================================================================="
    fb_stat = {'like_count': data['like_count'],
               'share_count': data['share_count'],
               'comment_count': data['comment_count']}
    return fb_stat

def get_fb_comments(query_url):
    url = "http://graph.facebook.com/comments?id="+query_url
    response = urllib2.urlopen(url, data=None, timeout=10)
    data = json.load(response)['data']
    print data
    

def project_detail_info(projects):
    base_url = "https://www.kickstarter.com"
    state = 'successful'
    for project in projects:
        updates_count = 0
        url = base_url + project['url']
        print url
        page = urllib2.urlopen(url=url, timeout=10)
        soup = BeautifulSoup(page)
        
        # Get number of backers, pledged goal and updates count
        backers_count = soup.select("div#backers_count")[0]['data-backers-count']
        pledged_goal = soup.select("div#pledged")[0]['data-goal']
        span = soup.select("span#updates_count")
        print span
        if len(span) > 0:
            updates_count = soup.select("span#updates_count")[0]['data-updates-count']
        fb_stat = get_facebook_stats(url)
#         try:
#             
#         except Exception, e:
#             print url
#             print e
#             break
        
        # write it back into file
        project['state'] = state
        project['backers_count'] = backers_count
        project['pledged_goal'] = pledged_goal
        project['updates_count'] = updates_count
        project['fb_stat'] = fb_stat
        
if __name__ == '__main__':
    i = 0
    for filename in os.listdir('raw-data'):
        print "visiting file " + filename
        if i < 1:
            with open(os.path.join('raw-data', filename), "r+") as f:
                projects = json.load(f)
                project_detail_info(projects)
                dump_data(filename, projects)
            i += 1
    print "done"

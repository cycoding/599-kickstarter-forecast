import json
import os
import urllib2
from bs4 import BeautifulSoup

def dump_data(filename, projects):
    fname = filename.split(".")[0] + "_comments." + filename.split(".")[1]
    print fname
    if os.path.isfile(fname):
        os.remove(fname)
    f = open(fname, "w+")
    f.write(json.dumps(projects))
    f.close()

def exist(filename):
    fname = filename.split(".")[0] + "_comments." + filename.split(".")[1]
    if os.path.isfile(fname):
        return True
    return False

def get_comments(project):
    base_url = "https://www.kickstarter.com"
    url=base_url+project['url']+"/comments"
    print "visiting ", url
    
    page = urllib2.urlopen(url=url, timeout=10)
    soup = BeautifulSoup(page)
    comment_tags=soup.select("div.comment-inner")
    print "len of first-page comments is: ", str(len(comment_tags))
    # get all comment_tags
    older_comment = soup.select("a.older_comments")
    while len(older_comment)>0:
        url=base_url+older_comment[0]['href']
        page=urllib2.urlopen(url=url, timeout=10)
        soup=BeautifulSoup(page)
        
        print "len of older-page comments is: ", str(len(soup.select("div.comment-inner"))) 
            
        comment_tags.extend(soup.select("div.comment-inner"))
        older_comment=soup.select("a.older_comments")
        
    #store comments into json object
    comments=[]
    for comment_tag in comment_tags:
        comment={}
        
        name_tag=comment_tag.select("a.author")[0]
        comment['author']=name_tag.contents[0].strip()
        comment['url']=name_tag['href']
        
        content=""
        content_tags=comment_tag.select("p")
        for content_tag in content_tags:
            try:
                content += content_tag.contents[0].strip()
            except Exception, e:
                print "error occurs: ", url
                print e
                continue
        comment['content'] = content
        comments.append(comment)
    project['comments'] = comments
    
if __name__ == '__main__':
    for filename in os.listdir('raw-data'):
        print "visiting file " + filename
        if not exist(filename):
            with open(os.path.join('raw-data', filename), "r+") as f:
                projects = json.load(f)
                for project in projects:
                    get_comments(project)
                dump_data(filename, projects)
    print "done"
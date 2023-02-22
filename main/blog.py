import requests
from bs4 import BeautifulSoup

 
# Making a GET request
r = requests.get('https://www.newscientist.com/subject/technology/')
 

soup = BeautifulSoup(r.content, 'html.parser')
 
lines = soup.find_all('div', class_="card__content card__content--linked")

from django.template.defaultfilters import slugify
def get_blogs():
    i = 1
    blog_list = []
    
    for line in lines:
        # print(line.find({"h2":'card__heading'}))
        a = line.find({"a":'card__link'}, href = True)
        r_in = requests.get('https://www.newscientist.com' + a['href'])
        soup_in = BeautifulSoup(r_in.content, 'html.parser')    
        lines_in = soup_in.find('div', class_="article-body js-scroll-point")
        blog_detail = {}
        blog_field ={}
        blog_detail['model'] = 'main.Blog'
        blog_detail['pk'] = i
        # blog_field["timestamp"] = ""
        blog_field["description"] = ""
        blog_field["is_active"] = True
        try:
            blog_field['name'] = lines_in.find({'h1':'article__title'}).text
            blog_field["slug"] = slugify(blog_field['name'])
            blog_field['body'] = lines_in.find({'p':'article__strap'}).text
            try:
                blog_field['author'] = lines_in.find('b').text
            except:
                pass
                # print("No author")
            src = lines_in.find('img')
            if src and src.has_attr('data-src'):
                blog_field['image'] = src['data-src']

        except:
            pass
            # print("error " ,  i)
        blog_detail['fields'] = blog_field
        blog_list.append(blog_detail)
        i+=1
        if i == 10:
            break
    return blog_list

blogs = get_blogs()
# blogs = dict(blogs)
import json
 
# Serializing json
json_object = json.dumps(blogs)
 
# Writing to sample.json
with open("fixtures/blog_data.json", "w") as outfile:
    outfile.write(json_object)


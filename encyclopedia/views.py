from django.shortcuts import render
import markdown
import random
from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content is None:
        return render(request, "encyclopedia/error.html", {
            "error_message": "There is no such entry"
        }) 
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html_content": html_content
        })
    
def search(request):
    if request.method == "POST":
        search_box = request.POST['q']
        html_content = convert_md_to_html(search_box)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
            "title": search_box,
            "html_content": html_content
            })
        else:
            entries = util.list_entries()
            recommendation = []
            for entry in entries:
                if search_box.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })
        

def create_new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                "error_message": "This entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "html_content": html_content
            })


def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    

def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html_content": html_content
        })


def rand(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    html_content = convert_md_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "html_content": html_content
    })
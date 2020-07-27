from django.shortcuts import render
from . import util
from markdown2 import Markdown

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(util.get_entry(entry)),
            "title": entry
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Requested page does not exit."
        })

def search(request):
    if request.method == "POST":

        ### Search query
        keyword = request.POST["q"]

        entries = util.list_entries()

        if keyword in entries:
            return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(util.get_entry(keyword)),
            "title": keyword
        })
        
        matches = []

        for entry in entries:
            if keyword.lower() in entry.lower():
                matches.append(entry)

        if len(matches) == 0:
            matches.append("No results found.")

        return render(request, "encyclopedia/search.html", {
            "keyword": keyword,
            "matches": matches
        })

def new(request):
    if request.method == "POST":

        title = request.POST["title"]
        content = request.POST["content"]

        entries = util.list_entries()

        if title in entries:
            
            return render(request, "encyclopedia/error.html", {
            "message": "Entry already exists with that title.  Please select a new title."
        })

        util.save_entry(title, content)

        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(util.get_entry(title)),
            "title": title
        })

    else:
        return render(request, "encyclopedia/new.html")

def edit(request):    

    title = request.POST["title"]
    content = util.get_entry(title)

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def update(request):
    if request.method == "POST":

        title = request.POST["title"]
        content = request.POST["content"]

        entries = util.list_entries()

        util.save_entry(title, content)

        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(util.get_entry(title)),
            "title": title
        })

def random(request):
    import random

    entries = util.list_entries()

    random_entry = random.choice(entries)

    return render(request, "encyclopedia/entry.html", {
        "entry": markdowner.convert(util.get_entry(random_entry)),
        "title": random_entry
    })
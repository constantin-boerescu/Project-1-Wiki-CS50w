from django.shortcuts import render
from . import util
from markdown2 import Markdown

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry):
    '''Renders a page of the encyclopedia entry'''

    # coverts the .md file format into HTML
    try:
        coverted = markdowner.convert(util.get_entry(entry))
        
    # if the entry is None renders a not found message
    except:
        return render(request, "encyclopedia/entry_page.html",{
        "entry_title": "Not found",
        "not_found": f"{entry.capitalize()} was not found"
    })

    # passing the entry_title and converted HTML code to the entry_page and renders it
    return render(request, "encyclopedia/entry_page.html",{
        "entry_title":entry.capitalize(),
        "entry": coverted
    })
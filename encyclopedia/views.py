from django.shortcuts import render

from . import util

from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry):
    '''Renders a page of the encyclopedia entry'''

    markdowner = Markdown()

    # coverts the .md file format into HTML
    coverted = markdowner.convert(util.get_entry(entry))

    # passing the entry_title and converted HTML code to the entry_page and renders it
    return render(request, "encyclopedia/entry_page.html",{
        "entry_title":entry.capitalize(),
        "entry": coverted
    })
from django.shortcuts import render

from . import util

import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry):
    title = markdown2.markdown(util.get_entry(entry))
    print(title)
    return render(request, "encyclopedia/entry_page.html",{
        "entry": title
    })
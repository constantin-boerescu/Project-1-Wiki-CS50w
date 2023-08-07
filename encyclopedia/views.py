from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django.urls import reverse


from django import forms
from django.http import HttpResponseRedirect
import re

markdowner = Markdown()

# ---Testing---
class NewSearchQuerry(forms.Form):
    query = forms.CharField(label="Search")


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

def search_result(request):
    '''Takes a user input and return a page acordingly'''

    # if the form is submited the search_result page is returned
    if request.method == 'POST':

        # gets the user input and assigns it to query variable
        query = request.POST.get('q')

        # gets the entries
        entries = util.list_entries()
        
        # lower the entries
        lowered = []
        for entry in entries:
            lowered.append(entry.lower())

        # if the query is in the entries list returns the entry page
        if query.lower() in lowered:
            #  Redirects the user to the entries page
            return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=[query]))

        else:
            # if the user query is a substring of an entry it returns the entry
            for entry in entries:
                if re.search(query, entry):

                    return render(request, "encyclopedia/search_result.html", {
                        "query": entry
                    })
            # if the query is not a substring returns a not found message
            return render(request, "encyclopedia/entry_page.html",{
                    "entry_title": "Not found",
                    "not_found": f"{query.capitalize()} was not found"
                })
        
def create_new(request):
    '''Let the user create a new encyclopedia entry'''

    if request.method == 'GET':

    # returns the create_new page
        return render(request,  "encyclopedia/create_new.html")
    
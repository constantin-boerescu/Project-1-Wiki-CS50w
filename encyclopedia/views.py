from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django.urls import reverse

from random import randint
from django import forms
from django.http import HttpResponseRedirect
import re

markdowner = Markdown()

def get_lower_entries():
    '''Gets a list of entries lowers them and returns a lowered list'''

    lower_entries = []

    # get the entries
    entries = util.list_entries()

    # lowers each entries and appends them to the lower list
    for entry in entries:
        lower_entries.append(entry.lower())

    # returns the lowered list
    return lower_entries

def save_content(title, raw_content):
    '''Get a title and raw content, and saves the entry'''
    content = f"#{title}\n" + raw_content
    util.save_entry(title, content)

def index(request):
    '''Renders the home page'''

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
        lowered = get_lower_entries()

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
    
    else:
        # gets the entry title
        title = request.POST.get('entry_title')
        # gets the entry content
        raw_content = request.POST.get('entry_content')

        
        # checks if title and content field are filled
        if title and raw_content:
            # checks if the entry name already exists
            if title.lower() in get_lower_entries():
                # returns an error message
                return render(request, "encyclopedia/error.html",{
                    "message":"Sorry but the entry already exists",
                })
            
            # if the entry does not already exists it makes an .md file
            else:
                # saves the content
                save_content(title, raw_content)
            
            return HttpResponseRedirect(reverse("encyclopedia:index"))
        else:
            # returns an error message
            return render(request, "encyclopedia/error.html",{
                "message":"Sorry but the title or content field are empty",
            })

def edit_page(request, entry_title):
    '''Let the user to edit a entry content'''

    if request.method == "GET":
        # get the content of the entry
        raw_content = util.get_entry(entry_title)
        # get the lines of the content
        lines = raw_content.splitlines()
        # get rid of the firt line of the content
        content = "\n".join(lines[1:])

        return render(request,  "encyclopedia/edit_page.html",{
            "entry_title":entry_title,
            "content": content
        })
    else:

        # gets the entry title
        title = request.POST.get('edit_title')
        # gets the entry content
        raw_content = request.POST.get('edit_content')
        # saves the content
        save_content(title, raw_content)

        return HttpResponseRedirect(reverse("encyclopedia:index"))

def random(request):
    '''Redirect the user on a random entry page'''

    #get the number of entries
    entries = util.list_entries()

    # count the entries
    cnt_entries = len(entries)

    # return sa random entry
    rand_entry = entries[randint(0, cnt_entries - 1)]
    return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=[rand_entry]))

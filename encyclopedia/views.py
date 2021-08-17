from django.shortcuts import render

import markdown2
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# this funtion takes a parameter entered in the url the parameter should be the title of one of the entrys
def entry(request, title):
    # if the parameter is not the titles of one of the entries then throw an error message
    if not util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": "Entry does not exist"
        })
    # if its is one of the entries then dispalay the information
    return render(request, "encyclopedia/entry.html", {
    "title": title,
    "content": markdown2.markdown(util.get_entry(title))
    })

def search(request):
    # as soon as user posts search request
    if request.method == "POST":
        # place user input into the title varuble
        title = request.POST["q"]
        # if the title does not match any of the titles saved
        if not util.get_entry(title):
            # then pull the list of all the titles saved
            list = util.list_entries()
            result = []
            # loop through them
            for item in list:
                # if one of the items kinda match what where looking for then save them in the result list
                if title in item:
                    result.append(item)
            # if the result list is empty then throw an error
            if not result:
                return render(request, "encyclopedia/search.html",{
                "message": "No Match Found",
                "result": list
                })
            # otherwise return the list
            return render(request, "encyclopedia/search.html",{
            "message": "Search results",
            "result" : result
            })

        # redirect them to the page with the results of the search request
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title":request.POST["q"]}))
    return render(request, "encyclopedia/search.html")

# created form
class new_page(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class':'title'}))
    content = forms.CharField(widget=forms.Textarea)

def create_new_page(request):
    # if user posted data
    if request.method == "POST":
        # take the data user submitted and save it in form
        form = new_page(request.POST)
        # make sure data is valid
        if form.is_valid():

            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # make sure title doen't exixt yet
            if not util.get_entry(title):
                # save content
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title":title}))

            else:
                # if it does exixt then render error message
                return render(request, "encyclopedia/error.html",{
                "error": "Title already exists"
                })


        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/create_new_page.html", {
                "form": form
            })
    # return blank form
    return render(request, "encyclopedia/create_new_page.html",{
    "form": new_page()
    })

def edit(request):
    # as soon as user posts search request
    if request.method == "POST":
        # place user input into the title varuble
        title = request.POST["title"]
        # derect user to page where they can edit the content
        return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": util.get_entry(title)
        })

    return render(request, "encyclopedia/error.html",{
    "error": "Select the page you want to edit"
    })

def update(request):
    # if user submits changes
    if request.method == "POST":
        # save the changes
        util.save_entry(request.POST["title"], request.POST["content"])
        # direct user to the page with the new content
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title":request.POST["title"]}))

    return render(request, "encyclopedia/error.html",{
    "error": "Select the page you want to update"
    })

def random_page(request):
    # redirect user to a random page
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"title":random.choice(util.list_entries())}))

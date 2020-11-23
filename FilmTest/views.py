# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 17:51:20 2020

@author: IvoryT
"""
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect


def hello(request):

    return redirect("http://127.0.0.1:8000/film/")


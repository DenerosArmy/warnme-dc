import sys, os 
import settings 
from django.core.management import setup_environ 
setup_environ(settings) 

from main.models import * 




import sys
import os

# Get absolute path to project root and add to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from components.Hero import show_hero
from components.home_content import show_home

show_hero()
show_home()
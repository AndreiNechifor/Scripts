from pep318_automation_class import AccesPep318
import warnings
import pytest
element=AccesPep318(without_window=True)
element=AccesPep318(without_window=True)
#test_pages = ['http://scratchpd.com','http://google.ro','http://python.org','http://www.bitacad.net']
test_pages=['http://python.org','http://python.org']

# Testing area
def over_all_testing():
    for e in test_pages:
        assert element.test_method(e)=="Test passed","Test not passed"
    return "Test passed"
over_all_testing()
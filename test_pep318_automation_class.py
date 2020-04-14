from pep318_automation_class import AccesPep318
import warnings
import pytest
element=AccesPep318(without_window=True)
# Testing area
test_pages=('http://scratchpd.com','http://google.ro','https://python.org','http://www.bitacad.net')
param_list=[(x,'Test passed') for x in['http://scratchpd.com','http://google.ro','https://python.org','http://www.bitacad.net']]                                            
@pytest.mark.parametrize('page,passed',param_list)
def test_test_method(page,passed): 
    for e in page:
        assert element.test_method(e)==passed






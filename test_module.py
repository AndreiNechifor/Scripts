from pep318_automation_class import AccesPep318
import warnings
element=AccesPep318(without_window=True)
def test_method(url):
    """This is the method that calls all the previously declared methods"""
    element.update_navigators()
    if not(element.request_url(url)):
        warnings.warn("Link could not be acces")
        return 0
    else:
        element.check_sum+=1
            
    if not(element.first_page()):
        warnings.warn("Elements from the first page could not be found")
        return 0
    else:
        element.check_sum+=1
    if not(element.open_search_result()):
        warnings.warn("Elements from the search page could not be found")        
        return 0
    else:
        element.check_sum+=1
        warnings.warn("Test succeded for page %s"%(url))
        return 1
succes_rate=0
succes_counter=0
page_scores={}
element=AccesPep318(without_window=True)
test_pages = ['http://scratchpd.com','http://google.ro','http://python.org','http://www.bitacad.net']

# Testing area
for e in test_pages:
    succes_counter=test_method(e)
    page_scores[e]=str(element.check_sum/3*100)+"%"

# Logging area
element.logging("Test finished with these results","")
for independent_score in page_scores:# Looping through individual test scores
    element.logging(independent_score+":",page_scores[independent_score])
succes_rate=succes_counter/len(test_pages)*100
element.logging("Overall result :",str(succes_rate))
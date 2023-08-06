from crossref.restful import Works
import time
import multiprocessing.dummy as mp 
import requests

def _download_content(DOI, location):
    """
    input:
        DOI : DOI of the article
        location : location where the article needs to be stored
    output:
        True: if the article was downloaded succesfully
        False: if the article could not be downloaded succesfully
    Feature:
        Download the Article present in the DOI
    """
    flag = 0
    works = Works()
    try:
        api_response = works.doi(DOI)
        if api_response:
            link = api_response.get('link')
            if link:
                for l in link:
                    address = l.get('URL')
                    if 'xml' in address:
                        time.sleep(1)
                        response = requests.get(address)
                        file_name =  location + DOI +'.xml'
                        if '</html>' not in str(response.content):
                            with open(file_name, 'wb') as f:
                                f.write(response.content)
                            flag = 1
                            return True

                    else:
                        response = requests.get(address)
                        file_name = location + DOI +'.pdf'
                        if '</html>' not in str(response.content):
                            with open(file_name, 'w') as f:
                                f.write(response.content)
                            flag = 1
        if flag == 0:
            return False
        else:
            return True                        
    except:
        time.sleep("120")
        print(DOI)


def download(DOI, location):
    """
    input:
        DOI : DOI of the article
        location : location where the article needs to be stored
    output:
        True: if the article was downloaded succesfully
        False: if the article could not be downloaded succesfully
    """
    if location[-1] != "/":
        location = location + "/"
    return _download_content(DOI, location)
    

def download_bulk(DOI_list, location):
    """
    input:
        DOI_list : list of DOIs of the articles
        location : location where the articles need to be stored
    output: None
    """
    if location[-1] != "/":
        location = location + "/"
    p=mp.Pool(8)
    p.map(_download_content, DOI_list, location) 
    p.close()
    p.join()



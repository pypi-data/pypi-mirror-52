import pandas as pd 
from crossref.restful import Works 
from unidecode import unidecode
import re
from urllib.parse import urlparse, unquote, unquote_plus


def get_DOI_from_URL(address):
    """
    input: 
        address: web address
    output: 
        DOI of the URL (if able to find)
        False: if undable to find the DOI
    """
    return _doi_retrieve(address)


def get_metadata_from_DOI(DOI):
    """
    input:
        DOI : DOI of the article
    output:
        metadata : dictionary containing the metadata of article  
    """
    return _get_metadata(DOI)
    

def get_metadata_from_URL(address):
    """
    input:
        address : Address of the article
    output:
        metadata : dictionary containing the metadata of article  
    """
    DOI = _doi_retrieve(address)
    if DOI == False:
        return (False, "DOI not found in address")
    return _get_metadata(DOI)


def _doi_retrieve(address):
    """
    input: 
        address: web address
    output: 
        DOI of the URL (if able to find)
        False: if undable to find the DOI
    """
    address = unquote(address).replace(" ","")
    doi_regex = r"^.*[/:=?](10.\d{4,9}/[-._;()/:a-zA-Z0-9]+).*$"
    result = re.search(doi_regex, address)
    if result: 
        return(result.group(1))
    return(False)


def _get_metadata(DOI):
    """
    input:
        DOI : DOI of the article
    output:
        metadata : dictionary containing the metadata of article  
    """
    works = Works()
    try:
        api_response = works.doi(DOI)
        if api_response:
            doi_type = api_response["type"]
            if doi_type == 'journal-article':
                result = {}
                result["doi"] = DOI
                result["publish_date"] = api_response.get("created").get("date-time") or ""
                result["title"] = api_response.get("title")[0] or ""
                result["journal"] = api_response.get('container-title')[0] or ""
                result["publisher"] = api_response.get('publisher') or ""
                author =  api_response.get("author") or ""
                if author != "":
                    result["author"] = _author_list_transformer(author)[0]
                    result["ORCID"] = _author_list_transformer(author)[1]
                ISSN = api_response.get('issn-type') or ""
                if ISSN != "":
                    result["ISSN_print"] = _ISSN_list_transformer(ISSN)[0]
                    result["ISSN_digital"] = _ISSN_list_transformer(ISSN)[1]
                if result["title"] == result["doi"] == result["journal"] == result["author"] == result["issn"] == "":
                    return(False, "Metadata not found for the DOI")
                else:
                    return(True, "journal-article", result)

            if doi_type == 'reference-book':
                result = {}
                result["doi"] = DOI
                result["publish_date"] = api_response.get("created").get("date-time") or ""
                result["title"] = api_response.get("title")[0] or ""
                author =  api_response.get("editor") or ""
                if author != "":
                    result["author"] = _author_list_transformer(author)[0]
                    result["ORCID"] = _author_list_transformer(author)[1]
                ISBN = api_response.get('isbn-type') or "" 
                if ISBN != "":
                    result["ISBN_print"] = _ISBN_list_transformer(ISBN)[0]
                    result["ISBN_digital"] = _ISBN_list_transformer(ISBN)[1]
                if result["title"] == result["isbn"] == "":
                    return(False, "Metadata not found for the DOI")
                else:
                    return(True, "reference-book", result)
                    
            if doi_type == "book-chatper":
                result["doi"] = DOI
                result["publish_date"] = api_response.get("created").get("date-time") or ""
                result["title"] = api_response.get("title")[0] or ""
                author =  api_response.get("author") or ""
                if author != "":
                    result["author"] = _author_list_transformer(author)[0]
                    result["ORCID"] = _author_list_transformer(author)[1]
                ISBN = api_response.get('isbn-type') or "" 
                if ISBN != "":
                    result["ISBN_print"] = _ISBN_list_transformer(ISBN)[0]
                    result["ISBN_digital"] = _ISBN_list_transformer(ISBN)[1]
                if result["title"] == result["isbn"] == "":
                    return(False, "Metadata not found for the DOI")
                else:
                    return(True, "book-chatper", result)

            if doi_type == "book":
                result["doi"] = DOI
                result["publish_date"] = api_response.get("created").get("date-time") or ""
                result["title"] = api_response.get("title")[0] or ""
                author =  api_response.get("editor") or ""
                if author != "":
                    result["author"] = _author_list_transformer(author)[0]
                    result["ORCID"] = _author_list_transformer(author)[1]
                ISBN = api_response.get('isbn-type') or "" 
                if ISBN != "":
                    result["ISBN_print"] = _ISBN_list_transformer(ISBN)[0]
                    result["ISBN_digital"] = _ISBN_list_transformer(ISBN)[1]
                if result["title"] == result["isbn"] == "":
                    return(False, "Metadata not found for the DOI")
                else:
                    return(True, "book", result)
        else:
            return(False, "Metadata not found for the DOI")
    except:
        return(False, "Metadata not found for the DOI")


def _author_list_transformer(author_dict):
    ORCID = []
    author_name = []
    for a in author_dict:
        given = a.get("given") or ""
        family = a.get('family') or ""
        author_name.append(given + " " + family)
        oid = a.get("ORCID") or ""
        ORCID.append(oid)
    return(author_name,ORCID)


def _ISSN_list_transformer(ISSN):
    ISSN_print = ""
    ISSN_digital =  ""
    for i in ISSN:
        if i["type"] == "print":
            ISSN_print = i["value"]
        if i["type"] == "electronic":
            ISSN_digital = i["value"]
    return(ISSN_print,ISSN_digital)


def _ISBN_list_transformer(ISBN):
    ISBN_print = ""
    ISBN_digital =  ""
    for i in ISBN:
        if i["type"] == "print":
            ISBN_print = i["value"]
        if i["type"] == "electronic":
            ISBN_digital = i["value"]
    return(ISBN_print,ISBN_digital)


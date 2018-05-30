GW Libraries fork of OCLC Python Authentication Library
=======================================================

This library is a fork of [https://github.com/OCLC-Developer-Network/oclc-auth-python](https://github.com/OCLC-Developer-Network/oclc-auth-python) which itself is a wrapper around the Web Service Authentication system used by OCLC web services, written for Python. It works with versions 2.7 and 3 (up to 3.6).

This library substitutes a GW-specific use case in place of the OCLC examples.  It calls the [Bibliographic Resource](https://www.oclc.org/developer/develop/web-services/worldcat-metadata-api/bibliographic-resource.en.html) read method from the [Worldcat Metadata API](https://www.oclc.org/developer/develop/web-services/worldcat-metadata-api.en.html), passing it an OCLC number and retrieving the item's MARC data.  From the MARC data, it attempts to extract the item's SUDOC number, title, year, and format.  The results are written to a CSV file.

Installation
------------

Clone the repository:

`git clone https://github.com/OCLC-Developer-Network/oclc-auth-python.git`

Set up a virtualenv:

`cd oclc-auth-python`
`virtualenv ENV`
`source ENV/bin/activate`

Install the `authliboclc` library:

`python setup.py install`

**Note:**  While the [WorldCat Search API does have a rate limit](https://www.oclc.org/developer/develop/web-services/worldcat-search-api/faqs.en.html), the WorldCat Metadata API does *not* have a rate limit at this time.


Running the Code
================

1. Change directories to `gw`

1. Edit `config.py` (copy from `example.config.py`) and insert your:
    * key
    * secret
    * principal_id
    * principal_idns
    * authenticating_institution_id
    * path to the input file (one clean OCLC id per line - blank lines are okay)
    * path to where you want the output CSV file
    
1. Run from the command line:

   `python metadata_lookup.py`
   
***GW Libraries Users***:  See `Deployment Notes / API Credentials / OCLC` for credentials


Resources
---------

* <a href="http://oclc.org/developer/home.en.html">OCLC Developer Network</a>
    * <a href="http://www.oclc.org/developer/develop/authentication.en.html">Authentication</a>
    * <a href="http://www.oclc.org/developer/develop/web-services.en.html">Web Services</a>
* <a href="https://platform.worldcat.org/wskey">Manage your OCLC API Keys</a>
* <a href="https://platform.worldcat.org/api-explorer/">OCLC's API Explorer</a>

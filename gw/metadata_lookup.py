#!/usr/bin/env python
# -*- coding: utf-8 -*-

from authliboclc import wskey, user
import httplib, urllib2
import json
from urllib2 import URLError


""" Helper class used to display the result headers """
class MyHTTPSConnection(httplib.HTTPSConnection):
    def send(self, s):
        print s
        httplib.HTTPSConnection.send(self, s)


""" Helper class used to display the result headers """
class MyHTTPSHandler(urllib2.HTTPSHandler):
    def https_open(self, req):
        request = self.do_open(MyHTTPSConnection, req)
        print request.info()
        return request


def biblookup(oclc_id):
    request_url = 'https://worldcat.org/bib/data/' + oclc_id

    authorization_header = my_wskey.get_hmac_signature(
        method='GET',
        request_url=request_url,
        options={
            'user': my_user,
            'auth_params': None}
    )

    """ We create an opener that accesses our helper classes,
        so we can display the headers that are returned."""
    opener = urllib2.build_opener(MyHTTPSHandler)
    opener.addheaders = [('Authorization', authorization_header),
                         ('Accept', 'application/atom+json')]

    try:
        # response = opener.open(request_url)
        # response_body = response.read()
        response_body = '{}'
        j = json.loads(response_body)
        # print json.dumps(j, indent=4, sort_keys=True)

    except URLError as e:
        response_body = e.read()
        print response_body
        if config.key == '{clientID}':
            print('\n** Note: Edit the script and supply \
                  valid authentication parameters. **\n')

    # TODO: Extract the four fields of interest
    # Put them in a Dictionary
    return {}


if __name__ == "__main__":
    import config

    my_wskey = wskey.Wskey(
        key=config.key,
        secret=config.secret,
        options=None)

    my_user = user.User(
        authenticating_institution_id=config.authenticating_institution_id,
        principal_id=config.principal_id,
        principal_idns=config.principal_idns
    )

    idfile = open(config.idfile, 'r')
    outfile = open(config.outfile, 'w')
    lastid = "0"
    lastbibinfo = {}
    for line in idfile.readlines():
        if len(line.strip()) == 0:
            outfile.write(",,,,\n")
        else:
            oclc_id = line[:-1]
            if oclc_id == lastid:
                # Don't re-look up the same id, but we still want a line
                bibinfo = lastbibinfo
            else:
                bibinfo = biblookup(oclc_id)
                lastid = oclc_id
                lastbibinfo = bibinfo
            outfile.write("%s,%s,%s,%s,%s\n" %
                          (oclc_id, 'A', 'B', 'C', 'D'))

    idfile.close()
    outfile.close()

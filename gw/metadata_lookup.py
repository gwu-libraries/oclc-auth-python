#!/usr/bin/env python
# -*- coding: utf-8 -*-

from authliboclc import wskey, user
import codecs
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

    bibresult = {'format': '', 'sudoc': '', 'title': '', 'year': '', 'found': False}
    try:
        response = opener.open(request_url)
        bibresult['found'] = True
        response_body = response.read()
        j = json.loads(response_body)
        record = j['content']['record']
        # print json.dumps(record, indent=4, sort_keys=True)

        fixedFields = record['fixedFields']
        variableFields = record['variableFields']
        for f in variableFields:
            if f['tag'] == '086':
                print("Found the 086")
                print json.dumps(f, indent=4, sort_keys=True)
                bibresult['sudoc'] = f['subfieldItems'][0]['data']
            if f['tag'] == '245':
                print("Found the 245")
                print json.dumps(f, indent=4, sort_keys=True)
                bibresult['title'] = ' '.join([s['data'] for s in f['subfieldItems']])
            if f['tag'] == '260':
                print("Found the 260")
                print json.dumps(f, indent=4, sort_keys=True)
                for s in f['subfieldItems']:
                    if s['subfieldCode'] == 'c':
                        bibresult['year260'] = s['data']
        for f in fixedFields:
            if f['tag'] == '008':
                print("FOUND THE 008")
                print json.dumps(f, indent=4, sort_keys=True)
                bibresult['format'] = f['data'].encode('ascii', 'ignore').decode('ascii')
                for e in f['fixedElements']:
                    if e['label'] == 'date1':
                        bibresult['year008'] = e['data']
        if 'year260' in bibresult and 'year008' in bibresult:
            # prefer the 008
            bibresult['year'] = bibresult['year008']
        else:
            bibresult['year'] = (bibresult['year260'] if 'year260' in bibresult else "") + \
                                (bibresult['year008'] if 'year008' in bibresult else "")

    except URLError as e:
        response_body = e.read()
        print "Response Code = %i" %  e.code
        print response_body
        if config.key == '{clientID}':
            print('\n** Note: Edit the script and supply \
                  valid authentication parameters. **\n')

    return bibresult


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
    outfile = codecs.open(config.outfile, 'w', 'utf-8')
    outfile.write('OCLC ID,SUDOC,TITLE,YEAR,FORMAT\n')
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
            if bibinfo['found'] is True:
                outfile.write('"' + oclc_id + '","' +
                              bibinfo['sudoc'] + '","' +
                              bibinfo['title'].replace('"', '""') + '",' +
                              bibinfo['year'] + ",Paper\n")
            else:
                outfile.write('\n')

    idfile.close()
    outfile.close()

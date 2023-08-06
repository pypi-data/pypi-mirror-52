#! /usr/bin/env python
# The ID of a sample document.
#DOCUMENT_ID = '1VvFBHxmpJ3IxMGiiM0GI733OlA73UFLAeCwS-E2hFGw'
#creds_fp = '/home/grg/credentials.json'

import pickle
import os.path as op
import os.path
import logging as log
import argparse
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
TESTS = False

cornflower_blue = {'blue': 0.929, 'green': 0.584, 'red': 0.392}
plum = {'blue': 0.867, 'green': 0.627, 'red': 0.867}
brownish = {'blue': 0.40, 'green': 0.40, 'red': 0.8}
black = {'blue': 0, 'green': 0, 'red': 0}


def get_creds(creds_fp):
    SCOPES = ['https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/documents']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/tmp/token.pickle'):
        with open('/tmp/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_fp, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/tmp/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def read_document(DOCUMENT_ID, creds):
    #creds = get_creds(creds_fp)
    service = build('docs', 'v1', credentials=creds, cache_discovery=False)
    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID, ).execute()
    return document

def copy_file(DOCUMENT_ID, title, creds, prefix='[BibTeX2Docs]'):
    #creds = get_creds(creds_fp)
    service = build('drive', 'v3', credentials=creds, cache_discovery=False)
    if TESTS:
        prefix = '[CI]'
    copy_title = '%s %s'%(prefix, title)
    body = {'name': copy_title}
    drive_response = service.files().copy(
        fileId=DOCUMENT_ID, body=body).execute()

    document_copy_id = drive_response.get('id')
    return document_copy_id

def apply(document_id, requests, creds):
    #creds = get_creds(creds_fp)
    service = build('docs', 'v1', credentials=creds, cache_discovery=False)
    result = service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()
    return result

def search_expression(document, expression='XNAT'):
    body = document['body']['content']
    found = []
    for e in body:
        if 'paragraph' in e:
            elements = e['paragraph']['elements']
            for el in elements:
                if 'textRun' in el and expression in el['textRun']['content']:
                    index = el['textRun']['content'].find(expression)
                    found.append(el['startIndex']+index)
    return found

def search_references(document):
    import re
    body = document['body']['content']
    found = []
    for e in body:
        if 'paragraph' in e:
            elements = e['paragraph']['elements']
            for el in elements:
                if 'textRun' in el:
                    els = re.split(' |;|,|\)|\n|\(', el['textRun']['content'])
                    els = [each for each in els if each != '']
                    for each in els:
                        if each.startswith('@'):
                            found.append(each)
    return found

def format_authors(authors):

    import re
    import nameparser as n
    authors = [n.HumanName(each) for each in authors.split(' and ')]

    s = ''
    for e in authors:
        first = '' if len(e['first']) == 0 else ' %s'%'.-'.join([w[0].upper() for w in re.split(' |-', e['first'].strip()) if w != ''])
        middle = '' if len(e['middle']) == 0 else ' %s.'%e['middle'][0]
        s = s + '%s,%s.%s, '%(e['last'], first, middle)
    return s

def format_reference(e):
    import re
    import nameparser as n
    a = [n.HumanName(each) for each in e['author'].split(' and ')][0]
    #ref = '%s et al. (%s)'%(a['last'], e['year'])
    ref = '%s et al., %s'%(a['last'], e['year'])

    return ref

def read_references(fp):

    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.customization import convert_to_unicode
    from pprint import pprint

    references = {}
    with open(fp) as bibtex_file:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
        for e in bib_database.entries:
            try:
                authors = e['author']
                journal = e['journal'] if 'journal' in e else e['booktitle']
                doi = ' doi:%s '%e['doi'] if 'doi' in e else ' %s '%e['url']
                if len(authors.split(' and ')) == 1:
                    print('Check authors in %s: %s'%(e['ID'], e['author']))

                s = format_authors(authors)
                volpages = '' if 'volume' not in e else '%s %s'%(e['volume'], '(%s)'%e['pages'] if 'pages' in e else '')
                if 'issn' in e:
                    volpages = volpages + ' ' + e['issn']
                shortref = format_reference(e)
                longref = '%s%s, %s, %s%s(%s)'%(s, e['title'], journal, volpages, doi, e['year'])
                references[e['ID']] = (shortref, longref)
            except KeyError as ex:
                print('Error with reference %s'%e['ID'])
                pprint(e)
                raise ex
    return references

def parse_groups(document, references):
    import re
    body = document['body']['content']
    elements = []
    for e in body:
        if 'paragraph' in e:
            elements.extend(e['paragraph']['elements'])
    elements = [{'startIndex': e['startIndex'], 'endIndex': e['endIndex'], 'content': ''.join([c for c in e['textRun']['content'] if c not in '().;, \n'])} for e in elements if 'textRun' in e]
    elements = [{'startIndex': e['startIndex'], 'endIndex': e['endIndex'], 'content': e['content']} for e in elements if e['content'] != '']
    groups = []

    is_in_group = False
    for el in elements:
        content = el['content']
        startIndex = el['startIndex']
        endIndex = el['endIndex']
        if content.startswith('@') and content.strip('@') in references:
            if not is_in_group:
                is_in_group = True
                start = startIndex
                group = []
            group.append(content)
            end = endIndex #+ len(content)
        elif is_in_group:
            groups.append({'start': start, 'refs': group, 'end': end})
            is_in_group = False
    return groups

def highlight_requests(document, references, highlight=True):

    requests = []
    if highlight:
        for e, (v0, v1) in list(references.items()):
            index = sorted(search_expression(document, expression='@%s'%e))
            for each in index:
                requests.append(
                    {
                        'updateTextStyle': {
                            'range': {
                                'startIndex': each,
                                'endIndex': each + len('@%s'%e)
                                },
                            'textStyle': {
                                'foregroundColor': {
                                    'color': {
                                        'rgbColor': cornflower_blue
                                    }
                                }
                            },
                            'fields': 'foregroundColor'
                        }
                    })
    return requests

def format_group(g, ordered_ref, references, numindex=False):
    if numindex:
        ref = [ordered_ref.index(r[1:]) + 1 for r in g]
        return ref_to_str(ref)
    else:
        return '; '.join([references[r[1:]][0] for r in g])


def replace_requests(groups, ordered_ref, references, numindex=False):
    groups.reverse()



    requests = []
    for g in groups:
        r = {'deleteContentRange': {
                'range': {
                    'startIndex': g['start'],
                    'endIndex': g['end'],
                }
            }
        }
        requests.append(r)

        grp = format_group(g['refs'], ordered_ref, references,
            numindex=numindex)
        r = {'insertText': {
                'location': {
                    'index': g['start'],
                },
                'text': grp
            },
            }
        requests.append(r)
        r = {'updateTextStyle': {
                'range': {
                            'startIndex': g['start'],
                            'endIndex': g['start'] + len(grp)
                        },
                'textStyle': {'foregroundColor': {
                    'color': {
                        'rgbColor': cornflower_blue
                    }
                }},
                'fields': 'foregroundColor',
            },
            }
        requests.append(r)

    return requests


def count_changes(res):
    res = res['replies']
    occ = 0
    for each in res:
        if 'replaceAllText' in each \
            and 'occurrencesChanged' in each['replaceAllText']:
            occ = occ + each['replaceAllText']['occurrencesChanged']

    return occ


def split_ref(ref):
    ref = sorted(ref)
    m, M = min(ref), max(ref)
    res = []
    a, end = 0,0
    while end < ref[-1]:
        while not a in ref:
            a = a + 1
        start = a
        while a in ref:
            a = a + 1
        end = a - 1
        if start != end:
            res.append((start, end))
        else:
            res.append((start,))
    return res

def ref_to_str(ref):
    s = '['
    bits = split_ref(ref)
    for b in bits:
        if len(b) == 1:
            s = s + '%s, '%b[0]
        else:
            s = s + '%s-%s, '%(b[0], b[1])
    s = s[:-2] + ']'
    return s

def color_biblio(document, bibtag):
    b = search_expression(document, bibtag)
    requests = []
    for e in b:
        r = {'updateTextStyle': {
                'range': {
                            'startIndex': e,
                            'endIndex': e + len(bibtag)
                        },
                'textStyle': {'foregroundColor': {
                    'color': {
                        'rgbColor': cornflower_blue
                    }
                }},
                'fields': 'foregroundColor',
            },
            }
        requests.append(r)
    return requests


def replace_references(document_id, bibtex_file, creds_fp, numindex=True,
    highlight=True, inplace=False, replace=True):

    bibtag = '{{bibliography}}'

    creds = get_creds(creds_fp)
    print('\n')
    document = read_document(document_id, creds)
    title = document.get('title')
    print('Read document (title: %s)'%title)

    references = read_references(bibtex_file)
    ordered_ref = find_references(document, references)

    references_found = {e : references[e] for e in ordered_ref}

    if references_found == {}:
        print('No matching references found. Exiting.')
        references = search_references(document)
        print('Found references: %s'%references)
        return

    title = document.get('title')

    if inplace:
        copy_id = document_id
        copy_doc = document
        copy_doc = read_document(copy_id, creds)
    else:
        copy_id = copy_file(document_id, title, creds)
        copy_doc = read_document(copy_id, creds)
        print('Created new document (title: %s)'%copy_doc.get('title'))


    requests = highlight_requests(copy_doc, references)
    result = apply(copy_id, requests, creds)
    print('%s references found and highlighted'%len(requests))
    copy_doc = read_document(copy_id, creds)

    groups = parse_groups(copy_doc, references)

    if replace:
        requests = replace_requests(groups, ordered_ref, references,
            numindex=numindex)
        result = apply(copy_id, requests, creds)
        print('%s references found and replaced'%len(requests))
        copy_doc = read_document(copy_id, creds)


    remaining_ref = search_references(copy_doc)
    if len(remaining_ref) != 0:
        print('References not found: %s'%remaining_ref)
    else:
        print('All references from the document were successfully replaced.')

    # Adding full reference list at {{bibtag}}
    if numindex:
        references_no = create_refno_dict(references, ordered_ref)
        reflist = build_reflist(references_no, numindex)
    else:
        reflist = build_reflist(references_found, numindex)

    if replace:
        requests = color_biblio(copy_doc, bibtag)
        result = apply(copy_id, requests, creds)
        copy_doc = read_document(copy_id, creds)

        requests = {
                'replaceAllText': {
                    'containsText': {
                        'text': bibtag,
                        'matchCase':  'true'
                    },
                    'replaceText': reflist,
                }
            }
        result = apply(copy_id, requests, creds)
        n_changes = count_changes(result)

        if n_changes != 0:
            print('Full reference list included successfully.')
        else:
            print('Missing tag (%s). Full reference list not included.'%bibtag)

    url = 'https://docs.google.com/document/d/' + copy_id
    print('Check new document at URL: %s'%url)

def find_references(document, references):
    ref = {}
    for k, v in references.items():
        index = sorted(search_expression(document, expression='@%s'%k))
        if len(index) > 0:
            ref[index[0]] = k

    ordered_ref  = [ref[e] for e in sorted(ref.keys())]
    return ordered_ref

def group_refs(elements, references):
    import re
    elements2 = [el for el in elements if 'textRun' in el]
    elements = []
    for el in elements2:
        content = el['textRun']['content']
        els = re.split(' |;|,|\)|\n|\(', content)
        els = [each for each in els if each != '']
        if els != []:
            elements.append(el)
    print(elements)


    groups = []

    for el in elements:
        content = el['textRun']['content']
        startIndex = el['startIndex']
        els = re.split(' |;|,|\)|\n|\(', content)
        els = [each for each in els if each != '']

        is_in_group = False
        last = None
        for i, each in enumerate(els):
            if each['content'].startswith('@') and each['content'] in references:
                if not is_in_group:
                    is_in_group = True
                    start = startIndex + content.find('@%s'%each)
                    group = []
                group.append(each)
                last = each
            if (not (each['content'].startswith('@') and each['content'] in references) \
                    and is_in_group) or (is_in_group and i == len(els) - 1):
                end = startIndex + content.find('@%s'%each) + len('@%s'%each)
                groups.append({'start': start, 'refs': group, 'end': end})
                is_in_group = False

    return groups


def create_refno_dict(references, ordered_ref):
    d = {}
    for i, e in enumerate(ordered_ref):
        d[e] = ('[%s]'%str(i+1), references[e][1])
    return d

def build_reflist(references, numindex=False):
    s = ''
    with_key = numindex
    if with_key:
        for e, v in references.items():
            i = v[0] if numindex else '%s:'%e
            s = s + i + ' '
            s = s + v[1] + '\n\n'
    else:
        for e in sorted(list(references.keys())):
            s = s + references[e][1] + '\n\n'
    return s

def create_parser():
    import argparse
    parser = argparse.ArgumentParser(description='bibtex2docs')
    parser.add_argument('DOCUMENT_ID', help='ID of the Google Docs document')
    parser.add_argument('BIBTEX', help='BibTeX file',
        type=argparse.FileType('r'))
    parser.add_argument('CREDENTIALS', help='File with credentials',
        type=argparse.FileType('r'))
    parser.add_argument('--verbose', '-V', action='store_true', default=False,
        help='Display verbosal information (optional)', required=False)
    parser.add_argument('--numbers', '-N', action='store_true', default=False,
        help='Replace by numbers or "FirstAuthor et al. (2019)"', required=False)
    parser.add_argument('--highlight', '-H', action='store_true', default=False,
        help='Highlight references', required=False)
    parser.add_argument('--noreplace', '-n', action='store_true', default=False,
        help='Don\'t replace references', required=False)
    parser.add_argument('--inplace', '-i', action='store_true', default=False,
        help='Modifiers document directly (not in a created copy)', required=False)
    return parser



import sys
if __name__=="__main__" :
    if len(sys.argv) == 1:
        DOCUMENT_ID = input('Enter ID of the Google Docs document: ')
        BIBTEX = input('Path to .bib file: ')
        CREDENTIALS = input('Path to Google API (OAuth 2.0) client credentials: ')
        do_nb = input('Reference style: 0: FirstAuthor et al. (2019) 1: Numbers ? ')
        do_numbers = do_nb==1

        replace_references(DOCUMENT_ID, BIBTEX,
             CREDENTIALS, numindex=do_numbers)
    else:
        parser = create_parser()
        args = parser.parse_args()
        if args.verbose:
            log.basicConfig(level=log.DEBUG)
        else:
            log.basicConfig(level=log.WARNING)

        if args.noreplace:
            print('References will not be replaced (but highlighted)')
            args.highlight = True


        replace_references(args.DOCUMENT_ID, args.BIBTEX.name,
            args.CREDENTIALS.name, numindex=args.numbers, inplace=args.inplace,
            highlight=args.highlight, replace=not args.noreplace)

#!/usr/bin/env python

# Dataverse TSV metadata block parser
# Author: Tim DiLauro <timmo@jhu.edu>
# Parse metadata block and produce Solr copyField and/or field entries

from __future__ import print_function

import argparse
import csv

HEADER_PREFIX = '#'
SOLR_DFLT_TYPE = 'text_en'
SOLR_MAPPING = {'NONE': SOLR_DFLT_TYPE, 'DATE': 'string', 'EMAIL': 'email',
                'URL': SOLR_DFLT_TYPE, 'INT': SOLR_DFLT_TYPE,
                'TEXT': SOLR_DFLT_TYPE, 'TEXTBOX': SOLR_DFLT_TYPE,
                'FLOAT': SOLR_DFLT_TYPE}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--copyfield', action="store_true",
                        help="print <copyField> entries")
    parser.add_argument('-f', '--field', action="store_true",
                        help="print <field> entries")
    parser.add_argument('files', nargs='+',
                        help='metadata block files to process...')
    args = parser.parse_args()

    for spec_file in args.files:
        mdblock = parse_mdblock(spec_file)
        mdblock_name = mdblock['metadataBlock']['name']

        solr_entries = {field: fragment for field, fragment in
                        {field: generate_solr_fragments(mdblock['datasetField'][field]['entry'],
                                                        current_mdblock=mdblock_name)
                            for field in mdblock['datasetField'].keys()}.items()
                        if fragment is not None}
        if not args.copyfield and not args.field:
            print("no fields specified")
        # print('\n*** solr copyFields ***')
        if args.copyfield:
            for field, entry in solr_entries.items():
                print(entry[0])
        # print('\n*** solr fields ***')
        if args.field:
            for field, entry in solr_entries.items():
                print(entry[1])


def parse_mdblock(mdblock_file):
    header_prefix_len = len(HEADER_PREFIX)
    with open(mdblock_file, 'r') as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        state = None
        lengths = {'metadataBlock': 3, 'datasetField': 15, 'controlledVocabulary': 4}
        mdblock = {'metadataBlock': {},
                   'datasetField': {}, }
        headings = None
        for entry in tsvreader:
            # todo: need to deal with empty line
            # check for heading line
            entry_type = entry.pop(0)
            if entry_type.startswith(HEADER_PREFIX):
                state = entry_type[header_prefix_len:]
                headings = [h.strip() for h in entry[:lengths[state]]]
            else:
                mdb_entry = encode_entry(entry, headings)
                if state == 'metadataBlock':
                    mdblock[state] = mdb_entry
                elif state == 'datasetField':
                    parent = mdb_entry['parent']
                    if parent != '' and mdblock[state][parent]['entry']['allowmultiples'].upper() == 'TRUE':
                        mdb_entry['parent_multi'] = True
                    else:
                        mdb_entry['parent_multi'] = False
                    mdblock[state].update({mdb_entry['name']: {'entry': mdb_entry, 'cvocab': []}})
                elif state == 'controlledVocabulary':
                    mdblock['datasetField'][mdb_entry['DatasetField']]['cvocab'].append(mdb_entry)
    return mdblock


def encode_entry(entry, fields):
    return {fields[i]: entry[i].strip() for i in range(len(fields))}


def generate_solr_fragments(entry, current_mdblock=None):
    # note that most true/false values are strings, but parent_multi is boolean
    multi = entry['allowmultiples'].lower() == 'true' or entry['parent_multi']
    solr_type = SOLR_MAPPING[entry['fieldType'].upper()]

    # Don't generate entries for fields not in the current mdblock
    if current_mdblock is None or entry['metadatablock_id'] == current_mdblock:
        cfld = '<copyField source="{field}" dest="text" maxChars="3000"/>'.format(
            field=entry['name'],
        )
        fld = '<field name="{field}" type="{solr_type}" multiValued="{multi}" stored="true" indexed="true"/>'.format(
            field=entry['name'], solr_type=solr_type, multi='true' if multi else 'false',
        )
        return cfld, fld
    else:
        return None


"""
sb.append("   <field name=\"" + nameSearchable + "\" type=\"" + type +
"\" multiValued=\"" + multivalued + "\" stored=\"true\" indexed=\"true\"/>\n");



Multivalued if either field or its parent is (or both are) maltivalued.
"""


if __name__ == '__main__':
    main()

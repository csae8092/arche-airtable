#!/usr/bin/env python
# coding: utf-8

import os
import pandas as pd
from pyairtable import Base
from rdflib import Graph, URIRef, Literal, XSD
from rdflib.namespace import RDF
from rdflib import Namespace

ACDH_NS = Namespace("https://example.org/")
API_KEY = os.environ.get("AIRTABLE_API_KEY")
BASE_ID = os.environ.get('BASE_ID', 'app6E6a4FoH5RjZsc')
VALUES = {
    'object_date_value': 'date',
    'object_text_value': 'string',
    'object_uri': 'uri',
    'object_class_value': 'class'
}
base = Base(API_KEY, BASE_ID)
predicate_table = base.get_table('ArcheObjects')
rows = [x['fields'] for x in predicate_table.all()]
df = pd.DataFrame(rows)
g = Graph()
for i, row in df.iterrows():
    sub = URIRef(row['subject'])
    obj = ()
    for key, value in VALUES.items():
        try:
            obj = (row.dropna()[key], value)
        except KeyError:
            continue
    if obj[1] == 'string':
        g.add((sub, ACDH_NS[row['predicate_value'][0]], Literal(obj[0])))
    elif obj[1] == 'date':
        g.add((sub, ACDH_NS[row['predicate_value'][0]], Literal(obj[0], datatype=XSD.date)))
    elif obj[1] == 'uri':
        g.add((sub, ACDH_NS[row['predicate_value'][0]], URIRef(obj[0])))
    elif obj[1] == 'class':
        g.add((sub, RDF.type, ACDH_NS[row['object_class_value'][0]]))

g.serialize('tmp_out.ttl')

import os
from pyairtable import Base
from rdflib import Graph, URIRef
from utils import make_predicate, make_object, yield_triple

API_KEY = os.environ.get("AIRTABLE_API_KEY")
BASE_ID = os.environ.get('BASE_ID', 'app6E6a4FoH5RjZsc')
base = Base(API_KEY, BASE_ID)
main_table = base.get_table('ArcheObjects')
g = Graph()
for x in yield_triple(main_table):
    sub = URIRef(x['sub'])
    pred = make_predicate(x['pred'])
    obj = make_object(x)
    print(sub, pred, obj)
    g.add(
        (sub, pred, obj)
    )

g.serialize('tmp_out.ttl')
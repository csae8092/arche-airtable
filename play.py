import os
from pyairtable import Base
from rdflib import Graph
from utils import create_graph

API_KEY = os.environ.get("AIRTABLE_API_KEY")
BASE_ID = os.environ.get('BASE_ID', 'app6E6a4FoH5RjZsc')
base = Base(API_KEY, BASE_ID)
airtable = base.get_table('ArcheObjects')
g = Graph()
create_graph(g, airtable)

g.serialize('tmp_out.ttl')
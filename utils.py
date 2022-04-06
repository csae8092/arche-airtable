from rdflib import Namespace

from rdflib import URIRef, Literal, XSD
from rdflib.namespace import RDF


ACDH_NS = Namespace("https://vocabs.acdh.oeaw.ac.at/acdh#")


def get_lang_tag(value, sep='@@@'):
    if sep in value:
        lang = value.split(sep)[-1]
        new_value = value.replace(f"{sep}{lang}", "")
        return lang, new_value
    else:
        return '', value


def yield_triple(table):
    for x in table.iterate():
        for y in x:
            fields = y['fields']
            try:
                obj_key = [x for x in fields.keys() if '___' in x][0]
            except IndexError:
                continue
            try:
                triple = {
                    "sub": fields['subject'],
                    "pred": fields['predicate_value'][0],
                    "obj_val": fields[obj_key],
                    "obj_key": obj_key
                }
            except KeyError:
                continue
            yield triple


def make_object(triple):
    obj_type = triple['obj_key'].split('___')[1]
    if obj_type == 'string':
        lang_tag = get_lang_tag(triple['obj_val'])
        if lang_tag[0]:
            obj = Literal(lang_tag[1], lang=lang_tag[0])
        else:
             obj = Literal(triple['obj_val'])
    elif obj_type == 'date':
        obj = Literal(triple['obj_val'], datatype=XSD.date)
    elif obj_type == 'uri':
        obj = URIRef(triple['obj_val'])
    elif obj_type == 'class':
        obj = ACDH_NS[triple['obj_val'][0]]
    return obj


def make_predicate(pred_val):
    if pred_val.startswith('rdf'):
        return RDF.type
    else:
        return ACDH_NS[pred_val]

def create_graph(g, airtable):
    for x in yield_triple(airtable):
        sub = URIRef(x['sub'])
        pred = make_predicate(x['pred'])
        obj = make_object(x)
        print(sub, pred, obj)
        g.add(
            (sub, pred, obj)
        )
    return g

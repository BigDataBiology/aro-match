import pronto
import typing

_name2id = None
def lazy_load_name2id():
    global _name2id
    if _name2id is None:
        aro = pronto.Ontology('./aro.owl')

        name2id = {}
        for t in aro.terms():
            name2id[t.name] = t.id
            for syn in t.synonyms:
                assert syn.scope == 'EXACT'
                name2id[syn.description] = t.id

        # Normalize by converting to lower case
        _name2id = {k.lower():v for k,v in name2id.items()}

        # Check that there were no conflicts introduced by the case conversion
        if len(name2id) != len(_name2id):
            print("Case normalization introduced conflicts")
    return _name2id

def try_match(gene : str) -> typing.Optional[str]:
    '''Attempt to match gene name based on some simple heuristics

    Parameters
    ----------
    gene : str

    Returns
    -------
    aro : str (or None)
        Corresponding ARO ID (if found)
    '''
    import re
    name2id = lazy_load_name2id()

    key = gene.lower()
    # resfinder:blaLEN1 is encoded as LEN-1 in ARO (note the "-")
    if key.startswith('blalen'):
        key = key.replace('blalen', 'len-')
    elif key.startswith('bla'):
        key = key[3:]
    # Erm(A) is encoded as "ErmA"
    elif re.match(r'erm\(.\)', key):
        key = re.sub(r'erm\((.)\)',r'erm\1', key)
    elif re.match(r'^tet\((.)\)$', key):
        key = re.sub(r'tet\((.)\)',r'tet\1', key)
    if key in name2id:
        return name2id[key]


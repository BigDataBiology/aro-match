import re
import pronto

aro = pronto.Ontology('./aro.owl')

name2id = {}
for t in aro.terms():
    name2id[t.name] = t.id
    for syn in t.synonyms:
        assert syn.scope == 'EXACT'
        name2id[syn.description] = t.id

# Normalize by converting to lower case
name2id = {k.lower():v for k,v in name2id.items()}

matched = []
unmatched = []
for line in open('resfinder_db/notes.txt'):
    if line[0] != '#':
        gene = line.split(':')[0]
        key = gene.lower()
        # blaLEN1 is encoded as LEN-1 (note the "-")
        if key.startswith('blalen'):
            key = key.replace('blalen', 'len-')
        elif key.startswith('bla'):
            key = key[3:]
        # Erm(A) is encoded as "ErmA"
        elif re.match(r'erm\(.\)', key):
            key = re.sub(r'erm\((.)\)',r'erm\1', key)
        if key in name2id:
            matched.append(gene)
        else:
            unmatched.append(gene)

frac = (len(matched)/(len(unmatched)  + len(matched)))
print(f'Matched {len(matched)} of {len(matched)+len(unmatched)} ({frac:.2%}) of identifiers')



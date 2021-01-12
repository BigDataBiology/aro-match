from by_name import try_match
matched = {}
unmatched = []
for line in open('resfinder_db/notes.txt'):
    if line[0] != '#':
        gene = line.split(':')[0]
        aro = try_match(gene)
        if aro is not None:
            matched[gene] = aro
        else:
            unmatched.append(gene)
frac = (len(matched)/(len(unmatched)  + len(matched)))
print(f'Matched {len(matched)} of {len(matched)+len(unmatched)} ({frac:.2%}) of identifiers')




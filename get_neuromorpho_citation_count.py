import requests
import json

data = json.loads(requests.get('http://neuromorpho.org:8081/literature/query/Specific_Details&=&In%20the%20repository').text)['data']

neuromorpho_citation_counts = {}

def increment_citation_count(key, count):
    # reject invalid keys before starting
    if key is None or key <= 0: return
    if key in neuromorpho_citation_counts:
        neuromorpho_citation_counts[key] += count
    else:
        neuromorpho_citation_counts[key] = count

related_pages = {}

for item in data:
    increment_citation_count(item['PMID'], item['No_of_Reconstructions'])
    increment_citation_count(item['Related_Page'], item['No_of_Reconstructions'])
    if item['Related_Page'] and item['Related_Page'] > 0:
        pmid = item['PMID']
        related_pmid = item['Related_Page']
        if pmid not in related_pages:
            related_pages[pmid] = [related_pmid]
        else:
            related_pages[pmid].append(related_pmid)
        if related_pmid not in related_pages:
            related_pages[related_pmid] = [pmid]
        else:
            related_pages[related_pmid].append(pmid)

# ensure all the related pages have the same values
change = True
while change:
    change = False
    for item, value in related_pages.iteritems():
        value = max([neuromorpho_citation_counts[item], max([neuromorpho_citation_counts[i] for i in value])])
        if value != neuromorpho_citation_counts[item]:
            neuromorpho_citation_counts[item] = value
            change = True

with open('neuromorpho_citation_count.json', 'w') as f:
    f.write(json.dumps(neuromorpho_citation_counts))
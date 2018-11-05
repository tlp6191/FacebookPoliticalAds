import csv
import re
import sys
csv.field_size_limit(sys.maxsize)

with open('SAT') as f:
	sat = f.readlines()
sat = [s.strip().lower() for s in sat]
sat = re.compile("|".join([s+"\b|\b"+s for s in sat]))
with open('GRE') as f:
	gre = f.readlines()
gre = [s.strip().lower() for s in gre]
gre = re.compile("|".join([s+"\b|\b"+s for s in gre]))

with open('fbpac-ads-en-US.csv') as f:
	r = list(csv.DictReader(f))
#	r = r[1:100]
	keys = ['title','message','lang','impressions','political_probability','advertiser','paid_for_by','listbuilding_fundraising_proba','maxage','minage','US politics','gre','sat','targets']
	counts = {'gre':gre,'sat':sat}
	sep = "|"
	print(sep.join(keys))
	extracted = {'US politics':re.compile('"target": "Segment", "segment": "US politics \((.*?)\)"'),'maxage':re.compile('"target": "MaxAge", "segment": "(\d+)"'),'minage':re.compile('"target": "MinAge", "segment": "(\d+)"')}
	for x in r:
		for e in extracted.keys():
			m = extracted[e].finditer(x['targets'])
			x[e] = ",".join(sorted([match.group(1) for match in m]))
	for x in r:
		for c in counts.keys():
			x[c] = str(len(counts[c].findall(x['message'].lower())))
	for x in sorted(r,key=lambda x: -1*int(x['impressions'])*float(x['political_probability'])):
		print(sep.join([x[k].replace("|","").replace("\n","") for k in keys]))

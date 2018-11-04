import csv
import re
import sys
csv.field_size_limit(sys.maxsize)

with open('fbpac-ads-en-US.csv') as f:
	r = list(csv.DictReader(f))
	keys = ['title','message','lang','impressions','political_probability','advertiser','paid_for_by','listbuilding_fundraising_proba','targets','maxage','minage','US politics']
	sep = "|"
	print(sep.join(keys))
	extracted = {'US politics':re.compile('"target": "Segment", "segment": "US politics \((.*)\)"'),'maxage':re.compile('"target": "MaxAge", "segment": "(\d+)"'),'minage':re.compile('"target": "MinAge", "segment": "(\d+)"')}
	for x in r:
		for e in extracted.keys():
			m = extracted[e].match(x['targets'])
			if m:
				r[e] = m.group(1)
			else:
				r[e] = ''
			
	for x in sorted(r,key=lambda x: int(x['impressions'])*float(x['political_probability'])):
		print(sep.join([x[k].replace("","") for k in keys]))


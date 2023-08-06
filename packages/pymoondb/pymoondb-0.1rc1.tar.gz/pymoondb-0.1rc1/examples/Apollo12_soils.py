#!/usr/bin/env python3

import moondb,sys

# Let's setup the data filter
f = moondb.AnalysisFilter()
f.mission = ["Apollo 12"]
f.analyte = ["Na2O","CaO"]
f.specimenType = ["SOIL"]
# retreive the results
results = f.get_results()

for r in results:
   print('\nDataset: ',r.dataset) 
   print('Lab,Specie,value')
   for dr in r.dataResults:
      print(",".join([dr.laboratory,dr.variable,dr.value+dr.unit]))
      



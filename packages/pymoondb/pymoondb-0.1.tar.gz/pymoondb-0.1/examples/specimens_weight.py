import moondb,sys


# Get all the scientific missions held in MoonDB
moon_missions = moondb.get_missions()

weight_cum = 0
for m in moon_missions:
   s = moondb.SpecimenFilter()
   s.missionName = [ m.name ]
   res = s.get_results()
   weight = 0
   for r in res:
      if r.weight is not None:
         weight += float(r.weight.split(' ')[0])
   weight_cum += weight
   print("MoonDB holds {:.3f} kg of specimens from {}".format(weight/1000.0,m.name))

print("MoonDB contains a total of {:.3f} kg of specimen from the Moon!".format(weight_cum/1000.0))


f = moondb.AnalysisFilter()
f.mission = ["Apollo 11"]
f.analyte = ["Na2O","CaO"]
f.specimenType = ["SOIL"]



results = f.get_results()

for r in results:
   for dr in r.dataResults:
      print(dr)
      #print(dr.laboratory,dr.variable,dr.value,dr.unit)
      



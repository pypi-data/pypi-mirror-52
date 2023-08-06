#!/usr/bin/python3
# 
# (c) 2019 Alessandro Frigeri, Istituto Nazionale di Astrofisica
# 
# MoonDB Python module
# https://realpython.com/api-integration-in-python/

import sys
import json 
import urllib.parse
import urllib3,socket
import logging
from dataclasses import dataclass
from collections import namedtuple

import requests
#import attr

class Mission:
   def __init__(self,name):
      self.name = name
   def __str__(self):
      return self.name

@dataclass
class Landmark:
   """The Landmark class"""
   name: str
   GPNFID: int
   GPNFURL: str
   latitude: float
   longitude: float

   def asWkt(self):
      point = "POINT ({} {})"
      return point.format(self.longitude,self.latitude)

@dataclass
class Specimen:
   specimenCode: str
   specimenName: str
   parentSpecimen: str
   childSpecimens: list
   specimenType: str
   samplingTechnique: str
   mission: str
   landmark: str
   lunarStation: str
   returnContainer: str
   weight: str
   pristinity: str
   pristinityDate: str
   description: str


class SpecimenType:
   def __init__(self,name):
      self.name = name
   def __str__(self):
      return self.name
   def __repr__(self):
      return self.name

class SamplingTechnique:
   def __init__(self,name):
      self.name = name
   def __str__(self):
      return self.name
   def __repr__(self):
      return self.name

class AnalyzedMaterial:
   def __init__(self,name):
      self.name = name
   def __str__(self):
      return self.name
   def __repr__(self):
      return self.name

class Analyte:
   def __init__(self,name):
      self.name = name
   def __str__(self):
      return self.name
   def __repr__(self):
      return self.name

class AnalysisMethod:
   def __init__(self,code,name):
      self.name = name
      self.code = code
   def __str__(self):
      return self.name
   def __repr__(self):
      return self.name


class AnalyisMethod:
   def __init__(self,name):
      self.name = name

class Analysis:
   __slots__ = ('analysisCode','analyzedMaterial','comment','dataset','citation','dataResults')

class DataResult:
   __slots__ = ('unit', 'laboratory', 'variable', 'methodName', 'methodComment', 'value', 'methodCode')

def _url(path):
   return "http://api.moondb.org" + urllib.parse.quote(path)

def _check_resp(resp):
   if resp.status_code != 200:
      #raise ApiError('Cannot fetch all objects: {}'.format(resp.status_code))
      pass

def _get_resp(path):
   try:
      resp = requests.get(_url( path ), timeout=1)
   except requests.exceptions.ReadTimeout: # urllib3.exceptions.ReadTimeoutError:
      print("no response in timeout time")
      logging.warning('no response in timeout time')
      sys.exit(0)
   except requests.exceptions.ConnectTimeout:
      print("no response in timeout time")
      logging.warning('no response in timeout time')
      sys.exit(0)
   _check_resp(resp)
   r = resp.json()
   #print(r)
   # To be checked with Peng
   #if 'result' and 'count' in r:
   #   return r['count'],r['result']
   if 'results' and 'count' in r:
      return r['count'],r['results']
   else:
      return r



def _json_object_hook(d): 
   return namedtuple('X', d.keys())(*d.values())

def json2obj(data): 
   return json.loads(data, object_hook=_json_object_hook)


def get_specimens(sc=None,mn=None,ln=None,sty=None,ste=None):
   '''
   Returns the specimen by specifying:
   
   :param sc: sample code string 
   :type sc: list
   :param mn: mission name e.g. 'Apollo 11'
   :type mn: list
   :return: something
   :rtype: string
   :raises: TypeError
   
   Parameters
   ----------
   sc: list 
       list of specimen codes
   mn: list
       list of mission names
   ln: list
       list of landmark names
   sty: list
       list of specimen types
   ste: list
       list of sampling techniques
   '''
   #print(mn)
   sp_list = []
   if sc:
      for s in sc: 
         spec = _get_resp('/specimen/'+s) 
         sp_list.append(spec)
   if mn:
      for n in mn:
         count,spec = _get_resp('/specimenlist/mission/'+n) 
         sp_list.extend(spec)

   if ln:
      for n in ln:
         count,spec = _get_resp('/specimenlist/mission/'+n) 
         sp_list.extend(spec)

   if sty:
      for st in sty:
         count,spec = _get_resp('/specimenlist/mission/'+st) 
         sp_list.extend(spec)

   if ste:
      for st in ste:
         count,spec = _get_resp('/specimenlist/mission/'+st) 
         sp_list.extend(spec)

   sp_obj_list = []

   for s in sp_list:
      # dict unpack
      # print(s)
      s_o = Specimen(**s)
      sp_obj_list.append(s_o)

   return sp_obj_list


def get_missions():
   missions = []
   resp = requests.get(_url('/authorities/missions/'))
   _check_resp(resp)
   for m_item in resp.json()['results']:
      missions.append( Mission(m_item['name'] ))
   return missions

## Controlled Vocabularies

def get_specimentypes():
   st_list = []
   count,st = _get_resp('/cv/specimentypes') 
   for s in st:
      stobj = SpecimenType(s['name'])
      st_list.append(stobj)
   return st_list

def get_samplingtechniques():
   st_list = []
   count,st = _get_resp('/cv/samplingtechniques') 
   for s in st:
      stobj = SamplingTechnique(s['name'])
      st_list.append(stobj)
   return st_list

def get_analyzedmaterials():
   st_list = []
   count,st = _get_resp('/cv/analyzedmaterials') 
   for s in st:
      stobj = AnalyzedMaterial(s['name'])
      st_list.append(stobj)
   return st_list

def get_analytes():
   analytes = []
   count,an = _get_resp('/cv/analyzedmaterials') 
   for a in an:
      analytes.append( Analyte(m_item['name'] ))
   return analytes

def get_analysismethods():
   am_list = []
   count,am = _get_resp('/cv/analysismethods') 
   for a in am:
      aobj = AnalysisMethod(s['name'])
      am_list.append(aobj)
   return am_list

def get_landmarks():
   lm_list = []
   count,lmlist = _get_resp('/authorities/landmarks') 
   for l in lmlist:
      lobj = Landmark(**l)
      lm_list.append(lobj)
   return lm_list

def get_landmark( landmark_name ):
   lms = get_landmarks()
   for l in lms:
      if l.name == landmark_name:
         return l
   return None

def get_samplingtechnique():
   pass


class dataFilter:
   def __init__(self):
      pass
   def _toJSON(self):
      return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True,separators=(",", ":"))

@dataclass
class SpecimenFilter:
   specimenCode: list = None
   missionName: list = None
   landmarkName: list = None
   specimenType: list = None
   samplingTechnique: list = None

   def get_results(self):
      res_list = get_specimens(sc=self.specimenCode,
                               mn=self.missionName,
                               ln=self.landmarkName,
                               sty=self.specimenType,
                               ste=self.samplingTechnique)
      return res_list

class AnalysisFilter:
   def __init__(self):
      self.mission = []
      self.landmark = []
      self.specimenType = []
      self.samplingTechnique = []
      self.analyzedMaterial = []
      self.analyte = []
      self.analysisMethod = []
   def _toJSON(self):
      return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True,separators=(",", ":"))

   def get_results(self):
      """
      A method's docstring with parameters and return value.
     
      Use all the cool Sphinx capabilities in this description, e.g. to give
      usage examples ...
      
      :Example:
      
      >>> another_class.foo('', AClass())        
      
      :param arg1: first argument
      :type arg1: string
      :param arg2: second argument
      :type arg2: :class:`module.AClass`
      :return: something
      :rtype: string
      :raises: TypeError
      """
      resp = requests.get(_url('/data/'+self._toJSON() ))
      res_list = []
      
      for r in resp.json()['results']:
         rd = dict(r)
         analysis = namedtuple("Analysis", rd.keys())(*rd.values())
         data_res_list = []
         for r in analysis.dataResults:
            data_res = namedtuple("dataResult", r.keys())(*r.values())
            data_res_list.append(data_res)
         analysis = analysis._replace(dataResults = data_res_list )
         res_list.append(analysis) 
      return res_list


if __name__ == "__main__":
   m = get_missions()
   f = AnalysisFilter()
   f.specimenType = ["SOIL"]
   f.analyte = ["H2O","Ti"]
   f.mission = ["Apollo 11"]
   print(80*"#")
   #print f.toJSON()
   results = f.get_results()
   for r in results:
       this_res = r['dataResults'][0]
       var = this_res['variable']
       val = this_res['value']
       unit = this_res['unit']
       print(var,": ",val,unit)

   s = get_specimen(mn=['Apollo 12','Apollo 11'])
   print(len(s))
   s1 = s[0]

   m = get_missions()
   ml = []
   for mn in m:
      ml.append(mn.name)
   s = get_specimen(mn=ml)
   print(len(s))
   s1 = s[0]
   #s1.say_hello()
   #print(type(s1))
   #for sp in s:
   #   print(sp['specimenName'])
   #sp_types = get_specimentypes()
   #print(sp_types)




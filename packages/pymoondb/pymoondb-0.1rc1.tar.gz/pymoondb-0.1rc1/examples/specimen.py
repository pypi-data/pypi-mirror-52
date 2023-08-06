#!/usr/bin/env python3

import moondb

s_12023 = moondb.get_specimens(sc=['12023'])[0]

#print(s_12023)

child = moondb.get_specimens(sc=['12023,114'])[0]

#print(' A N A L Y S E S ')
a = child.get_analyses()


print(a[0])

a0_results = a[0].dataResultsObj


print('Result: {} {} {}'.format(a0_results[0].variable,a0_results[0].value,a0_results[0].unit,a0_results[0].methodName))



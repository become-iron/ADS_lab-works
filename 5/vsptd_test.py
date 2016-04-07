# -*- coding: utf-8 -*-
from vsptd import Triplet, TripletString
from math import sin, cos, tan, atan
# print(Triplet(4, 'd', 'dsad'))
# meow = Triplet('G', 'V', 324.6)
_ = TripletString(Triplet('G', 'V', 'fdd'), Triplet('W', 'R', 'fdd'), Triplet('T', 'V', 'dsad'), Triplet('J', 'R', 'dsad'))
# trpString2 = TripletString(Triplet('d', 'n', 'dsad'), Triplet('u', 't', 'dsad'))
# print(*exampleTrpString)
# for i in exampleTrpString:
#     print(i)
# print(exampleTrpString)
# print(exampleTrpString + Triplet('h', 'q', 'fdsf'))
# print(exampleTrpString['dsfs'])
# b=TripletString()
print(_.check_condition('$g.v = $w.r'))

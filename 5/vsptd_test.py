# -*- coding: utf-8 -*-

from vsptd import Triplet, TripletString

# print(Triplet(4, 'd', 'dsad'))
# meow = Triplet('G', 'V', 324.6)
# trpString2 = TripletString(Triplet('d', 'n', 'dsad'), Triplet('u', 't', 'dsad'))
# print(*exampleTrpString)
# for i in exampleTrpString:
#     print(i)
# print(exampleTrpString)
# print(exampleTrpString + Triplet('h', 'q', 'fdsf'))
# print(exampleTrpString['dsfs'])
# b=TripletString()

_ = TripletString(Triplet('G', 'V', True), Triplet('W', 'R', 'fdd'), Triplet('T', 'V', 'dsad'), Triplet('J', 'R', 'dsad'))
print(_.check_condition('нет($i.trv) = есть($w.r) и ($t.v != $g.v)'))

#!/usr/bin/env python3.6

import pickle
with open("list.pickle",'rb') as fr:
	data = pickle.load(fr)


def mid(tlen_list):
	if len(tlen_list) == 0:
		return "empty"
	else:
		tlen_list.sort()
		midium = 0
		num = len(tlen_list)
		if num%2 == 1:
			num = num//2
			midium = tlen_list[num]
		else:
			num = num//2
			midium = (tlen_list[num-1]+tlen_list[num])/2
		return midium

print("--------------------------------------")
print("median TLEN is", mid(data))
print("--------------------------------------")

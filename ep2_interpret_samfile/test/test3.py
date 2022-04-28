#!/usr/bin/env python3.6

import sys
file = sys.argv[1]

import pickle
with open("dict.pickle",'rb') as fr:
	data = pickle.load(fr)


print(data)


list1 = []
for k,v in data.items():
	for i in range(v):
		list1.append(k)

with open("list.pickle",'wb') as fw:
	pickle.dump(list1,fw)


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


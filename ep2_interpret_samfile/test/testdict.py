#!/usr/bin/env python3.6

# function for get median 
def med_TLEN(dict_TLEN):
	cnt_TLEN = sum(dict_TLEN.values())
	p_med = (cnt_TLEN+1)/2
	dict_TLEN_sorted = sorted(dict_TLEN.items(),key=lambda item:item[0])
	
	total_cnt =0
	before_TLEN =0
	med =0
	for TLEN, cnt in dict_TLEN_sorted:
		if total_cnt < p_med: # in before case 
			med = (TLEN + before_TLEN)/2
		total_cnt += cnt
		if total_cnt > p_med:
			med = TLEN
			break
		else:
			before_TLEN = TLEN
	return med

import pickle
with open("dict.pickle","rb") as fr:
	data = pickle.load(fr)



print("-------------------------------------")
print("- median TLEN in FR",med_TLEN(data))
print("-------------------------------------")


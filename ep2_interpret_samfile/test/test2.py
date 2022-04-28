#!/usr/bin/env python3.6

import sys
f = sys.argv[1]

# The number of all read pairs

FR_TLEN = {}
RF_TLEN = {}

for line in open(f,'r'):
	if line[0] != '@':
		aln_info = line.split('\t')
		FLAG = int(aln_info[1])
		TLEN = int(aln_info[8])

		# FR/RF classification
		if FLAG & 3840 == 0 and FLAG & 67 == 67: # exclude not properly pair / properly & first in pair
			if FLAG & 99 == 99: # mate reverse strand
				if TLEN >0: #FR
					if TLEN in FR_TLEN.keys():
						FR_TLEN[TLEN]+=1
					else:
				 		FR_TLEN[TLEN]=1
				elif -TLEN in RF_TLEN.keys(): #RF
					RF_TLEN[-TLEN]+=1
				else:
					RF_TLEN[-TLEN]=1
			elif FLAG & 83 == 83: # read reverse strand
				if TLEN >0: #FR
					if TLEN in RF_TLEN.keys():
						RF_TLEN[TLEN]+=1
					else:
						RF_TLEN[TLEN]=1
				elif -TLEN in FR_TLEN.keys(): #RF
					FR_TLEN[-TLEN] +=1
				else:
					FR_TLEN[-TLEN]=1

# function for get median 
def med_TLEN(dict_TLEN):
	cnt_TLEN = sum(dict_TLEN.values())
	p_med = (cnt_TLEN+1)/2
	dict_TLEN_sorted = sorted(dict_TLEN.items(),key=lambda item:item[0])
	
	total_cnt =0
	before_TLEN =0
	med =0
	suzy = []
	for TLEN, cnt in dict_TLEN_sorted:
		suzy.append(total_cnt)
		if total_cnt < p_med: # in before case 
			med = (TLEN + before_TLEN)/2
		total_cnt += cnt
		if total_cnt > p_med:
			med = TLEN
			break
		else:
			before_TLEN = TLEN
	print(suzy)
	return med

import pickle
with open("dict.pickle","wb") as fw:
	pickle.dump(FR_TLEN,fw)

'''
print("-------------------------------------")
print("- median TLEN in FR",med_TLEN(FR_TLEN))
print("- median TLEN in RF",med_TLEN(RF_TLEN))
print("-------------------------------------")
'''

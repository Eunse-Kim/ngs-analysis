#!/usr/bin/env python3.6

import sys
f = sys.argv[1]

# The number of all read pairs

FR_TLEN = {}
RF_TLEN = {}
chr_dict = {} #{'chr1':{'FR': -, 'RF': -}, 'chr2':{'FR':-,'RF':-}}
 

for line in open(f,'r'):
	if line[0] != '@':
		aln_info = line.split('\t')
		FLAG = int(aln_info[1])
		TLEN = int(aln_info[8])
		RNAME = aln_info[2]

		# chr & FR/RF classification
		if FLAG & 3840 == 0 and FLAG & 67 == 67: # exclude not properly pair / properly & first in pair
			if not RNAME in chr_dict: # chr classification
				chr_dict[RNAME] = {'FR':0, 'RF':0}
			if FLAG & 99 == 99: # mate reverse strand
				if TLEN >0: #FR
					if TLEN in FR_TLEN.keys():
						FR_TLEN[TLEN]+=1
					else:
				 		FR_TLEN[TLEN]=1
					chr_dict[RNAME]['FR']+=1
				elif -TLEN in RF_TLEN.keys(): #RF
					RF_TLEN[-TLEN]+=1
				else:
					RF_TLEN[-TLEN]=1
				chr_dict[RNAME]['RF']+=1
			elif FLAG & 83 == 83: # read reverse strand
				if TLEN >0: #FR
					if TLEN in RF_TLEN.keys():
						RF_TLEN[TLEN]+=1
					else:
						RF_TLEN[TLEN]=1
					chr_dict[RNAME]['FR']+=1
				elif -TLEN in FR_TLEN.keys(): #RF
					FR_TLEN[-TLEN] +=1
				else:
					FR_TLEN[-TLEN]=1
				chr_dict[RNAME]['RF']+=1

# function for get median 
def med_TLEN(dict_TLEN):
	cnt_TLEN = sum(dict_TLEN.values())
	p_med = (cnt_TLEN+1)/2
	dict_TLEN_sorted = sorted(dict_TLEN.items(),key=lambda item:item[0])
	
	total_cnt =0
	med = 0	
	before_TLEN = 0

	for TLEN, cnt in dict_TLEN_sorted:
		
		if total_cnt < p_med: # in before case 
			med = (TLEN + before_TLEN)/2
		total_cnt += cnt
		if total_cnt >= p_med:
			med = TLEN
			break

		else:
			before_TLEN = TLEN

	return med


# estimate insert length
cnt_FR = sum(FR_TLEN.values())
cnt_RF = sum(RF_TLEN.values())
if cnt_FR > cnt_RF:
	insert_len = med_TLEN(FR_TLEN)
else:
	insert_len = med_TLEN(RF_TLEN)

print("-------------------------------------")
print("#1. The numver of all read pairs is")
print("#2. FR information")
print("- # of properly-aligned read pairs is")
print("- median TLEN in FR",med_TLEN(FR_TLEN))
print("- fraction of FR is")
print("#3. RF information")
print("- # of properly-aligned read pairs is")
print("- median TLEN in RF",med_TLEN(RF_TLEN))
print("- fraction of RF is")
print("#4. Estimated insert length is", insert_len)
print("#5. Properly-aligned read pairs per each reference chromosomes")
print("-",chr_dict)
print("-------------------------------------")


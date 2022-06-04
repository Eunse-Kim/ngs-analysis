#!/usr/bin/env python3.6

import sys
f = sys.argv[1]

# The number of all read pairs

FR_TLEN = {}
RF_TLEN = {}
chr_dict = {} #{'chr1':{'FR': -, 'RF': -}, 'chr2':{'FR':-,'RF':-}}
cnt_all_pairs =0

for line in open(f,'r'):
	if line[0] != '@':
		aln_info = line.split('\t')
		FLAG = int(aln_info[1])
		TLEN = int(aln_info[8])
		RNAME = aln_info[2]
		QNAME = aln_info[0]
		
		if FLAG & 65 == 65 and FLAG & 3840 == 0: #read pair, first, not 4
			cnt_all_pairs +=1
		# chr & FR/RF classification
			if FLAG & 67==67: # properly
				if not RNAME in chr_dict: # chr classification
					chr_dict[RNAME] = {'FR':0, 'RF':0}
				if FLAG & 115 == 99: # mate reverse strand
					if TLEN >0: #FR
						chr_dict[RNAME]['FR']+=1
						if TLEN in FR_TLEN.keys():
							FR_TLEN[TLEN]+=1
						else:
							FR_TLEN[TLEN]=1
					else:
						chr_dict[RNAME]['RF']+=1
						if -TLEN in RF_TLEN.keys(): #RF
							RF_TLEN[-TLEN]+=1
						else:
							RF_TLEN[-TLEN]=1
				elif FLAG & 115 == 83: # read reverse strand
					if TLEN >0: #RF
						chr_dict[RNAME]['RF']+=1
						if TLEN in RF_TLEN.keys():
							RF_TLEN[TLEN]+=1
						else:
							RF_TLEN[TLEN]=1
					else:
						chr_dict[RNAME]['FR']+=1
						if -TLEN in FR_TLEN.keys(): #FR
							FR_TLEN[-TLEN] +=1
						else:
							FR_TLEN[-TLEN]=1

# function for get median 
def med_TLEN(dict_TLEN):
	cnt_TLEN = sum(dict_TLEN.values())
	p_med = (cnt_TLEN+1)/2
	dict_TLEN_sorted = sorted(dict_TLEN.items(),key=lambda item:item[0])
	
	total_cnt =0
	med = 0	
	before_TLEN = 0

	for TLEN, cnt in dict_TLEN_sorted:
		
		if total_cnt == int(p_med): # in before case 
			med = (TLEN + before_TLEN)/2
			break
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

# ---------------------------------------------------------------------------
# Result
print("===============================================================================")
print("The number of all read pairs :",cnt_all_pairs)
print("The number of properly-aligned FR read pairs : {} || median TLEN {} || ratio {}".format(cnt_FR,med_TLEN(FR_TLEN),round(cnt_FR/cnt_all_pairs,2)))
print("The number of properly-aligned RF read pairs : {} || median TLEN {} || ratio {}".format(cnt_RF,med_TLEN(RF_TLEN),round(cnt_RF/cnt_all_pairs,2)))
print("The estimated insert length :", insert_len)
print("===============================================================================")
print("The number and fraction of properly-aligned read pairs per each reference chromosomes")
print("-------------------------------------------------------------------------------")
print("chromosome\tFR(ratio)\tRF(ratio)")
print("-------------------------------------------------------------------------------")
for c,a in chr_dict.items():
	fr_cnt = a['FR']
	rf_cnt = a['RF']
	fr_frac = round(fr_cnt/cnt_all_pairs,3)
	rf_frac = round(rf_cnt/cnt_all_pairs,3)
	print("{}\t{}({})\t{}({})".format(c,fr_cnt,fr_frac,rf_cnt,rf_frac))
print("-------------------------------------------------------------------------------")


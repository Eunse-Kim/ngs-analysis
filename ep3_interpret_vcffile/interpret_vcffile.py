#!/usr/bin/env python3.6

import sys
f = sys.argv[1]

dic_num = {}
dic_len = {}

for line in open(f,'r'):
	if line[0] != '#':
		v_info = line.split('\t')
		CHR = v_info[0]
		REF = v_info[3]
		ALT = v_info[4]
		QUAL = float(v_info[5])
		INFO = v_info[7]
		info_list = INFO.split(';')
		
		#DP&AF definition
		for i in info_list:
			if 'DP=' in i:
				DP = float(i[3:])
			if 'AF=' in i:
				AF = float(i[3:])

		# requirement
		if ',' in ALT:
			continue
		if QUAL <20 or DP<20 or AF!=1:
			continue
		
		# REF/ALT Length definition
		ln_REF = len(REF)
		ln_ALT = len(ALT)

		# classification
		if not CHR in dic_num:
			dic_num[CHR] = {'SUB':0, 'INS':0, 'DEL':0}
			dic_len[CHR] = {'SUB':0, 'INS':0, 'DEL':0}
		if ln_REF < ln_ALT:
			dic_num[CHR]['INS'] +=1
			gap = ln_ALT-ln_REF
			dic_len[CHR]['INS'] += gap
		elif ln_ALT < ln_REF:
			dic_num[CHR]['DEL'] +=1
			gap = ln_REF-ln_ALT
			dic_len[CHR]['DEL'] += gap
		else:
			dic_num[CHR]['SUB'] +=1
			dic_len[CHR]['SUB'] +=1

# dictionary sorting
dic_num = dict(sorted(dic_num.items()))
dic_len = dict(sorted(dic_len.items()))


# function: print all chromosome
def print_all(dic):
	all_sub, all_ins, all_del = 0,0,0
	for n in dic.values():
		all_sub += n['SUB']
		all_ins += n['INS']
		all_del += n['DEL']
	print("-For all chromosomes")
	print("SUB\tINS\tDEL")
	print("{}\t{}\t{}".format(all_sub, all_ins, all_del))

# function: print each chrmosome
def print_each(dic):
	print("-For each chromosome")
	print("CHROM\tSUB\tINS\tDEL")
	for c, n in dic.items():
		print("{}\t{}\t{}\t{}".format(c,n['SUB'],n['INS'],n['DEL']))

# result
print("===== The number of substitutions, insertions, and deletions =====")
print_all(dic_num)
print_each(dic_num)
print("\n===== The total length of substitutions, insertions, deletions =====")
print_all(dic_len)
print_each(dic_len)	

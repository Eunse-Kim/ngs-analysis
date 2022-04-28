#!/usr/bin/env python3.6

import sys
file = sys.argv[1]


cnt =0
for i in open(file,'r'):
	if i[0] != '@':
		aln_info = i.split('\t')
		if int(aln_info[1]) &83== 83: #1,2,16,64 만족
			if int(aln_info[8]) ==0: #tlen이 0인 값
				print(aln_info)
				break


			

'''
#list1 = [i for i in name.values() if i>2 ]
list1 = [i for i in name.values() if i > 2]
'''

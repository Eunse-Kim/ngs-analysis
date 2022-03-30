#!/usr/bin/env python3.6

import sys
f = sys.argv[1]

# The number of reads and bases

seq_ln_list=[]
ln =0
with open(f,'r') as file:
	for line in file.readlines():
		ln += 1
		if ln%4 == 2:
			seq_ln = len(line.rstrip())
			seq_ln_list.append(seq_ln)
num = ln/4
seq_ln_total=sum(seq_ln_list)
print()
print("[The number of reads and bases]")
print("- This file includes",int(num), "reads and",seq_ln_total,"bases.")
print()

# The distribution of read lengths

mean = seq_ln_total/num
deviations = [(i-mean)**2 for i in seq_ln_list]
var = sum(deviations)/len(deviations)
sd = var**(1/2)

seq_ln_list.sort()
p_q1 = int((num+1)/4)
p_median= int(2*(num+1)/4)
p_q3 = int(3*(num+1)/4)


## Q2(median)
if (num+1)%2 == 0:
	median = seq_ln_list[p_median-1]
else:
	median = (seq_ln_list[p_median-1]+seq_ln_list[p_median])/2

## Q1 & Q3
if (num+1)%4 ==0:
	q1 = seq_ln_list[p_q1-1]
	q3 = seq_ln_list[p_q3-1]
else:
	q1 = (seq_ln_list[p_q1-1]+seq_ln_list[p_q1])/2
	q3 = (seq_ln_list[p_q3-1]+seq_ln_list[p_q3])/2


print("[Distibution of read lengths]")
print("- The mean is {}.".format(mean))
print("- The standard deviation is {}.".format(sd))
print("- 1st qualtile: {}, 2nd qualtile(median): {}, 3rd qualtile: {}, 4th qualtile: {}".format(int(q1),int(median),int(q3),seq_ln_list[-1]))
print()


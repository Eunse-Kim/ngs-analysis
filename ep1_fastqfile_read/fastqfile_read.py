#!/usr/bin/env python3.6

import sys
f = sys.argv[1]

#1. The number of read sequences

with open(f,'r') as file:
	ln = len(file.readlines())
	num = int(ln/4)


#2. Total length of read sequences

seq_ln_list = []
with open(f,'r') as file:
	for i in range(ln):
		line = file.readline()
		if i in range(1,ln,4):
			seq_ln = len(line.rstrip())
			seq_ln_list.append(seq_ln)
seq_ln_total = sum(seq_ln_list)

print()
print("[The number of read sequences & Total length of read sequences]")
print("- This file includes",int(num), "reads and",seq_ln_total,"bases.")
print()

#3. The distribution of read lengths

mean = seq_ln_total/num
deviations = [(i-mean)**2 for i in seq_ln_list]
var = sum(deviations)/len(deviations)
sd = var**(1/2)

seq_ln_list.sort()
p_q1 = (num+1)/4
p_q3 = 3*(num+1)/4
if (num+1)//4 ==0:
	q1 = seq_ln_list[p_q1-1]
	q3 = seq_ln_list[p_q3-1]
else:
	p_q1 = int(p_q1)
	p_q3 = int(p_q3)
	q1 = (seq_ln_list[p_q1-1]+seq_ln_list[p_q1])/2
	q3 = (seq_ln_list[p_q3-1]+seq_ln_list[p_q3])/2

iqr = q3-q1 
bottom = q1-1.5*iqr
top = q3+1.5*iqr
outlier = [x for x in seq_ln_list if x<bottom or x>top]
ln_out = len(outlier)

print("[Distibution of read lengths]")
print("- The mean is {}.".format(mean))
print("- The standard deviation is {}.".format(sd))
if ln_out == 0:
	print("- There are no outliers.")
else:
	print("- There are {} outliers.".format(ln_out))
print()


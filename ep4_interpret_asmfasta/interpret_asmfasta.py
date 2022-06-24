#!/usr/bin/env python3.6

import sys
f = sys.argv[1]

cnt = 0
ln = 0
total = 0 #total length
dic_ln = {}
for line in open(f,'r'):
	if line.startswith(">"):
		cnt += 1 #counting number
		if ln !=0:
			if not ln in dic_ln:
				dic_ln[ln] = 1
			else:
				dic_ln[ln] += 1
			
			total += ln
			ln=0 #reset ln
	else:
		ln += len(line.rstrip())

#last one
total +=ln
if not ln in dic_ln:
	dic_ln[ln] =1
else:
	dic_ln[ln] +=1

#sorting dict
dic_ln = dict(sorted(dic_ln.items(),reverse=True))

# The length of the longest * shortest sequence
len_list = list(dic_ln.keys())
lgt = len_list[0]
sht = len_list[-1]

# N50
half_tot_len = total/2
add_len = 0 #지금까지 더해진 길이
for ln,n in dic_ln.items():
	add_len += ln*n
	if add_len >= half_tot_len:
		N50 = ln
		break

# N10
n10_len = total/10
add_len_n10 = 0
for ln,n in dic_ln.items():
	add_len_n10 += ln*n
	if add_len_n10 >= n10_len:
		n10 = ln
		break

#N90
n90_len = (total/10)*9
add_len_n90 = 0
for ln,n in dic_ln.items():
	add_len_n90 += ln*n
	if add_len_n90 >= n90_len:
		n90 = ln
		break

# result
#1 
print("The number of total sequences:",cnt)
#2
print("Total length of sequences:",total)
#3
print("The length of the longest sequences:",lgt)
#4
print("The length of the shortest sequences:",sht)
#5
print("N50:",N50)
print("N10:",n10)
print("M90",n90)

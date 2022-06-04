#!/usr/bin/env python3.6

import sys

seg = sys.argv[1] # Conserved.Segments
odr = sys.argv[2] # Genomes.Orger


asm = 0 # asm == 0: Reference / asm ==1: Target
ref_cnt, tar_cnt = 0, 0 # number of sequences
syn_cnt = 0 # number of synteny blocks
ref_seq_str, tar_seq_str = {},{}

# 1. no of sequences & saving block info
for line in open(odr,'r'):
	if line =='\n': # exclude <blank line>
		asm +=1
		continue
	if asm == 0:
		if line[0] =='>':
			ref_cnt = line.split()[1]
		elif line[0] == '#':
			chro = line.split()[1]
		else:
			ref_seq_str[chro] = line.split()[:-1]
	elif asm == 1:
		if line[0] == '>':
			tar_cnt = line.split()[1]
		elif line[0] == '#':
			chro = line.split()[1]
		else:
			tar_seq_str[chro]=line.split()[:-1]

ref_seq, tar_seq = {},{}
for chro,blocks in ref_seq_str.items():
	ref_seq[chro]= list(map(int,blocks))
for chro,blocks in tar_seq_str.items():
	tar_seq[chro]= list(map(int,blocks))

# 2. no of synteny blocks & #5. Coverage
bt9_syn, bt9_len = 0,0
trs_syn, trs_len = 0,0
bt9_len_dict,trs_len_dict = {},{}

where = 0
for line in open(seg,'r'): 
	if line[0] == '>':
		syn_cnt +=1
		where +=1
	elif where ==1:
		chro = line.split(".")[1].split(":")[0]
		pos = line.split(":")[1].split("-")
		end = int(pos[1].split('+')[0])
		start = int(pos[0])
		bt9_syn += end-start
		where +=1
		if chro in bt9_len_dict:
			bt9_len_dict[chro] = max(bt9_len_dict[chro],end)
		else:
			bt9_len_dict[chro] = end
	elif where ==2:
		chro= line.split(".")[1].split(":")[0]
		pos = line.split(":")[1].split("-")
		end = int(pos[1].split('+')[0])
		start = int(pos[0])
		trs_syn += end-start
		where = 0
		if chro in trs_len_dict:
			trs_len_dict[chro] = max(trs_len_dict[chro],end)
		else:
			trs_len_dict[chro] = end

for chr_len in bt9_len_dict.values():
	bt9_len += chr_len
for chr_len in trs_len_dict.values():
	trs_len += chr_len

bt9_coverage = bt9_syn/bt9_len
trs_coverage = trs_syn/trs_len

# len만 구하면 돼 

# 3-4.the number of broken synteny pairs

ref_pairs = []
tar_pairs = []

for blocks in ref_seq.values():
	for i in range(len(blocks)-1):
		ref_pairs.append(blocks[i:i+2])

for blocks in tar_seq.values():
	for i in range(len(blocks)-1):
		tar_pairs.append(blocks[i:i+2])

# function: broken pairs in asm1 compared with asm2
def broken_pairs(asm1_pairs,asm2_pairs):
	cnt =0
	for pair in asm1_pairs:
		if not pair in asm2_pairs:
			cnt +=1
		else:
			pair = [-i for i in pair]
			pair.reverse()
			if not pair in asm2_pairs:
				cnt +=1
	return cnt

ref_broken = broken_pairs(ref_pairs,tar_pairs)
tar_broken = broken_pairs(tar_pairs,ref_pairs)


# 6. mapping result of my assembly against a reference genome

tar_frag = {} # not synteny
mapping_before = {} # mapping my tar fragments against reference 
frag = []
cnt = 1 # 1,2,3 in 1-1, 1-2 ,1-3 
mapping_after = {}

# copy ref_seq to mapping_after
for chro,blocks in ref_seq.items():
	mapping_after[chro]=[]
	for block in blocks:
		mapping_after[chro].append(block)

# mapping function
def mapping(m,r,f,fn): #m:mapping_after/ r=rchro/ f=frag/ fn = fragname
	if f[-1] in m[r]:
		i = m[r].index(f[-1])
		m[r][i-len(f)+1:i+1]=[fn]
	else:
		i = m[r].index(-f[-1])
		m[r][i:i+len(f)]=['-'+fn]

# mapping process
for tchro, tblocks in tar_seq.items():
	for ti, tblock in enumerate(tblocks):
		frag.append(tblock)
		forbreak =0
		for rchro, rblocks in ref_seq.items():
			if forbreak ==1:
				break
			for ri, rblock in enumerate(rblocks):
				if abs(tblock) == abs(rblock):
					if ti == len(tblocks)-1: #last block
						if cnt ==1: # no break point in blocks
							fragname = tchro
						else:
							fragname = tchro+chr(96+cnt)
						tar_frag[fragname] = frag
						mapping(mapping_after,rchro,frag,fragname)
						frag =[] #reset
						cnt = 1 #reset
						forbreak = 1
						break
					elif tblock == rblock: # not reverse
						if ri == len(rblocks)-1 or tblocks[ti+1] != rblocks[ri+1]: #break point
							fragname = tchro+chr(96+cnt)
							tar_frag[fragname] = frag
							mapping(mapping_after,rchro,frag,fragname)
							frag = []
							cnt+=1
						else:
							continue
					else: # reverse
						if ri == 0 or tblocks[ti+1] != -rblocks[ri-1]: #break point
							fragname = tchro+chr(96+cnt)
							tar_frag[fragname] = frag
							mapping(mapping_after,rchro,frag,fragname)
							frag = []
							cnt+=1
						else:
							continue

# ------------------------------
print("="*100)
print("#1. The number of sequences and synteny blocks in a reference genome")
print("\t# of sequences:",ref_cnt)
print("\t# of synteny blocks:",syn_cnt)
print("-"*100)
print("#2. The number of sequences and synteny blocks in my assembly")
print("\t# of sequences:",tar_cnt)
print("\t# of synteny blocks:",syn_cnt)
print("-"*100)
print("#3. The number of broken synteny pairs in a refence genome compared with my assembly")
print("\t# of broken synteny pairs:", ref_broken)
print("-"*100)
print("#4. The number of broken synteny pairs in my assembly compared with reference genome")
print("\t# of broken synteny pairs:", tar_broken)
print("-"*100)
print("#5. The coverage of synteny blocks against a reference genome and my assembly")
print("\tCoverage of bosTau9:",bt9_coverage)
print("\tCoverage of Redunca:",trs_coverage)
print("-"*100)
print("#6. Mapping result of my assembly against a reference genome")
print("-"*100)
for chro,mapped_l in mapping_after.items():
	print(chro,end="\t")
	for mapped in mapped_l:
		print(mapped,end=" ")
	print()
print("="*100)

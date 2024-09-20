#make alphabetized version of CatLLex and check for duplicates.

import sys

LEXLOC = "SpanLLex_not_glitched.txt" if len(sys.argv) <= 1 else sys.argv[1]

o = open(LEXLOC,encoding='utf-8',mode='r')

lines = [(ln+'$').split('$')[0].strip() for ln in o.readlines()]
o.close()

lines = [ln for ln in lines if ln != ''] 
lines = sorted(lines)

lexloc_prefix = LEXLOC[:LEXLOC.rindex(".")] if "." in LEXLOC else LEXLOC

o = open(lexloc_prefix+"_alphasorted.txt",mode='w',encoding='utf-8')

for i in range(len(lines)-1):
	o.write(lines[i] + "\n")
	if lines[i] == lines[i+1]:
		print("duplicate line at alphabetically sorted line number "+str(i)+": "+lines[i])
o.write(lines[-1]+"\n")
o.close()

# make alphabetized version of file at LEX_LOC and check for duplicates.

LEX_LOC = "SpanLLex.txt"

with open(LEX_LOC, mode='r', encoding='utf-8') as o:
    # lines = [(ln+'$').split('$')[0].strip() for ln in o.readlines()]
    lines_with_comments = [ln.strip() for ln in o.readlines()]
    lines = [ln.split('$')[0].strip() for ln in lines_with_comments]

lines = [ln for ln in lines if ln != '']
lines = sorted(lines)

lines_with_comments = sorted([ln for ln in lines_with_comments if ln != '' and ln[0] != '$'])

with open("alphasorted.txt", mode='w', encoding='utf-8') as o:
    for i in range(len(lines) - 1):
        o.write(lines_with_comments[i] + "\n")
        if lines[i] == lines[i + 1]:
            print("duplicate line at alphabetically sorted line number " + str(i) + ": " + lines[i])
    o.write(lines_with_comments[-1] + "\n")

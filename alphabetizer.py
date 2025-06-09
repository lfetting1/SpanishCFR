# make alphabetized version of file at LEX_LOC and check for duplicates.
import pdb

LEX_LOC = "SpanLLex.txt"
STRESS_MARKERS = ["ˈ", "ˌ"]
CMT_FLAG = "$"

with open(LEX_LOC, mode='r', encoding='utf-8') as o:
    lines = [ln.strip() for ln in o.readlines()]


# moves character in @param [string] inp index @param [int] target to index @param [int] dest
# @param dest will be the new index,
#   so if targ < dest, it is 1 less than where it would be in the prior state of the string
def move_character(inp, targ, dest):
    assert targ != dest, "tried to move character to same location in string. inp: "+inp
    assert len(inp) > targ >= 0, "tried to move character from location outside string bounds: " + str(targ)
    assert len(inp) > dest >= 0, "tried to move character to location outside string bounds: " + str(dest)
    mutandum = (inp[targ + 1:dest + 1] + inp[targ]) if targ < dest else (inp[targ] + inp[dest:targ])
    return "" + inp[:min(targ, dest)] + mutandum + inp[max(targ, dest) + 1:]


# @author: Clayton Marr, June 9, 2025
# moves secondary or primary stress markers to end of symbol they mark
# for a single lexicon line
# assumes all characters delimited by " "!
# retrograde -- if moving stress mark from end back to beginning of symbol
def stress_mark_switch(inp_line, retrograde=False):
    # handle beginning of comment; -1 if there is none
    cmt_start = inp_line.find(CMT_FLAG)

    if cmt_start==0:
        return inp_line

    comment = "" if cmt_start == -1 else inp_line[cmt_start:]
    scope = "" + inp_line if cmt_start == -1 else inp_line[:cmt_start]

    targets = [ind for ind, ltr in enumerate(scope) if ltr in STRESS_MARKERS]
    targets = sorted(targets, reverse=True)  # end to beginning to minimize cascading error
    # plus it's better if retrograde

    #if retrograde:
    #    pdb.set_trace()

    for targ_i in targets:
        dest_i = 0
        if retrograde:
            dest_i = scope[:targ_i].rfind(" ") + 1
        else:
            if scope[targ_i:].find(" ") == -1:
                dest_i = len(scope) - 1
            else:
                dest_i = scope[targ_i:].find(" ") + targ_i - 1
        # when 'forward',dest_i will be the end of the scope for the last stress mark
        # if final space is somehow missing.
            # same applies if retrograde for the first character
                # but -1 + 1 = 0 so you end up with the same result anyways (get -1 for rfind if it's not there)
        scope = move_character(scope, targ_i, dest_i)

    return scope + comment


# @author: Clayton Marr, June 9, 2025
# sorting method
# can be modified
# possibly do it based on features in the future
# right now, it's functioning to prevent stress markers from messing with ordering.
def sorting(inp_lines):
    # keep header and any following comments at the top

    out_lines = [stress_mark_switch(ln) for ln in inp_lines if ln != '']
    out_lines = sorted(out_lines)
    return [stress_mark_switch(ln, retrograde=True) for ln in out_lines]


prologue = []
while lines[0][0] in ["=", "~", "$"]:
    prologue += [lines[0]]
    lines = lines[1:]

if len(prologue) > 0:
    prologue += [""]

print("Empty lines : "+str(len([ln for ln in lines if ln == ''])))

lines = [ln for ln in lines if ln != '']
lines = prologue + sorting(lines)


def ln_sans_cmt(ln):
    return ln if ln.find(CMT_FLAG) == -1 else ln[:ln.find(CMT_FLAG)].strip()


with open("alphasorted.txt", mode='w', encoding='utf-8') as o:
    for i in range(len(lines) - 1):
        o.write(lines[i] + "\n")
        if ln_sans_cmt(lines[i]) == ln_sans_cmt(lines[i + 1]) and lines[i][0] != "$":
            print("duplicate line at alphabetically sorted line number " + str(i) + ": " + lines[i])
    o.write(lines[-1] + "\n")

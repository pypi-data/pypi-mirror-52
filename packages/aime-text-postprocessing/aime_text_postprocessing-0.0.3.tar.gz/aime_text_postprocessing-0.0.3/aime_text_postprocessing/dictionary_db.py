import codecs
import re

REPLY_REGEXS, REPLY_OUT = [], []

NAME_REGEXS, NAME_OUT = [], []


def load(fpath, saved=True):
    comp_regexs = []
    rep_ouputs = []
    f = codecs.open(fpath, 'r', 'utf-8')
    try:
        for line in f:
            temp = line
            if line.endswith('\n'):
                temp = line[:-1]
            if temp.startswith('#'):
                continue
            tgs = temp.split('-->')
            try:
                comp_regexs.append(re.compile(tgs[0]))
                rep_ouputs.append(tgs[1])
            except:
                print('err at line:  %s' % temp)
    finally:
        f.close()
    if saved:
        global REPLY_OUT, REPLY_REGEXS
        REPLY_REGEXS, REPLY_OUT = comp_regexs, rep_ouputs
    return comp_regexs, rep_ouputs


def loads(text, saved=True):
    comp_regexs = []
    rep_ouputs = []
    for line in text.splitlines():
        temp = line
        if line.endswith('\n'):
            temp = line[:-1]
        if temp.startswith('#'):
            continue
        tgs = temp.split('-->')
        try:
            comp_regexs.append(re.compile(tgs[0]))
            rep_ouputs.append(tgs[1])
        except:
            print('err at line:  %s' % temp)
    if saved:
        global REPLY_OUT, REPLY_REGEXS
        REPLY_REGEXS, REPLY_OUT = comp_regexs, rep_ouputs
    return comp_regexs, rep_ouputs


def load_name(fpath, saved=True):
    comp_regexs, rep_ouputs = load(fpath, saved=False)
    if saved:
        global NAME_REGEXS, NAME_OUT
        NAME_REGEXS, NAME_OUT = comp_regexs, rep_ouputs
    return comp_regexs, rep_ouputs


def loads_name(text, saved=True):
    comp_regexs, rep_ouputs = loads(text, saved=False)
    if saved:
        global NAME_REGEXS, NAME_OUT
        NAME_REGEXS, NAME_OUT = comp_regexs, rep_ouputs
    return comp_regexs, rep_ouputs

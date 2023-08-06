from tokenize import tokenize, untokenize, COMMENT,NL,NEWLINE
from efdir import fs
from io import BytesIO
import estring.estring as eses
import re
import elist.elist as elel

# tokenize.NL
# Token value used to indicate a non-terminating newline. 
# The NEWLINE token indicates the end of a logical line of Python code; 
# NL tokens are generated when a logical line of code is continued over multiple physical lines.

def _group2str(group):
    s = untokenize(group)
    s = eses.strip(s,"\\\n",mode="whole")
    return(s)

def _infos2group(infos):
    def map_func(ele):
        ele.pop(0)
        return(ele)
    indexes = elel.cond_select_indexes_all(infos,cond_func=lambda info:(info.type==NEWLINE))
    groups = elel.broken_seqs(infos,indexes)
    groups = elel.remove_all(groups,[])
    groups = elel.mapv(groups,map_func)
    groups = elel.remove_all(groups,[])
    groups = elel.mapv(groups,_group2str)
    try:
        groups = elel.remove_last(groups,"\n")
        groups = elel.remove_first(groups,"\n")
    except:
        pass
    else:
        pass
    return(groups)


def tst2kvlist(**kwargs):
    if("codec" in kwargs):
        codec = kwargs["codec"]
    else:
        codec = "utf-8"
    if("code" in kwargs):
        code = kwargs["code"]
    else:
        code = fs.rfile(kwargs["fn"])
    code = code + "\n#"
    g = tokenize(BytesIO(code.encode(codec)).readline)
    info = next(g)
    kl = []
    vl = []
    k = ""
    infos = [info]
    for info in g:
        if(info.type == COMMENT):
            kl.append(k)
            v = _infos2group(infos)
            vl.append(v)
            k = info.string.lstrip("#")
            infos = []
        else:
            infos.append(info)
    indexes = elel.cond_select_indexes_all(kl,cond_func=lambda ele:ele=="")
    kl = elel.pop_indexes(kl,indexes)['list']
    vl = elel.pop_indexes(vl,indexes)['list']
    return((kl,vl))


#####


def arr2str(cmds_arr):
    return(elel.join(cmds_arr,"\n"))

def creat_head(s,i=None,bot="-"):
    if(i==None):
        pass
    else:
        s = str(i) + ". " + s
    return(s+"\n"+bot*s.__len__()+"\n\n")

def creat_title(title="Usage",bot="="):
    return(creat_head(title,i=None,bot=bot))

def creat_code_blk(cmds_arr):
    s = arr2str(cmds_arr)
    arr = s.split("\n")
    head1 = "    ::"
    head2 = "    "
    arr = elel. mapv(arr,lambda s:("        "+s))
    arr = elel.prepend(arr,head2)
    arr = elel.prepend(arr,head1)
    s = elel.join(arr,"\n") + "\n\n"
    return(s)


def get_svg_name(k):
    regex = re.compile("(.*?)\(.*\)")
    m = regex.search(k)
    if(m):
        return(m.group(1))
    else:
        return(k)

def creat_one_rst(k,v,i=None,**kwargs):
    if('bot' in kwargs):
        bot = kwargs['bot']
    else:
        bot = "-"
    head = creat_head(k,i,bot=bot)
    body = creat_code_blk(v)
    name = get_svg_name(k)
    image = ".. image:: ./images/" + name+".svg"+"\n\n"
    return(head+body+image)

def creat_rst(kl,vl,**kwargs):
    if("title" in kwargs):
        title = kwargs['title']
    else:
        title = "Usage"
    if("title_bot" in kwargs):
        title_bot = kwargs['title_bot']
    else:
        title_bot = "="
    if("entry_bot" in kwargs):
        entry_bot = kwargs['entry_bot']
    else:
        entry_bot = "-"
    title = creat_title(title=title,bot=title_bot)
    sarr = []
    for i in range(kl.__len__()):
        k = kl[i]
        v = vl[i]
        s = creat_one_rst(k,v,i=i,bot=entry_bot)
        sarr.append(s)
    s = title + elel.join(sarr,"")
    return(s)


#####

#####
#creat  from  comments
#####

def creat_projhd(projname,desc):
    l0 = ".. contents:: Table of Contents\n"
    l1 = "   :depth: 5\n\n\n"
    l2 = "*"+projname+"*\n"
    l3 = "=" * (len(l2) - 1) + "\n"
    descs = desc.split("\n")
    descs = elel.mapv(descs, lambda ele:"- "+ele)
    l4 = elel.join(descs,"\n")
    l5 = "\n\n\n"
    s = l0+l1+l2+l3+l4+l5
    print(s)
    return(s)


def creat_install(*args):
    l0 = "Installation\n"
    l1 = "------------\n"
    l2 = "\n    ::\n"
    l3 = "\n"
    projname = args[0]
    l4 = "        $ "
    l5 = "pip3 install " if(len(args)==1) else args[1]
    l6 = projname
    l7 = "\n\n"
    s = l0+l1+l2+l3+l4+l5+l6+l7
    print(s)
    return(s)



def creat_license(*args):
    lic = "MIT" if(len(args)==0) else args[0]
    tem = "License\n-------\n\n- " + lic + "\n\n"
    print(tem)
    return(tem)



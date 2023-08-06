import ast
import astunparse
from efdir import fs
import ast
import astunparse
import elist.elist as elel

def get_node_type(nd):
    return(type(nd).__name__)

def is_leaf(v):
    cond0 = (isinstance(v,list) and len(v)==0)
    cond1 = not(is_node(v))
    cond = true if(cond0) else cond1
    return(cond)

def is_node(v):
    s  = v.__str__()
    if('_ast.' in s):
        return(True)
    else:
        return(False)

def nd2d(nd):
    d = {}
    g = ast.iter_fields(nd)
    d['_type'] = get_node_type(nd)
    for it in g:
        d[it[0]] = it[1]
    return(d)

def is_children(v):
    if(is_node(v)):
        return(True)
    elif(isinstance(v,list) and len(v)>0):
        return(True)
    else:
        return(False)

def is_list_children(v):
    return(isinstance(v,list) and len(v)>0)

def get_children(d):
    children = []
    for k in d:
        v = d[k]
        if(is_list_children(v)):
            v = elel.mapv_inplace(v,nd2d)
            d[k] = v
            children.extend(v)
        elif(is_node(v)):
            v = nd2d(v)
            d[k] = v
            children.append(v)
        else:
            pass
    return(children)



def wfsdig(root):
    d = nd2d(root)
    unhandled = [d]
    while(unhandled.__len__()>0):
        next_unhandled = []
        for i in range(unhandled.__len__()):
            ele = unhandled[i]
            children = get_children(ele)
            next_unhandled.extend(children)
        unhandled = next_unhandled
    return(d)


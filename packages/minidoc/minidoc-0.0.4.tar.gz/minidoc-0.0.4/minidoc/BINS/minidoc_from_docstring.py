from minidoc import minidoc
from minidoc import tst
from minidoc import comast
import argparse
from efdir import fs
import ast
from minidoc.comast import wfsdig
from minidoc.tst import creat_rst
import elist.elist as elel

parser = argparse.ArgumentParser()
parser.add_argument('-src','--src_file', default="",help=".py file name")
parser.add_argument('-codec','--codec', default="utf-8",help=".tst.py file codec")
parser.add_argument('-dst','--dst_file', default="",help="destination rst")
parser.add_argument('-proj','--proj_name', default="projname",help="project name")
parser.add_argument('-desc','--proj_desc', default="desc0\ndesc1",help="project description")
parser.add_argument('-lic','--proj_lic', default="MIT",help="project license")
parser.add_argument('-inst','--proj_inst_cmd', default="",help="project install cmd")
parser.add_argument('-tbot','--title_bot', default="=",help="parent title bottom char")
parser.add_argument('-ebot','--entry_bot', default="-",help="entry title bottom char")


def boolize(s):
    s = s.lower()
    if(s=="true"):
        return(True)
    elif(s=="false"):
        return(False)
    else:
        return(False)

def creat_usage_from_code(cd):
    root = ast.parse(cd)
    d = wfsdig(root)
    body = d['body']
    funcs = elel.cond_select_all(d['body'],cond_func=lambda ele:ele['_type'] == 'FunctionDef')
    kl = elel.mapv(funcs,lambda func:func['name'])
    vl = elel.mapv(funcs,lambda func:[func['body'][0]['value']['s']])
    usage = creat_rst(kl,vl)
    return(usage)

args = parser.parse_args()


def main():
    projhd = tst.creat_projhd(args.proj_name,args.proj_desc)
    install = tst.creat_install(args.proj_name)
    license = tst.creat_license(args.proj_lic)
    src = (args.proj_name+".py") if(args.src_file=="") else args.src_file
    cd = fs.rfile(src)
    usage = creat_usage_from_code(cd)
    rst_str = projhd + install + license + usage
    dst = (args.proj_name+".rst") if(args.dst_file=="") else args.dst_file
    fs.wfile(dst,rst_str,codec=args.codec)



#minidoc_from_comments

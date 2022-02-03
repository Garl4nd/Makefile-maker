import mkfilegen.condensemod as cm
import re
import os
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
#print("********")
def main(draw=False,save=False):
    s="" 
    filenames=[file for file in os.listdir() if file.endswith(".f90") or file.endswith(".for")]
    module_dict=dict()
    all_mods=set()
    for filename in filenames:
        with open(filename) as file:
            text=file.read().lower()
            
            deps=set([word.strip().strip(",").strip() for word in re.findall("^\s*use(?:\s|,)(.*?)(?:only|$)",text,re.MULTILINE)])
            deps={dep for dep in deps if " " not in dep}
            module_dict[filename]=deps
            all_mods.update(deps)

    asoc=dict()
    for mod in all_mods:
        
        for filename in filenames:
            with open(filename) as file:
                text=file.read().lower()
                
                if re.findall("module.*"+mod,text):
                    asoc[mod]=filename
            
    file_deps={filename:{asoc.get(dep,None) for dep in deps} for filename,deps in module_dict.items() } 
    file_deps={key:{el for el in val if el!=None} for key,val in file_deps.items()}
    nameddict,tupdict,leveldict=cm.create_groups_levels(file_deps)
    try:
        with open("mkfilegen/preamble.txt") as file:
            prefix=file.read()
    except IOError:
    
        prefix=""
    with open("makefile","w") as file:
        file.write(prefix+"\n\n")
        
        
        
        sorted_files=sorted(nameddict.keys(),key=lambda x: leveldict[x])
        sourcestring="allfiles={}".format(' '.join(sorted_files))
        level0={key:val for (key,val) in nameddict.items() if leveldict[key]==0}
        #print(level0)
        o_str=re.sub('(\.f90|\.for)','.o',sourcestring)
        file.write(o_str+"\n\n")
        source_str=' '.join(key for key in level0)
        o_str=re.sub('(\.f90|\.for)','.o',source_str)
            
        o_names,src_names=[],[]
        print("namedict= {}".format(nameddict))
        for ind,(group,deps) in enumerate(nameddict.items()):
            
            source_str=group
            o_str=re.sub('(\.f90|\.for)','.o',source_str)
            o_names.append("ogroup{}".format(ind+1))
            src_names.append("srcgroup{}".format(ind+1))
            file.write("{0}={1}\n".format(o_names[-1],o_str))
            file.write("{0}={1}\n\n".format(src_names[-1],source_str))
        file.write("default: $(NAME)\n")
        file.write("$(NAME): $(allfiles)\n") 
        file.write("\t$(COMPILER) $(FLAGS) -o $(NAME) $(allfiles)\n\n")
        for ind,(group,tupgroup) in enumerate(zip(nameddict.keys(),tupdict.keys())):
            file.write("$({0}): $({1})\n".format(o_names[ind],src_names[ind]))
            if len(tupgroup)>1:
                file.write("\t-$(COMPILER) $(FLAGS) -c $^; if [ $$? -ne 0 ]; then -$(COMPILER) $(FLAGS) -c $^ ; fi\n\n")
            else:
                file.write("\t-$(COMPILER) $(FLAGS) -c $^\n\n")
        file.write("clean:\n")
        file.write("\trm *.o *.mod")
    print("Makefile generation successful!")
    if draw:
        print("Generating figures of the dependance structure.")
        cm.draw_deps(file_deps,save=save,figname="orig_structure.png")
        cm.draw_deps(nameddict,save=save,show=not save,tree=True,levels=leveldict,figname="condensed_structure.png")
if __name__=="__main__":
    args=sys.argv
    try:
        draw=True if sys.argv[1]=="1" else False
        try:
            save=True if sys.argv[2]=="1" else False
        except IndexError:
            save=False    
    except IndexError:
        draw=False
        save=False
    main(draw=draw,save=save)
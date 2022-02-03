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
            
            #deps=set([word.strip().strip(",").strip() for word in re.findall("use(.*?)",text) if not " " in word])
            #deps=set([word.strip().strip(",").strip() for word in re.findall("use(.*?)",text,re.MULTILINE) if not " " in word])
            #deps=set([word.strip().strip(",").strip() for word in re.findall("use (.*?)(?:only|$)",text,re.MULTILINE) if not " " in word])
            deps=set([word.strip().strip(",").strip() for word in re.findall("^\s*use(?:\s|,)(.*?)(?:only|$)",text,re.MULTILINE)])
            deps={dep for dep in deps if " " not in dep}
            ##print(filename,re.findall("use,?(.*?)(?:only|$)",text,re.MULTILINE))
            module_dict[filename]=deps
            all_mods.update(deps)

    #for item in module_dict.items():
    #    #print(item)
    asoc=dict()
    for mod in all_mods:
        
        for filename in filenames:
            with open(filename) as file:
                text=file.read().lower()
                
                if re.findall("module.*"+mod,text):
                    asoc[mod]=filename
            
    #print(asoc)
    ##print(module_lists)
    ##print(len(all_mods),len(asoc))
    #print(f"module_dict: {module_dict}")
    file_deps={filename:{asoc.get(dep,None) for dep in deps} for filename,deps in module_dict.items() } 
    file_deps={key:{el for el in val if el!=None} for key,val in file_deps.items()}
    nameddict,tupdict,leveldict=cm.create_groups_levels(file_deps)
    try:
        with open("mkfilegen/preamble.txt") as file:
            prefix=file.read()
    except IOError:
        #print("IOError")
        prefix=""
    with open("makefile","w") as file:
        file.write(prefix+"\n\n")
        
        
        
        sorted_files=sorted(nameddict.keys(),key=lambda x: leveldict[x])
        sourcestring=f"allfiles={' '.join(sorted_files)}"
        level0={key:val for (key,val) in nameddict.items() if leveldict[key]==0}
        #print(level0)
        o_str=re.sub('(\.f90|\.for)','.o',sourcestring)
        file.write(o_str+"\n\n")
        source_str=' '.join(key for key in level0)
        o_str=re.sub('(\.f90|\.for)','.o',source_str)
            
        o_names,src_names=[],[]
        print(f"namedict= {nameddict}")
        for ind,(group,deps) in enumerate(nameddict.items()):
            
            source_str=group
            o_str=re.sub('(\.f90|\.for)','.o',source_str)
            o_names.append(f"ogroup{ind+1}")
            src_names.append(f"srcgroup{ind+1}")
            file.write(f"{o_names[-1]}={o_str}\n")
            file.write(f"{src_names[-1]}={source_str}\n\n")
            #file.write(f"ogroup{ind-inddif}={' '.join(re.sub('(f90|for)','o',str(el)) for el in group)}\n")
            #file.write(f"depgroup{ind-inddif}={dep_str}\n")
            #file.write(f"ogroup{ind}={re.sub(',',' ',group).strip('(').strip(')')}\n")
            #file.write(f"depgroup{ind}={re.sub(',',' ',' '.join(dep for dep in deps))}\n")
        file.write("default: $(NAME)\n")
        file.write("$(NAME): $(allfiles)\n") 
        file.write("\t$(COMPILER) $(FLAGS) -o $(NAME) $(allfiles)\n\n")
        for ind,(group,deps) in enumerate(nameddict.items()):
            file.write(f"$({o_names[ind]}): $({src_names[ind]})\n")
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
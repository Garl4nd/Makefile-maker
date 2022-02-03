import matplotlib.pyplot as plt
import numpy as np


def get_terminals(depdict):
    return [el for el,val in depdict.items() if (not val) or (len(val)==1 and next(iter(val))==el) ]
def get_initials(depdict):
    return get_terminals(invert(depdict))
def make_str(tup,par=False):
        #print(f"{len(tup)=},{tup=}")
        if len(tup)==1:
            return str(tup[0])
        else:
            if par:
                return "( "+(", ".join(str(el) for el in tup))+" )"
            else:
                return " ".join(str(el) for el in tup)
def make_el_loops(start,deps):
    
    loops=[]
    terminals=get_terminals(deps)
    #print(f"{start=},{deps=},{terminals=}")
    #input()
    for id in terminals:
        loops.append({id})
        #print(f"{id=} is terminal!")
    def _make_el_loops(id,parents=[]):
        #if id in terminals:
        #    loops.append({id})
        #    #print(f"{id=} is terminal!")
            #input()
        #    return 
        #if id not in loopdict and id in parents:
        if id in parents:
            myind=parents.index(id)
            loop_parents=parents[myind:]
            newloop={*loop_parents}
            loops.append(newloop)
            #print(f"{id=} returned to itself. Adding {newloop=} to loops")
            #input()
            return 

        #dont_look={id}
        #for loop in loops:
        #    if id in loop:
        #        dont_look.update(loop)
        #print(f"{id=},{deps[id]=},{loops=},{dont_look=}")
        for child_id in deps[id]:
            if child_id==id or child_id in terminals:
                continue
            if any(id in loop and child_id in loop for loop in loops):
                #print(f"{id=} is not entering {child_id=} because both are in one of the {loops=}")
                continue
            #print(f"{id=} is entering {child_id=}")
            #input()
            _make_el_loops(child_id,parents+[id])
            #if child_id not in dont_look:
        if not any(id in loop for loop in loops):
            #print(f"{id=} is not in any loop all children were entered, adding singular loop.")
            loops.append({id})
        #if id not in loopdict:
            
        #    loopdict[id]=loops[-1]
        return

    _make_el_loops(start)
    return loops
    
def get_levels(depdict,id=0):
    levels={}
    terminals=get_terminals(depdict)
    #input()
    def _get_levels(id):
            #print(f"get levels: {depdict=},{id=}")        
            if id in terminals:
                levels[id]=0
                return levels[id]
            else:
                #print(f"{id=},{depdict[id]=}")
                levels[id]=max(_get_levels(child_id) for child_id in depdict[id] if child_id!=id)+1
                return levels[id]
    _get_levels(id)
    return levels
def draw_deps(depdict,save=False,show=False,figname="depgraph.png",levels=None,tree=False):
    if save:
        fig,ax=plt.subplots(figsize=(10,10))
    else:    
        fig,ax=plt.subplots()
    n=len(depdict)
    idict={key:i for i,key in enumerate(depdict)}
    #print("*.*.*.",idict)
    colors=plt.rcParams['axes.prop_cycle'].by_key()['color']
    #print(f"{idict=},{depdict=}")
    angs=[2*3.14/n*i for i in range(n)]
    if tree:
        if levels==None:
            raise ValueError("Drawing a tree requires filling the levels= key argument !")
        xposar={}
        yposar={}
        max_height=max(val for val in levels.values())
        
        for i in range(n):
            chosen={key:val for (key,val) in depdict.items() if levels[key]==i}
            for ind,(key,val) in enumerate(chosen.items()):
                width=len(chosen)
                #print(width)
                xposar[key]=2*(ind-(width-1)/2)
                yposar[key]=max_height-i
        halfwidth=max(xposar.values())
        width=2*halfwidth+1.5
        arwidth=0.01*(width)/3
    else:
        xposar={key:np.cos(ang) for key,ang in zip(depdict,angs)}
        yposar={key:np.sin(ang) for key,ang in zip(depdict,angs)}
        arwidth=0.01
    for i,(file,deps) in enumerate(depdict.items()):
        #ang=angs[i]
        xpos,ypos=xposar[file],yposar[file]#np.cos(ang),np.sin(ang)
        #plt.annotate(file,(xpos,ypos))
        t=ax.text(xpos,ypos,file,bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'),ha="center")
        if levels is not None:
            if tree:
                r = fig.canvas.get_renderer()
                bb = t.get_window_extent(renderer=r)
                #print(f"{bb=}")
                x1,y1=bb.width,bb.height
                xbox,ybox=-ax.transData.inverted().transform((x1,y1))
                #print(f"{xbox=}")
                
                #ax.text(xpos+0.1*width,ypos,levels[file],ha="center",color="red")
                ax.text(xpos-1.5*xbox,ypos+1.5*ybox,levels[file],color="red")
            else:
                ax.text(xpos*1.3,ypos*1.3,levels[file],ha="center",color="red")
        #print(f"{deps=}")
        for dep in deps:
            if dep is None or dep==file:
                continue
            #print(f"{idict[dep]=}")
            #ang=angs[idict[dep]]
            xpos2,ypos2=xposar[dep],yposar[dep]#np.cos(ang),np.sin(ang)
            dx=(xpos2-xpos);dy=(ypos2-ypos)
            ax.arrow(xpos+0.05*dx,ypos+0.05*dy,0.9*dx,0.9*dy,width=arwidth,color=colors[idict[dep]%10])
    if tree:
        ax.set_ylim(-0.5,max_height+0.5)
        ax.set_xlim(-0.75-halfwidth,0.75+halfwidth)
    else:
        ax.set_xlim(-1.5,1.5)
        ax.set_ylim(-1.5,1.5)
    if save:
        fig.savefig(figname)
    else:
        if show:
            plt.show()
def invert(depdict):
        res={key:set() for key in depdict}
        #print(f"{depdict=}")
        for key,deps in depdict.items():
            for dep in deps:
                res[dep].add(key)

        return res

def condense_groups(deps0,start_key=0):
    #print(f"calling elloops with {start_key=},{deps0}")
    #input()
    loops=make_el_loops(start_key,deps0)
    #print(f"done, {loops=}")
    #print(f"{loops=}")
    final_loops=set()
    final_loops=[]
    #print(f"starting condensing with {loops=}")
    #input()

    while loops:
     #   #print(f"{loops=},{final_loops=}")
      #  input()
        #first=loops[0]
        rem_inds=[]
        remove_first=True
        for ind,loop in enumerate(loops[1:]):
            if loop.intersection(loops[0]):
                remove_first=False
                loops[0]=loop.union(loops[0])
                rem_inds.append(ind+1-len(rem_inds))
        for ind in rem_inds:
            del loops[ind]
        if remove_first:
            final_loops.append(tuple(loops[0]))
            del loops[0]

            

    #for loop in loop_list:
    #    newloop=loop
    #    for loop2 in loops:
    #        if loop2.intersection(newloop):
    #            newloop=newloop.union(loop2)
                #print(f"combining  {loop2=} and {newloop=}")
                #input()
    #    final_loops.add(tuple(newloop))
        #print(f"added  {newloop=}")
        #input()
    #final_loops=list(final_loops)
    depdict={}

    for loop_ind,loop_els in enumerate(final_loops):
        newdeps=set()
        for key in loop_els:
            for dep in deps0[key]:
                for loop2_ind,loop2_els in enumerate(final_loops):
                    if dep in loop2_els:
                        if loop2_ind!=loop_ind:
                            newdeps.add(loop2_ind)
        depdict[loop_ind]=newdeps
    #print(f"{final_loops=},{deps0=},{depdict=}")

    
    
    #print(loops_inds)
    
    #print(f"{final_loops=},{depdict=}")

    
    auxdict={final_loops[ind]:{final_loops[val] for val in value} for ind,value in depdict.items() }
    nameddict={make_str(key):{make_str(val) for val in value} for key,value in auxdict.items() }
    #nameddict={make_str(final_loops[ind]):{make_str(final_loops[val]) for val in value} for ind,value in depdict.items() }
    #print(f"{depdict=},{nameddict=},{deps0=}")
    #print(f"{auxdict=},{nameddict=},orig {start_key=}")
    
    #zero_ind=0
    for key in auxdict:
        if start_key in key:
            start_key=make_str(key)
            break
    #        break
    #print(f"{auxdict=},{nameddict=},new {start_key=}")
    #input()
    #print(f"Preparing to make levels with {zero_ind=},{start_key=},{nameddict=}")
    #input()
    
    #print(f"Preparing to make levels with {start_key=},{nameddict=}")
    
    #input()
    try:
        #print(f"entering get levels with {nameddict=} and {start_key=}")
        #input()
        levels=get_levels(nameddict,id=str(start_key))
    except RecursionError:
        #print(f"{final_loops=}")
        initials=get_initials(deps0)
        deps0={key:value for (key,value) in deps0.items() if key==start_key or key not in initials }
        draw_deps(deps0,show=False)
        draw_deps(nameddict,show=True)
        raise ValueError("bac")
    loops_inds=[]
    #for index,level in levels.items():
    #    loops_inds.append((final_loops[index],level))
    #print(sorted(loops,key= lambda x: x[1]))
    return nameddict,auxdict,levels
    
def create_groups_levels(deps0):
    initials=get_initials(deps0)
    #print(f"{initials=}")
    #print(f"{invert(deps0)=}")
    #deps0={key:value for (key,value) in deps0.items() if key not in [initials[0]]+initials[2:] }
    #draw_deps(deps0,show=True)
    #draw_deps(invert(deps0),show=True)
    #make_el_loops(initials[1],deps0)
    #exit()
    #terminals=get_terminals(deps0)    
    #print(f"{initials=},{terminals=}")
    #exit()
    #draw_deps(deps0)
    #draw_deps(invert(deps0))
    #input()
    if not initials:
        initials=[next(iter(deps0.keys()))]
    nameddicts,tupdicts,levels=zip(*[condense_groups(deps0,start) for start in initials])
    #nameddict=condense_groups(deps0,0)
    #nameddict2=condense_groups(deps0,7) 
    combdict={}
    comblevels={}
    combtupdict={}

    for namedict in nameddicts:
        combdict={**combdict,**namedict}
    for tupdict in tupdicts:
        combtupdict={**combtupdict,**tupdict}
    for level in levels:
        comblevels={**comblevels,**level}
    #draw_deps(deps0,show=False)
    #draw_deps(combdict,show=True,levels=comblevels,tree=True)
    return combdict,combtupdict,comblevels
    #print(comblevels)
if __name__=="__main__":
    deps0={'randomdynmod.f90': {'inversion.f90', 'randomdynmod.f90'}, 'dynamicsolver.f90': {'fd3d_init.f90', 'mod_pt.f90', 'inversion.f90', None, 'waveforms.f90'}, 'inversion_com.f90': set(), 'mod_pt.f90': set(), 'waveforms.f90': {'waveforms.f90', 'PGAmisf.f90', 'fd3d_init.f90', 'mod_pt.f90'}, 'filters.for': set(), 'fd3d_theo.f90': {'fd3d_init.f90'}, 'fd3d_init.f90': {'inversion.f90', 'PGAmisf.f90', 'fd3d_init.f90'}, 'fd3d_deriv.f90': {None, 'fd3d_init.f90'}, 'inversion.f90': {'PGAmisf.f90', 'fd3d_init.f90', 'mod_pt.f90', 'inversion.f90', 'waveforms.f90'}, 'PGAmisf.f90': {'waveforms.f90', 'PGAmisf.f90'}};deps0={key:{el for el in val if el!=None} for key,val in deps0.items()}
    #deps0={0: {1,2,3},1:{4},2:{4},3:{4},4:set()}
    #deps0={0:{"a",2,3},"a":{2},2:{3},3:{"a"}}
    #deps0={0:{1},1:{2},2:{0}}
    #deps0={0:{1},1:{2,7},2:{3,5},3:{1,6},5:set(),6:{3},7:set()}
    #deps0={0:{1,2,3,4},1:set(),2:{1,3,6},3:{4,6},6:{2},7:{3},8:{3,6},4:{2,6,3,1},5:{4}}
    deps1,tupdeps,levels=create_groups_levels(deps0)
    draw_deps(deps0,show=False)
    draw_deps(deps1,show=True,tree=True,levels=levels)
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys

def get_terminals(depdict):
    return [el for el,val in depdict.items() if (not val) or (len(val)==1 and next(iter(val))==el) ]
def get_initials(depdict):
    return get_terminals(invert(depdict))
def make_str(tup,par=False):
        if len(tup)==1:
            return str(tup[0])
        else:
            if par:
                return "( "+(", ".join(str(el) for el in sorted(tup,key=str)))+" )"
            else:
                return " ".join(str(el) for el in sorted(tup,key=str))
                
def make_el_loops(start,deps):
    
    loops=[]
    terminals=get_terminals(deps)
    for id in terminals:
        loops.append({id})
    def _make_el_loops(id,parents=[]):
        
        if id in parents:
            myind=parents.index(id)
            loop_parents=parents[myind:]

            newloop=set(loop_parents)

            loops.append(newloop)
            return 

        for child_id in deps[id]:
            if child_id==id or child_id in terminals:
                continue
            if any(id in loop and child_id in loop for loop in loops):
                continue
            _make_el_loops(child_id,parents+[id])
            
        if not any(id in loop for loop in loops):
            loops.append({id})
        return

    _make_el_loops(start)
    return loops
    
def get_levels(depdict,id=0):
    levels={}
    terminals=get_terminals(depdict)
    def _get_levels(id):
            
            if id in terminals:
                levels[id]=0
                return levels[id]
            else:
                levels[id]=max(_get_levels(child_id) for child_id in depdict[id] if child_id!=id)+1
                return levels[id]
    _get_levels(id)
    return levels
def draw_deps(depdict,save=False,show=False,figname="depgraph.png",levels=None,tree=False):
    if save:
        matplotlib.use("Agg")
        fig,ax=plt.subplots(figsize=(10,10))
    else:    
        matplotlib.use("TkAgg")
        fig,ax=plt.subplots()
    n=len(depdict)
    idict={key:i for i,key in enumerate(depdict)}
    if sys.version_info[1]<7:
        colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
    else:
        colors=plt.rcParams['axes.prop_cycle'].by_key()['color']
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
        xpos,ypos=xposar[file],yposar[file]#np.cos(ang),np.sin(ang)
        t=ax.text(xpos,ypos,file,bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'),ha="center")
        if levels is not None:
            if tree:
                r = fig.canvas.get_renderer()
                bb = t.get_window_extent(renderer=r)        
                x1,y1=bb.width,bb.height
                xbox,ybox=-ax.transData.inverted().transform((x1,y1))

                ax.text(xpos-1.5*xbox,ypos+1.5*ybox,levels[file],color="red")
            else:
                ax.text(xpos*1.3,ypos*1.3,levels[file],ha="center",color="red")
        
        for dep in deps:
            if dep is None or dep==file:
                continue
            xpos2,ypos2=xposar[dep],yposar[dep]
            dx=(xpos2-xpos);dy=(ypos2-ypos)
            if sys.version_info[1]<7:
                fact=0.15
            else:
                fact=1
            ax.arrow(xpos+0.05*dx,ypos+0.05*dy,0.9*dx,0.9*dy,width=fact*arwidth,color=colors[idict[dep]%len(colors)])
           # ax.arrow(xpos+0.05*dx,ypos+0.05*dy,0.9*dx,0.9*dy,width=arwidth)
            #ax._get_lines.get_next_color()

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
    return nameddict,auxdict,levels
def create_groups_levels(deps0):
    initials=get_initials(deps0)
    if not initials:
        initials=[next(iter(deps0.keys()))]
    nameddicts,tupdicts,levels=zip(*[condense_groups(deps0,start) for start in initials])
    combdict={}
    comblevels={}
    combtupdict={}

    def merge_dicts(x,y):
        z = x.copy()
        z.update(y)
        return z
    for namedict in nameddicts:
        combdict=merge_dicts(combdict,namedict)
    for tupdict in tupdicts:
        combtupdict=merge_dicts(combtupdict,tupdict)
    for level in levels:
        comblevels=merge_dicts(comblevels,level)
    return combdict,combtupdict,comblevels
if __name__=="__main__":
    deps0={'randomdynmod.f90': {'inversion.f90', 'randomdynmod.f90'}, 'dynamicsolver.f90': {'fd3d_init.f90', 'mod_pt.f90', 'inversion.f90', None, 'waveforms.f90'}, 'inversion_com.f90': set(), 'mod_pt.f90': set(), 'waveforms.f90': {'waveforms.f90', 'PGAmisf.f90', 'fd3d_init.f90', 'mod_pt.f90'}, 'filters.for': set(), 'fd3d_theo.f90': {'fd3d_init.f90'}, 'fd3d_init.f90': {'inversion.f90', 'PGAmisf.f90', 'fd3d_init.f90'}, 'fd3d_deriv.f90': {None, 'fd3d_init.f90'}, 'inversion.f90': {'PGAmisf.f90', 'fd3d_init.f90', 'mod_pt.f90', 'inversion.f90', 'waveforms.f90'}, 'PGAmisf.f90': {'waveforms.f90', 'PGAmisf.f90'}};deps0={key:{el for el in val if el!=None} for key,val in deps0.items()}
   
    deps1,tupdeps,levels=create_groups_levels(deps0)
    draw_deps(deps0,show=False)
    draw_deps(deps1,show=True,tree=True,levels=levels)
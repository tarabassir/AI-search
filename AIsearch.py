def readtext():
  f=open("input.txt","r")
  r=f.readlines()
  for i in range(0,len(r)):
    r[i]=r[i].replace("\n","")
  search=r[0]
  start_state=r[1]
  goal_state=r[2]
  linenumber=int(r[3])
  sunday_linenum=int(r[linenumber+4])
  
  for i in range(4,linenumber+4):
    r[i]=r[i].split(' ')
  for i in range(linenumber+5,linenumber+sunday_linenum+5):
    r[i]=r[i].split(' ')
  trafficlines=r[4:linenumber+4]
  sunday_trafficlines=r[linenumber+5:linenumber+sunday_linenum+5]
  return {'start':start_state,
              'goal':goal_state,
              'n_traffic':linenumber,
              'n_sunday':sunday_linenum,
              'traffic_l':trafficlines,
              'sunday_l':sunday_trafficlines,
              'search':search}
class nodes:
  def __init__(self,state,pathcost,h,f):
    self.state=state
    self.parent=[]
    self.pathcost=pathcost
    self.h=h
    self.f=f
def find_child(p):
  r=readtext()
  children=[]
  num=r['n_traffic']
  traffic=r['traffic_l']
  for i in range(0,len(traffic)):
    temp=traffic[i]
    if (temp[0]==p.state):
      state=temp[1]
      if (r['search']=='BFS' or r['search']=='DFS'):
        pathC=p.pathcost+1
        n=nodes(state,pathC,None,None)
        children.append(n)
      elif(r['search']=='UCS'):
        pathC=p.pathcost+int(temp[2])
        n=nodes(state,pathC,None,None)
        (n.parent).append(p)
        children.append(n)
      elif(r['search']=='A*'):
        pathC=p.pathcost+int(temp[2])
        l=r['sunday_l']
        h=0
        for i in range(0,len(l)):
          t=l[i]
          if (t[0]==state):
            h=int(t[1])
        n=nodes(state,pathC,h,h+pathC)
        (n.parent).append(p)
        children.append(n)
  return children

def solution(goal,start,write_list,d):
  f=open("output.txt","w")
  if (goal.state==start):
    write_list.append(goal.state+" "+str(goal.pathcost)+"\n")
  else:
    discovered_n=d[goal]
    solution(discovered_n,start,write_list,d)
    write_list.append(goal.state+" "+str(goal.pathcost)+"\n")
        
  f.writelines(write_list)
    
def goal_test(state,goal):
  if (state==goal):
    return True
  else:
    return False
    
def BFS():
  inputs=readtext()
  start=inputs['start']
  goal=inputs['goal']
  n=nodes(start,0,None,None)
  l=[]
  d={}
  explored=[]
  if (goal_test(start,goal)): 
    solution(n,start,l, d)
    return
  frontier=[]
  frontier.append(n) 
  while(1):
    if not frontier:
      return
    n=frontier.pop(0)
    test=[]
    for i in frontier:
      test.append(i.state)  
    if (goal_test(n.state,goal)):
      solution(n,start,l,d)
      return
    explored.append(n.state)
    if find_child(n):
      for i in find_child(n):
        if ((i.state) not in explored and i.state not in test):
          d[i]=n
          frontier.append(i)
          test=[]
          for i in frontier:
            test.append(i.state)
          
def DFS():
  inputs=readtext()
  start=inputs['start']
  goal=inputs['goal']
  n=nodes(start,0,None,None)
  explored=[]
  frontier=[]
  frontier.append(n)
  l=[]
  d={}
  while(1):
    if not frontier: 
      return
    n=frontier.pop(0)
    test=[]
    for i in frontier:
      test.append(i.state)
    if (goal_test(n.state,goal)):
      solution(n,start,l,d)
      return
    explored.append(n.state)
    if find_child(n):
      m=find_child(n)
      m.reverse() #check
      for i in m:
        if ((i.state) not in explored and i.state not in test): 
          d[i]=n
          frontier.insert(0,i)
          test=[]
          for i in frontier:
            test.append(i.state)

def UCS():
  inputs=readtext()
  start=inputs['start']
  goal=inputs['goal']
  n=nodes(start,0,None,None)
  closed=[]
  frontier=[]
  frontier.append(n)
  l=[]
  d={}
  while(1):
    if not frontier:
      return
    n=frontier.pop(0)
    if (goal_test(n.state,goal)):
      solution(n,start,l,d)
      return
    if find_child(n):
      for i in find_child(n):
        f_match=[x for x in frontier if x.state==i.state]
        c_match=[x for x in closed if x.state==i.state]
        if not f_match and not c_match:
          frontier.append(i)
          d[i]=n
        elif f_match:
          if i.pathcost<f_match[0].pathcost: 
            frontier.remove(f_match[0])
            frontier.append(i) 
            d[i]=n
            
        elif c_match:
          if i.pathcost<c_match[0].pathcost:
            closed.remove(c_match[0])
            frontier.append(i)
            d[i]=n           
    closed.append(n)    
    frontier.sort(key = lambda x:x.pathcost,reverse=False)            
       
def A_star():
  inputs=readtext()
  start=inputs['start']
  goal=inputs['goal']
  t=inputs['sunday_l']
  h=0
  for i in range(0,len(t)):
    temp=t[i]
    if (temp[0]==start):
      h=int(temp[1])
  n=nodes(start,0,h,h)
  closed=[]
  frontier=[]
  frontier.append(n)
  l=[]
  d={}
  while(1):
    if not frontier:
      return
    n=frontier.pop(0)
    if (goal_test(n.state,goal)):
      solution(n,start,l,d)
      return
    if find_child(n):
      for i in find_child(n):
        f_match=[x for x in frontier if x.state==i.state]
        c_match=[x for x in closed if x.state==i.state]
        if not f_match and not c_match:
          frontier.append(i)
          d[i]=n 
        elif f_match:
          if i.f<f_match[0].f:
            frontier.remove(f_match[0])
            frontier.append(i)
            d[i]=n   
        elif c_match:
          if i.f<c_match[0].f:
            closed.remove(c_match[0])
            frontier.append(i)
            d[i]=n
    closed.append(n)
    frontier.sort(key = lambda x:x.f,reverse=False)

if __name__ == "__main__":
  inputs=readtext()
  search=inputs['search']
  if search=='UCS':
    UCS()
  elif search=='BFS':
    BFS()
  elif search=='DFS':
    DFS()
  elif search=='A*':
    A_star()

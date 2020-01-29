'''
https://medium.com/coinmonks/what-is-entropy-and-why-information-gain-is-matter-4e85d46d2f01
https://m.habr.com/ru/post/264915/
Методы фильтрации (filter methods) : Informaition gain
'''

import pandas as pd
import pickle
import math 
import scipy.stats as st
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")
    
names=['income (dependent variable)','office','training','experience','sales','managers','efficiency','foreign','area','man']
def create_data():
    xls = pd.ExcelFile("Data.xls")
    sheetX = xls.parse(0)
    t = []
    for i in range(90):
        t.append(sheetX[names[0]][i])
    for e in t:
        if t.count(e) != 1:
            print(1/0)
    l = []
    for i in range(90):
        k = []
        for u in names: 
            if u == names[-1]:
                if sheetX[u][i] == 'No':
                    k.append(0)
                else:
                    k.append(1)
                continue
            k.append(sheetX[u][i])
        
        l.append(k)
    with open("data","wb")as f:
        pickle.dump(l,f)
        
class main:
    def __init__(self):
        self.length = 90.0
        self.dev = 4
        with open('data','r') as f:
            self.data = pickle.load(f)
        self.form_data()
        self.count()
    
    def __str__(self):
        s = ""
        d = {}
        for u in range(len(self.gain)):
            d[names[u+1]] = self.gain[u]
        s_a = (sorted(list(d.values())))
        s_a.reverse()
        m = max(s_a)
        s = ""
        for u in s_a:
            for k in d:
                if d[k] == u:
                    s += k + " -> "+ str(d[k])+'\n'
                    d[k] = m*10
        return s
            
    def form_data(self):
        ind = []
        q = int(self.length/self.dev)
        for u in range(len(names)-3):
            re = []
            for w in range(int(self.length)):
                re.append(self.data[w][u])
            re = sorted(re)
            lis = []
            for c in range(1,self.dev):
                lis.append(re[q*c])
            lis.append(max(re))
            ind.append(lis)
        self.formed = []
        self.ind = ind
        for y in self.data:
            tr = []
            for g in range(len(y)-3):
                for n in range(self.dev):
                    if y[g] <= ind[g][n]:
                        tr.append(self.dev-n-1)
                        break
            self.formed.append(tr+[y[-3],y[-2],y[-1]])
        
    def count(self):
        self.gain = []
        inc = [i[0] for i in self.formed]
        par_e = -1*sum([(inc.count(r)/self.length)*math.log(inc.count(r)/self.length,2.0) for r in range(self.dev)])
        for i in range(1,len(names)):
            xz = self.dev
            cou = [[] for index in range(xz)]
            if i == 7:
                cou = [[],[],[]]
                xz = 3
            if i > 7:
                xz = 2
                cou = [[],[]]
                
            for u in self.formed:
                cou[u[i]].append(u[0])
                
            wer = []
            for r in range(xz):
                inf = []
                for u in range(self.dev):
                    inf.append(cou[r].count(u))
                wer.append(st.entropy(inf,base =2))
                    
            #wer = [st.entropy([cou[r].count(0),cou[r].count(1),cou[r].count(2)],base=2)for r in range(xz)]
            self.gain.append(par_e - sum([(len(cou[r])/self.length) * wer[r] for r in range(xz)]))
            del cou
                        
    
if __name__ == "__main__" :
    create_data()
    #try:
    cl = main()
    print (cl)
    #except ValueError:
        #print ("bad")
        

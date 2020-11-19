#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:20:47 2020

@author: viktorstenby
"""

def generate_testcase(ncandidates=8, nvotes=10):
    import pandas as pd
    import numpy as np
    #Name of candidates
    candidates = ['Arne', 'Bob', 'Cecilie', 'Dennis', 'Erika', 'Freja', \
                  'Gunnar', 'Hanne', 'Ida', 'Johan', 'Karl', 'Lars']
    
    if ncandidates > 12:
        raise ValueError("Hopefully you won't be that many...")
    
    candidates = candidates[:ncandidates]
        
    x = np.arange(1,ncandidates+1)
    
    votes = np.zeros([nvotes, ncandidates])
    for i in range(nvotes):
        votes[i,:] = np.random.permutation(x)
    
    df = pd.DataFrame(columns=candidates, data=votes.astype(int))
    return df

def main():
    import sys
    import pandas as pd
    import numpy as np
    if len(sys.argv) <= 1:
        raise ValueError('Too few arguments.')
    elif len(sys.argv) > 3:
        raise ValueError('Too many arguments.')
    else:
        
        ncandidates = int(sys.argv[1])
        nvotes = int(sys.argv[2])
        
        df = generate_testcase(ncandidates, nvotes)
        df.to_csv('test.csv',index=False)

if __name__ == "__main__":
    main()
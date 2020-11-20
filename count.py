#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:11:45 2020

@author: viktorstenby
"""

import pandas as pd
import numpy as np

def print_results(running, votecount, ncount):
    votepct = votecount/np.sum(votecount)*100
    
    s = 'The votes have been counted. These are the results:'
    print(f'Count {ncount}'.center(len(s)))
    print(s)
    for candidate, votes, pct in zip(running, votecount, votepct):
        pct_string = format(np.round(pct,2),'.2f').rjust(5)
        print(candidate.ljust(20) + f'{int(votes)} ({pct_string}%)'.rjust(len(s)-20))
    print('')

def read_votes(path):
    df = pd.read_csv(path)

    if 'Tidsstempel' in df.columns:
        #Google Sheets csv file
        df.columns = [x.replace('Stemmeseddel','').strip().replace('[','').replace(']','') for x in df.columns]
        df = df.drop(['Tidsstempel','Studienummer'],axis=1)
        
    return df

def main():
    import sys
    try:
        path = ' '.join(sys.argv[1:])
    except:
        print('.csv file not found')
        return
    
    vote_df = read_votes(path)
      
    #Tiebreak methods (if multiple candidates have the lowest number of votes)
    #All means that all candidates with the same low amount of vote should be eliminated.
    tiebreak_method = 'all'
    
    #Coin means that a coin is flipped among the candidates with the same low amount of votes.
    #tiebreak_method = 'coin'
    
    #All candidates are running
    running = vote_df.columns.to_numpy()
    
    i = 0
    # -- Alternative Vote, START --
    while True:
        i += 1
        
        votecount = np.zeros(len(running),)
        
        for n, vote in vote_df.iterrows():
            vote = vote.to_numpy()
            
            #Sort the candidates based on vote. 
            #Here, vote contains 1:ncandidate, so this sort cannot go wrong.
            preferences = vote_df.columns[np.argsort(vote)]
            
            #Keep the candidates who are not eliminated.
            preferences = preferences[np.isin(preferences, running)]
            
            #Take the top preference.
            candidate = preferences[0]        
            
            #Add the vote to the top candidate.
            votecount[running == candidate] += 1
       
        #If all of the remaining candidates have the same amount of votes,
        #then there is a draw.
        if len(np.unique(votecount)) == 1:
            raise ValueError('Draw.')
       
        #Count the percentages
        votepct = votecount/np.sum(votecount)*100
        
        print_results(running, votecount, i)
        if np.any(votepct >= 50):
            #If votepct is split 50/50, then it is a draw.            
            winner = running[np.argmax(votecount)]
            print(f'{winner} wins.')
            break
        else:
            #Here, argmin would give one person, but if several people have
            #the same low amount of votes, they should all be eliminated.
            least_popular = running[votecount == votecount.min()] 
            if len(least_popular) == 1:
                #Eliminate a single candidate.
                least_popular = least_popular[0]
                print(f'No candidate exceeds 50%. {least_popular} is eliminated.\n')
            else:
                #Several candidates have the same low amount of votes.
                if tiebreak_method is 'all':
                    s = ', '.join(least_popular[:-1]) + ' and ' + least_popular[-1]
                    print(f'No candidate exceeds 50%. {s} are eliminated.\n')
                elif tiebreak_method is 'coin':
                    #Draw a single one at random
                    least_popular = np.random.choice(least_popular,1)
                    least_popular = least_popular[0]
                    print(f'No candidate exceeds 50%. A coin is flipped, and {least_popular} is eliminated.\n')
                else:
                    raise ValueError('Unknown tiebreak method.')
                    
            #Keep those who should not be eliminated.
            running = running[np.invert(np.isin(running,least_popular))]
        # -- Alternative Vote, END --
        

if __name__ == "__main__":
    main()
    
    

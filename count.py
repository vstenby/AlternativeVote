#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import argparse
import os
    
def verify(infile, print_count = False):
    '''
    Verify the vote, i.e. count the number of votes. 
    '''
    
    if not os.path.exists('constituents.csv'):
        print('constituents.csv is needed to verify vote.')
        return
        
    constituents = pd.read_csv('constituents.csv')
    
    if 'Studienummer' not in constituents.columns:
        return
    
    constituents = constituents.sort_values('Studienummer')
          
    if not infile.endswith('.csv'): infile += '.csv'
    
    voters = pd.read_csv(infile)['Studienummer'].to_numpy()
    unique_voters = np.sort(np.unique(voters))
    
    s1 = 'Studynumber'.ljust(15) + 'Votes cast'.center(10) + 'Constituent'.center(20) + 'Valid'.center(10) + 'Name'.center(30)
    
    if print_count:
        print(s1)
        print('-'*len(s1))
        
    status = 'valid'
    
    for voter in unique_voters:
        votecount   = np.sum(voter == voters)
        constituent = voter in constituents['Studienummer'].to_numpy()
        valid_vote = votecount == 1 and constituent
        if not valid_vote: status = 'invalid'
        if constituent:
            name = constituents['Navn'].loc[constituents['Studienummer'] == voter].iloc[0]
        else:
            name = ''
            
        s2 = voter.ljust(15) + str(votecount).center(10) + str(constituent).center(20) + str(valid_vote).center(10) + name.ljust(30)
        
        if print_count:
            print(s2)
    
    if print_count:
        print('')
        print(f'Conclusion: The vote is {status} with a total of {len(unique_voters)} unique voters.')
        print('')
        
    return status

def print_results(running, votecount, ncount):
    votepct = votecount/np.sum(votecount)*100
    
    s = 'The votes have been counted. These are the results:'
    print(f'Count {ncount} (n = {int(votecount.sum())})'.center(len(s)))
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

    #Set up the arguments. 
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default=None, type=str, help='specify the path to the csv you want to count.')
    parser.add_argument('--exclude', default="['']", type=str, help='specify the candidates you want to exclude from the count.')
    parser.add_argument('--tiebreak', default='stop', choices = ['stop', 'coin', 'all'], type=str, help='specify the tiebreak method you want to use. Default is to stop the count.')
    parser.add_argument('--ignore-invalid', default=False, action='store_true', help='allows a non-valid vote to be counted.')
    
    #TODO: This should be implemented!
    #parser.add_argument('--include-nonconstituents', default=False, action='store_true', help='decides whether or not nonconstituents should be allowed to vote.')
    
    args = parser.parse_args()
    
    #Set the path
    path = args.path

    not_counted = eval(args.exclude)
    not_counted = [x for x in not_counted if x != '']
    
    status = verify(path, print_count=True)
    if (status == 'invalid')&(not args.ignore_invalid):
        return
    
    if len(not_counted) == 0:
        s = 'All candidates are running.'
    elif len(not_counted) == 1:
        s = not_counted[0] + ' is not counted.'
    else:
        s = ', '.join(not_counted[:-1]) + ' and ' + not_counted[-1] + ' are not counted.'
    print(s)
    print('')
    
    not_counted = np.asarray(not_counted)
    
    vote_df = read_votes(path)
      
    #All candidates are running
    running = vote_df.columns.to_numpy()
    
    #Remove the candidates that we should not count.
    running = running[np.invert(np.isin(running,not_counted))]
    
    i = 0
    # -- Alternative Vote, START --
    while True:
        i += 1
        
        votecount = np.zeros(len(running),)
        
        for n, vote in vote_df.iterrows():
            vote = vote.to_numpy()
                    
            #Drop candidates where this voter does not have a preference.
            candidates = vote_df.columns[~pd.isna(vote)]
            
            #Drop na votes such that we can sort on it.
            vote = vote[~pd.isna(vote)]
            
            #Sort the candidates based on vote. Here, candidates which the voter does not have a preference is removed.
            preferences = candidates[np.argsort(vote)]
            
            #Keep the candidates who are not eliminated.
            preferences = preferences[np.isin(preferences, running)]
            

            #Try to take the top preference, otherwise the vote is not counted because the voter does not have an opinion.
            try:
                candidate = preferences[0]
            except:
                #This voter does not have an opinion.
                continue
            
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
                if args.tiebreak == 'all':
                    s = ', '.join(least_popular[:-1]) + ' and ' + least_popular[-1]
                    print(f'No candidate exceeds 50%. {s} are eliminated.\n')
                elif args.tiebreak == 'coin':
                    #Draw a single one at random
                    least_popular = np.random.choice(least_popular,1)
                    least_popular = least_popular[0]
                    print(f'No candidate exceeds 50%. A coin is flipped, and {least_popular} is eliminated.\n')
                elif args.tiebreak == 'stop':
                    print(f"The count has come to an end since args.tiebreak = 'stop'.")
                    return
                else:
                    raise NotImplementedError('Tiebreak method is not implemented.')
                    
            #Keep those who should not be eliminated.
            running = running[np.invert(np.isin(running,least_popular))]
            if len(running) == 1:
                winner = running[0]
                print(f'{winner} wins.')
                break
                
        # -- Alternative Vote, END --
        

if __name__ == "__main__":
    main()
    
    

# AlternativeVote

## About 

This code was written for the S/M-KID 2021 KABS election, where we wanted to use the Alternative Vote system. CGP Grey has made a good video explaining how the Alternative Vote system works here:

[![Watch the video here](https://img.youtube.com/vi/3Y3jE3B8HsE/maxresdefault.jpg)](https://www.youtube.com/watch?v=3Y3jE3B8HsE)

You can also read more about the Alternative Vote, or Instant-runoff voting as it's also called, on the Wikipedia page [here](https://en.wikipedia.org/wiki/Instant-runoff_voting).

## Download 

To download this repository, type the following in your terminal:
  
`` git clone https://github.com/vstenby/AlternativeVote.git ``

## Voting Procedure

At the moment, this code only works with **full preferential voting**. This means that all voters have to mark a preference for *every* candidate. At the S/M-KID KABS21 election, this will be done in Google Forms. An example of a form can be seen [here](https://forms.gle/i724RPzX8FH3e6fU8). When downloaded, this form is the ``form_demo.csv`` file. 

## Functions

### `count.py`

The main function of this repository is `count.py`, which counts the votes in a given csv file and prints the results to the terminal. 

The function is called as follows:

``python count.py sheets_demo.csv``

### `gentest.py`

If you want to test the counter, you can generate test examples with the function `gentest.py`. 
This function takes two inputs, which are the number of candidates and the number of votes cast.

If you for instance want to generate a count, where 20 voters choose between 10 candidates, you call the function like this: 

``python gentest.py 10 20``

## Examples

### Small scale example 

Say we have an election with 5 candidates and 10 voters. We can generate this test case by calling `python gentest.py 5 10`. We inspect the csv-file which looks like this:

|Arne|Bob|Cecilie|Dennis|Erika|
|----|---|-------|------|-----|
|5   |2  |3      |1     |4    |
|3   |1  |5      |2     |4    |
|1   |2  |4      |3     |5    |
|3   |2  |1      |4     |5    |
|3   |1  |5      |4     |2    |
|3   |5  |2      |1     |4    |
|4   |3  |1      |5     |2    |
|4   |2  |3      |1     |5    |
|5   |2  |4      |1     |3    |
|4   |5  |3      |2     |1    |

We can count the vote `python count.py test.csv`, which prints the following to the terminal:

```
                      Count 1                      
The votes have been counted. These are the results:
Arne                                     1 (10.00%)
Bob                                      2 (20.00%)
Cecilie                                  2 (20.00%)
Dennis                                   4 (40.00%)
Erika                                    1 (10.00%)

No candidate exceeds 50%. Arne and Erika are eliminated.

                      Count 2                      
The votes have been counted. These are the results:
Bob                                      3 (30.00%)
Cecilie                                  2 (20.00%)
Dennis                                   5 (50.00%)

Dennis wins.
```
We can see that the 2 votes were moved. The vote from Arne was moved to Bob, since this voter had Bob as their 2nd choice. Likewise, a vote for Erika was moved to Dennis since this voter had Dennis as their 2nd priority. Dennis won since he had 50% or more of the total votes. 

### Larger scale example

Another test case is generated, where we have 10 candidates and 50 votes using `gentest.py`. Like previously, this is counted `count.py` giving the following output:

```
                      Count 1                      
The votes have been counted. These are the results:
Arne                                     2 ( 4.00%)
Bob                                      7 (14.00%)
Cecilie                                  5 (10.00%)
Dennis                                   3 ( 6.00%)
Erika                                    4 ( 8.00%)
Freja                                    7 (14.00%)
Gunnar                                   9 (18.00%)
Hanne                                    7 (14.00%)
Ida                                      4 ( 8.00%)
Johan                                    2 ( 4.00%)

No candidate exceeds 50%. Arne and Johan are eliminated.

                      Count 2                      
The votes have been counted. These are the results:
Bob                                      7 (14.00%)
Cecilie                                  6 (12.00%)
Dennis                                   4 ( 8.00%)
Erika                                    4 ( 8.00%)
Freja                                    8 (16.00%)
Gunnar                                   9 (18.00%)
Hanne                                    8 (16.00%)
Ida                                      4 ( 8.00%)

No candidate exceeds 50%. Dennis, Erika and Ida are eliminated.

                      Count 3                      
The votes have been counted. These are the results:
Bob                                     10 (20.00%)
Cecilie                                  8 (16.00%)
Freja                                    8 (16.00%)
Gunnar                                  15 (30.00%)
Hanne                                    9 (18.00%)

No candidate exceeds 50%. Cecilie and Freja are eliminated.

                      Count 4                      
The votes have been counted. These are the results:
Bob                                     16 (32.00%)
Gunnar                                  22 (44.00%)
Hanne                                   12 (24.00%)

No candidate exceeds 50%. Hanne is eliminated.

                      Count 5                      
The votes have been counted. These are the results:
Bob                                     19 (38.00%)
Gunnar                                  31 (62.00%)

Gunnar wins.
```

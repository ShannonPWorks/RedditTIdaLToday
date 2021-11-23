# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 09:58:41 2021

@author: shannon.perry
"""
import pandas as pd
from datetime import datetime
#the below is for installing praw if necessary
try: 
    import praw
except:
    import pip
    pip.main(['install','praw'])

#this establishes the call to reddit r/TIdaL's data for today
reddit = praw.Reddit(client_id='sBGqufQCL_CZAFPAX82ZTQ', \
                     client_secret='7kIGg5WjbnqVIfrI5vLsQbgnRXOq-g', \
                     user_agent='potato1', \
                     username='bigbadpotatochip', \
                     password='hashbrownfromdunkin')
subreddit = reddit.subreddit('TIdaL')
tidal_today_subreddit = subreddit.top('day')

#this creates the data dictionaries to be populated by the submissions and comments
submission_dict = { 
    "title":[]
    ,"selftext":[]
    ,"id":[]
    ,"upvote_ratio":[]
    ,"num_comments":[]
    ,"link_flair_text":[]
    ,"score":[]
    ,"created_utc":[]
    ,"author":[]
    ,"author_fullname":[]
    ,"retrieved_on":[]
    }
comments_dict = {
    "comment_body":[]   
    ,"comment_id":[]      
    ,"comment_score":[]  
    ,"comment_author":[]  
    #,"comment_author_fullname":[] #this does not exist in praw
    ,"comment_parent_id":[]  
    ,"comment_created_utc":[] 
    }

#this populates the data, comments must be nested within the submission loop
for submission in tidal_today_subreddit:
    if not submission.stickied:
        submission_dict["title"].append(submission.title)
        submission_dict["selftext"].append(submission.selftext)
        submission_dict["id"].append(submission.id)
        submission_dict["upvote_ratio"].append(submission.upvote_ratio)
        submission_dict["num_comments"].append(submission.num_comments)
        submission_dict["link_flair_text"].append(submission.link_flair_text)
        submission_dict["score"].append(submission.score)
        submission_dict["created_utc"].append(submission.created_utc)
        submission_dict["author"].append(submission.author_fullname)
        submission_dict["author_fullname"].append(submission.author_fullname)
        submission_dict["retrieved_on"].append(datetime.now())
        submission.comments.replace_more(limit = 1)
        for comment in submission.comments.list():
            comments_dict["comment_body"].append(comment.body)
            comments_dict["comment_id"].append(comment.id)
            comments_dict["comment_score"].append(comment.score)
            comments_dict["comment_author"].append(comment.author)
            #comments_dict["comment_author_fullname"].append(comment.author_fullname) #this does not exist in praw
            comments_dict["comment_parent_id"].append(comment.parent_id) #key field to join these tables for query
            comments_dict["comment_created_utc"].append(comment.created_utc)

#this populates the dataframes and generates the csv files            
submission_data = pd.DataFrame(submission_dict)
comments_data = pd.DataFrame(comments_dict)
submission_data.to_csv('topicstoday.csv', index=False) 
comments_data.to_csv('commentstoday.csv', index=False)


#this section is for viewing in console 
#can be deleted when not of interest
print('Date/Time:',datetime.now())
print('Topic attributes:',dir(subreddit))
print('Submission attributes:',dir(tidal_today_subreddit))
for submission in subreddit.top(limit=1):
    print('Comment attributes:',dir(submission.comments)) 
print('Submissions Today:')
for submission in subreddit.top('day'):
    if not submission.stickied:
        print(submission.id, submission.title, sep=',')
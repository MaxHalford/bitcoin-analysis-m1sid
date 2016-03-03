import pandas as pd

df = pd.read_csv('../data/dataframes/allTweets.csv')

#import sys, os
#import urllib2
#import re
#
#print(sys.argv)
#_input = sys.argv[1]
#_separator = sys.argv[2]
#
#dict_terms = {}
#dict_hashtags ={}
#dict_tweets = {}
#dict_users = {}
#dict_dates = {}
#dict_urls = {}
#
#with open(_input,"r") as input:
#    for line in input:
#
#        # split line according to _separator
#        t_line = line.split(_separator)
#        user = t_line[0]
#        date = t_line[2].strip(' \t\n\r')
#        terms, hashtags, urls = get_info_from_tweet(t_line[1])
#
#        id_user = 0
#        id_date = 0
#
#        #TWEET
#        id_tweet = len(dict_tweets)+1
#        dict_tweets[id_tweet]=""
#        write_to_tweet(id_tweet)
#
#        #USER
#        if user in dict_users:
#            id_user = dict_users[user]
#        else :
#            id_user = dict_users[user] = len(dict_users)+1
#            write_to_user(id_user,user)
#
#        #DATE
#        if date in dict_dates:
#            id_date = dict_dates[date]
#        else :
#            id_date = dict_dates[date] = len(dict_dates)+1
#            write_to_date(id_date,date)
#
#        write_to_tweeter(id_user,id_tweet)
#        write_to_posted_at(id_tweet,id_date)
#
#
#        for t in terms:
#            id_term = 0 
#            if t in dict_terms:
#                id_term = dict_terms[t]
#            else :
#                id_term = dict_terms[t] = len(dict_terms)+1
#                write_to_term(id_term,t)
#            write_to_term_in_tweet(id_tweet,id_term)
#
#        for h in hashtags:
#            id_hashtag = 0 
#            if h in dict_terms:
#                id_hashtag = dict_hashtags[h]
#            else :
#                id_hashtag = dict_hashtags[h] = len(dict_hashtags)+1
#                write_to_hashtag(id_hashtag,h)
#            write_to_hashtag_in_tweet(id_tweet,id_hashtag)
#
#        for u in urls:
#            id_url = 0 
#            if u in dict_urls:
#                id_url = dict_urls[u]
#            else :
#                id_url = dict_urls[u] = len(dict_urls)+1
#                write_to_url(id_url,u)
#            write_to_url_in_tweet(id_tweet,id_url)

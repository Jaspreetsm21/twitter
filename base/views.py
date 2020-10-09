from django.shortcuts import render,redirect
import tweepy
import emoji
import iso8601
from .forms import TwitterForm
from .models import Twitter_Model
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()
# Create your views here.

def home(request):

    if request.method == 'POST':
        form = TwitterForm(request.POST)
        if form.is_valid():
                form.save()

    form = TwitterForm()
    
    twitters = Twitter_Model.objects.all()
    twttt_created  = []
    for tk in twitters:
        t1 = tk
    
        twttt_created.append(tk)
    kk =(twttt_created[-1])
    #print(kk)

    consumer_key = 'WURYy5DNwdoKNuq36C2ME9MG5'
    consumer_secret = 'GAFW5dHB7VJxtzefeZgi3YuSRIOBSILAIjzSZZqLYfaS2yFXJN'
    access_token_key = '1145240407229587458-WiSLolua6cpjAyeyPqAY7pfEkZegEv'
    access_token_secret = 'GA0h27EWeaucrnkSzRsYNqe6FGPxVHweAeS6kTzG3weFi'
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

    # Access to user's access key and access secret 
    auth.set_access_token(access_token_key, access_token_secret) 

    # Calling api 
    api = tweepy.API(auth)

    # 200 tweets to be extracted 
    number_of_tweets=200
    user = api.get_user(screen_name=kk)
    twt_followers = []
    twt_friends = []

    #info
    followers = user.followers_count
    friends = user.friends_count
    twt_name = user.name 
    twt_desc = user.description
    twt_followers.append(followers)
    twt_friends.append(friends)
    profile_pic = user.profile_image_url

    #print(tweets)
    # Empty Array 
    tmp=[]
    twt_created = []
    tt_created = []
    twt_id = []
    twt_likes = []
    twt_retweet = []
    count = []
    if user.protected ==False:
        name = kk
    else:
        name = 'Twitter'  

    tweets = api.user_timeline(screen_name=name, count = 999 ,include_rts = False,exclude_replies=False)


    for x in tweets:
        j = x.text
        j = j + ''.join(c for c in j if c in emoji.UNICODE_EMOJI)
        c = len(x.text)
        if c > 1:
            c =1 
        else:
            c = 0
        twt_created_1 = (x.created_at).strftime("%d %m %Y")
        twt_created_2 = (x.created_at).strftime("%d %b %Y")
        twt_id_1 = x.id
        twt_likes_1 = x.favorite_count
        twt_retweet_1 =x.retweet_count
        tt_created.append(twt_created_2)
        count.append(c)
        tmp.append(j)
        twt_created.append(twt_created_1)
        twt_id.append(twt_id_1)
        twt_likes.append(twt_likes_1)
        twt_retweet.append(twt_retweet_1)

        #result1 = {'d':zip(twt_created,tmp,twt_id,twt_likes,twt_retweet),'kk':kk,'form':form,'profile_pic':profile_pic,'twt_followers':twt_followers[0],'twt_friends':twt_friends[0],'twt_name':twt_name,'twt_desc':twt_desc}
    #return render(request, 'base/home.html',result1)
    df = pd.DataFrame({'tweet':tmp,
        'tweet_count':(count),
        'tweet_send':twt_created,
        'twt_likes':twt_likes,
        'twt_retweet':twt_retweet,
        'twt_id':twt_id})
    
    top5 = df.sort_values(by='twt_likes', ascending=False,)[:5]
    t5_tweet = top5['tweet'].to_list()
    t5_send = top5['tweet_send'].to_list()
    t5_like = top5['twt_likes'].to_list()
    t5_retweet = top5['twt_retweet'].to_list()
    t5_id = top5['twt_id'].to_list()

    df['tweet_send'] = pd.to_datetime(df['tweet_send'],format='%d %m %Y')
    df = df.drop_duplicates()
    new_data = pd.pivot_table(index='tweet_send',values='tweet_count',data=df,aggfunc='sum')
    new_data = new_data.reset_index()
    result = new_data.sort_values(('tweet_send'), ascending=False)
    result['twt_send'] = result['tweet_send'].dt.strftime("%d %b")

# Today = pd.to_datetime('today',format='%Y-%m-%d')#.strftime("%Y-%m-%d")
    Today = datetime.utcnow().replace(minute=0, hour=0, second=0, microsecond=0)
    last_90days = start_date = Today - timedelta(days=90)

    last_14days = start_date = Today - timedelta(days=14)
    Yesterday = start_date = Today - timedelta(days=1)
    tweets_90days = df[(df['tweet_send']>(last_90days))]

    tweets_14days = result[(result['tweet_send']>(last_14days))]
    No_tweet_14_sum = tweets_14days['tweet_count'].sum()
    No_tweet_14_avg = round(tweets_14days['tweet_count'].mean(),0)
    try:
        tweet_today = result[(result['tweet_send']>Yesterday)]
    except:
        tweet_today = None
    twt_today = tweet_today['tweet_count'].sum()
    max_tweet = tweets_90days['tweet_count'].max()
    total_tweet = result['tweet_count'].sum()
    twt_90_total = tweets_90days['tweet_count'].sum()
    mean_tweet = round(tweets_90days['tweet_count'].mean(),1)
    context = {'twt_today':twt_today,'max_tweet':max_tweet,'total_tweet':twt_90_total,'No_tweet_14_avg':No_tweet_14_avg,'mean_tweet':mean_tweet,'d':zip(tt_created[:20],tmp[:20],twt_id[:20],twt_likes[:20],twt_retweet[:20]),'z':zip(t5_tweet,t5_send,t5_like,t5_retweet,t5_id),'kk':kk,'form':form,'profile_pic':profile_pic,'twt_followers':twt_followers[0],'twt_friends':twt_friends[0],'twt_name':twt_name,'twt_desc':twt_desc}
    return render(request, 'base/home.html',context)#
 

from chartjs.views.lines import BaseLineChartView
from django.views.generic import TemplateView
from django.http import JsonResponse

# def get_data(request):
#     qs_count = User.objects.all().count()
#     labels = ["Users","Blue","Yellow","Green","Purple","Orange"]
#     default_items = [qs_count, 2, 5, 5, 2, 4, 6]
#     data = {
#         "labels": labels,
#         "default": default_items,
#     }
#     return JsonResponse(data) #Rrender(request, 'base/home.html',data)




def get_data(request):

    if request.method == 'POST':
        form = TwitterForm(request.POST)
        if form.is_valid():
                form.save()
    form = TwitterForm()
    
    twitters = Twitter_Model.objects.all()
    twttt_created  = []
    for tk in twitters:
        t1 = tk
    
        twttt_created.append(tk)
    kk =(twttt_created[-1])
    #print(kk)

    consumer_key = 'WURYy5DNwdoKNuq36C2ME9MG5'
    consumer_secret = 'GAFW5dHB7VJxtzefeZgi3YuSRIOBSILAIjzSZZqLYfaS2yFXJN'
    access_token_key = '1145240407229587458-WiSLolua6cpjAyeyPqAY7pfEkZegEv'
    access_token_secret = 'GA0h27EWeaucrnkSzRsYNqe6FGPxVHweAeS6kTzG3weFi'
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

    # Access to user's access key and access secret 
    auth.set_access_token(access_token_key, access_token_secret) 

    # Calling api 
    api = tweepy.API(auth) 

    # 200 tweets to be extracted 
    number_of_tweets=200
    user = api.get_user(screen_name=kk)

    twt_followers = []
    twt_friends = []

    #info
    followers = user.followers_count
    friends = user.friends_count
    twt_name = user.name 
    twt_desc = user.description
    twt_followers.append(followers)
    twt_friends.append(friends)
    profile_pic = user.profile_image_url

    #print(tweets)
    # Empty Array 
    tmp=[]
    twt_created = []
    twt_id = []
    twt_likes = []
    twt_retweet = []
    count = []

    if user.protected ==False:
        name = kk
    else:
        name = 'Twitter' 
    
    tweets = api.user_timeline(screen_name= name, count = 999, include_rts = False, exclude_replies=False)

    for x in tweets:
        j = x.text
        j = j + ''.join(c for c in j if c in emoji.UNICODE_EMOJI)
        c = len(x.text)
        if c > 1:
            c =1 
        else:
            c = 0
        twt_created_1 = ((x.created_at).strftime("%d %m %Y"))
        twt_id_1 = x.id
        twt_likes_1 = (x.favorite_count)
        twt_retweet_1 =x.retweet_count
        #twt_followers_1 = x.followers_count
        #twt_friends_1 = x.friends_count
        count.append(c)
        tmp.append(j)
        default_items =(tmp)
        #print(default_items)
        twt_created.append((twt_created_1))
        twt_created = (twt_created)#.sort(reverse=True)
        twt_id.append(twt_id_1)
        twt_likes.append(twt_likes_1)
        twt_retweet.append(twt_retweet_1)

    df = pd.DataFrame({'tweet':tmp,
                'tweet_count':(count),
                'tweet_send':twt_created})
    df['tweet_send'] = pd.to_datetime(df['tweet_send'],format='%d %m %Y')
    df = df.drop_duplicates()


    Today = datetime.utcnow().replace(minute=0, hour=0, second=0, microsecond=0)
    last_90days = start_date = Today - timedelta(days=90)
    Yesterday = start_date = Today - timedelta(days=1)
    #print(last_90days)
    tweets_90days = df[(df['tweet_send']>(last_90days))]
    #tweets_90days.to_csv('90.csv')
    new_data = pd.pivot_table(index='tweet_send',values='tweet_count',data=tweets_90days,aggfunc='sum')
    new_data = new_data.reset_index()
    result = new_data.sort_values(('tweet_send'), ascending=False)
    result['twt_send'] = result['tweet_send'].dt.strftime("%d %b")

    total = result['tweet_count'].to_list()
    send = result['twt_send'].to_list()
    #result.to_csv('result.csv')
    #send = sorted(send,key=lambda x: datetime.datetime.strptime(x, '%d %b'),reverse=True)

    data = {
    "labels": send,
    "default": total
    }
    return JsonResponse(data)

def date30d(request):

    if request.method == 'POST':
        form = TwitterForm(request.POST)
        if form.is_valid():
                form.save()

    form = TwitterForm()
    
    twitters = Twitter_Model.objects.all()
    twttt_created  = []
    for tk in twitters:
        t1 = tk
    
        twttt_created.append(tk)
    kk =(twttt_created[-1])
    #print(kk)

    consumer_key = 'WURYy5DNwdoKNuq36C2ME9MG5'
    consumer_secret = 'GAFW5dHB7VJxtzefeZgi3YuSRIOBSILAIjzSZZqLYfaS2yFXJN'
    access_token_key = '1145240407229587458-WiSLolua6cpjAyeyPqAY7pfEkZegEv'
    access_token_secret = 'GA0h27EWeaucrnkSzRsYNqe6FGPxVHweAeS6kTzG3weFi'
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

    # Access to user's access key and access secret 
    auth.set_access_token(access_token_key, access_token_secret) 

    # Calling api 
    api = tweepy.API(auth)

    # 200 tweets to be extracted 
    number_of_tweets=200
    user = api.get_user(screen_name=kk)
    twt_followers = []
    twt_friends = []

    #info
    followers = user.followers_count
    friends = user.friends_count
    twt_name = user.name 
    twt_desc = user.description
    twt_followers.append(followers)
    twt_friends.append(friends)
    profile_pic = user.profile_image_url

    #print(tweets)
    # Empty Array 
    tmp=[]
    twt_created = []
    tt_created = []
    twt_id = []
    twt_likes = []
    twt_retweet = []
    count = []
    if user.protected ==False:
        name = kk
    else:
        name = 'Twitter'  

    tweets = api.user_timeline(screen_name=name, count = 999 ,include_rts = False,exclude_replies=False)


    for x in tweets:
        j = x.text
        j = j + ''.join(c for c in j if c in emoji.UNICODE_EMOJI)
        c = len(x.text)
        if c > 1:
            c =1 
        else:
            c = 0
        twt_created_1 = (x.created_at).strftime("%d %m %Y")
        twt_created_2 = (x.created_at).strftime("%d %b %Y")
        twt_id_1 = x.id
        twt_likes_1 = x.favorite_count
        twt_retweet_1 =x.retweet_count
        tt_created.append(twt_created_2)
        count.append(c)
        tmp.append(j)
        twt_created.append(twt_created_1)
        twt_id.append(twt_id_1)
        twt_likes.append(twt_likes_1)
        twt_retweet.append(twt_retweet_1)

        #result1 = {'d':zip(twt_created,tmp,twt_id,twt_likes,twt_retweet),'kk':kk,'form':form,'profile_pic':profile_pic,'twt_followers':twt_followers[0],'twt_friends':twt_friends[0],'twt_name':twt_name,'twt_desc':twt_desc}
    #return render(request, 'base/home.html',result1)
    df = pd.DataFrame({'tweet':tmp,
            'tweet_count':(count),
            'tweet_send':twt_created,
            'twt_likes':twt_likes,
            'twt_retweet':twt_retweet,
            'twt_id':twt_id})
    
    top5 = df.sort_values(by='twt_likes', ascending=False,)[:5]
    t5_tweet = top5['tweet'].to_list()
    t5_send = top5['tweet_send'].to_list()
    t5_like = top5['twt_likes'].to_list()
    t5_retweet = top5['twt_retweet'].to_list()
    t5_id = top5['twt_id'].to_list()

    df['tweet_send'] = pd.to_datetime(df['tweet_send'],format='%d %m %Y')
    df = df.drop_duplicates()
    new_data = pd.pivot_table(index='tweet_send',values='tweet_count',data=df,aggfunc='sum')
    new_data = new_data.reset_index()
    result = new_data.sort_values(('tweet_send'), ascending=False)
    result['twt_send'] = result['tweet_send'].dt.strftime("%d %b")

# Today = pd.to_datetime('today',format='%Y-%m-%d')#.strftime("%Y-%m-%d")
    Today = datetime.utcnow().replace(minute=0, hour=0, second=0, microsecond=0)
    last_90days = start_date = Today - timedelta(days=90)

    last_14days = start_date = Today - timedelta(days=14)
    Yesterday = start_date = Today - timedelta(days=1)
    tweets_90days = df[(df['tweet_send']>(last_90days))]

    tweets_14days = result[(result['tweet_send']>(last_14days))]
    No_tweet_14_sum = tweets_14days['tweet_count'].sum()
    No_tweet_14_avg = round(tweets_14days['tweet_count'].mean(),0)
    try:
        tweet_today = result[(result['tweet_send']>Yesterday)]
    except:
        tweet_today = None
    twt_today = tweet_today['tweet_count'].sum()
    max_tweet = tweets_90days['tweet_count'].max()
    total_tweet = result['tweet_count'].sum()
    twt_90_total = tweets_90days['tweet_count'].sum()
    mean_tweet = round(tweets_90days['tweet_count'].mean(),1)
    context = {'twt_today':twt_today,'max_tweet':max_tweet,'total_tweet':twt_90_total,'No_tweet_14_avg':No_tweet_14_avg,'mean_tweet':mean_tweet,'d':zip(tt_created[:20],tmp[:20],twt_id[:20],twt_likes[:20],twt_retweet[:20]),'z':zip(t5_tweet,t5_send,t5_like,t5_retweet,t5_id),'kk':kk,'form':form,'profile_pic':profile_pic,'twt_followers':twt_followers[0],'twt_friends':twt_friends[0],'twt_name':twt_name,'twt_desc':twt_desc}
    return render(request, 'base/date30d.html',context)#





def date14d(request):

    if request.method == 'POST':
        form = TwitterForm(request.POST)
        if form.is_valid():
                form.save()

    form = TwitterForm()
    
    twitters = Twitter_Model.objects.all()
    twttt_created  = []
    for tk in twitters:
        t1 = tk
    
        twttt_created.append(tk)
    kk =(twttt_created[-1])
    #print(kk)

    consumer_key = 'WURYy5DNwdoKNuq36C2ME9MG5'
    consumer_secret = 'GAFW5dHB7VJxtzefeZgi3YuSRIOBSILAIjzSZZqLYfaS2yFXJN'
    access_token_key = '1145240407229587458-WiSLolua6cpjAyeyPqAY7pfEkZegEv'
    access_token_secret = 'GA0h27EWeaucrnkSzRsYNqe6FGPxVHweAeS6kTzG3weFi'
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

    # Access to user's access key and access secret 
    auth.set_access_token(access_token_key, access_token_secret) 

    # Calling api 
    api = tweepy.API(auth)

    # 200 tweets to be extracted 
    number_of_tweets=200
    user = api.get_user(screen_name=kk)
    twt_followers = []
    twt_friends = []

    #info
    followers = user.followers_count
    friends = user.friends_count
    twt_name = user.name 
    twt_desc = user.description
    twt_followers.append(followers)
    twt_friends.append(friends)
    profile_pic = user.profile_image_url

    #print(tweets)
    # Empty Array 
    tmp=[]
    twt_created = []
    tt_created = []
    twt_id = []
    twt_likes = []
    twt_retweet = []
    count = []
    if user.protected ==False:
        name = kk
    else:
        name = 'Twitter'  

    tweets = api.user_timeline(screen_name=name, count = 999 ,include_rts = False,exclude_replies=False)


    for x in tweets:
        j = x.text
        j = j + ''.join(c for c in j if c in emoji.UNICODE_EMOJI)
        c = len(x.text)
        if c > 1:
            c =1 
        else:
            c = 0
        twt_created_1 = (x.created_at).strftime("%d %m %Y")
        twt_created_2 = (x.created_at).strftime("%d %b %Y")
        twt_id_1 = x.id
        twt_likes_1 = x.favorite_count
        twt_retweet_1 =x.retweet_count
        tt_created.append(twt_created_2)
        count.append(c)
        tmp.append(j)
        twt_created.append(twt_created_1)
        twt_id.append(twt_id_1)
        twt_likes.append(twt_likes_1)
        twt_retweet.append(twt_retweet_1)

        #result1 = {'d':zip(twt_created,tmp,twt_id,twt_likes,twt_retweet),'kk':kk,'form':form,'profile_pic':profile_pic,'twt_followers':twt_followers[0],'twt_friends':twt_friends[0],'twt_name':twt_name,'twt_desc':twt_desc}
    #return render(request, 'base/home.html',result1)
    df = pd.DataFrame({'tweet':tmp,
            'tweet_count':(count),
            'tweet_send':twt_created,
            'twt_likes':twt_likes,
            'twt_retweet':twt_retweet,
            'twt_id':twt_id})
    
    top5 = df.sort_values(by='twt_likes', ascending=False,)[:5]
    t5_tweet = top5['tweet'].to_list()
    t5_send = top5['tweet_send'].to_list()
    t5_like = top5['twt_likes'].to_list()
    t5_retweet = top5['twt_retweet'].to_list()
    t5_id = top5['twt_id'].to_list()

    df['tweet_send'] = pd.to_datetime(df['tweet_send'],format='%d %m %Y')
    df = df.drop_duplicates()
    new_data = pd.pivot_table(index='tweet_send',values='tweet_count',data=df,aggfunc='sum')
    new_data = new_data.reset_index()
    result = new_data.sort_values(('tweet_send'), ascending=False)
    result['twt_send'] = result['tweet_send'].dt.strftime("%d %b")

# Today = pd.to_datetime('today',format='%Y-%m-%d')#.strftime("%Y-%m-%d")
    Today = datetime.utcnow().replace(minute=0, hour=0, second=0, microsecond=0)
    last_90days = start_date = Today - timedelta(days=90)

    last_14days = start_date = Today - timedelta(days=14)
    Yesterday = start_date = Today - timedelta(days=1)
    tweets_90days = df[(df['tweet_send']>(last_90days))]

    tweets_14days = result[(result['tweet_send']>(last_14days))]
    No_tweet_14_sum = tweets_14days['tweet_count'].sum()
    No_tweet_14_avg = round(tweets_14days['tweet_count'].mean(),0)
    try:
        tweet_today = result[(result['tweet_send']>Yesterday)]
    except:
        tweet_today = None
    twt_today = tweet_today['tweet_count'].sum()
    max_tweet = tweets_90days['tweet_count'].max()
    total_tweet = result['tweet_count'].sum()
    twt_90_total = tweets_90days['tweet_count'].sum()
    mean_tweet = round(tweets_90days['tweet_count'].mean(),1)
    context = {'twt_today':twt_today,'max_tweet':max_tweet,'total_tweet':twt_90_total,'No_tweet_14_avg':No_tweet_14_avg,'mean_tweet':mean_tweet,'d':zip(tt_created[:20],tmp[:20],twt_id[:20],twt_likes[:20],twt_retweet[:20]),'z':zip(t5_tweet,t5_send,t5_like,t5_retweet,t5_id),'kk':kk,'form':form,'profile_pic':profile_pic,'twt_followers':twt_followers[0],'twt_friends':twt_friends[0],'twt_name':twt_name,'twt_desc':twt_desc}
    return render(request, 'base/date14d.html',context)#


def date7d(request):

    if request.method == 'POST':
        form = TwitterForm(request.POST)
        if form.is_valid():
                form.save()

    form = TwitterForm()
    
    twitters = Twitter_Model.objects.all()
    twttt_created  = []
    for tk in twitters:
        t1 = tk
    
        twttt_created.append(tk)
    kk =(twttt_created[-1])
    #print(kk)

    consumer_key = 'WURYy5DNwdoKNuq36C2ME9MG5'
    consumer_secret = 'GAFW5dHB7VJxtzefeZgi3YuSRIOBSILAIjzSZZqLYfaS2yFXJN'
    access_token_key = '1145240407229587458-WiSLolua6cpjAyeyPqAY7pfEkZegEv'
    access_token_secret = 'GA0h27EWeaucrnkSzRsYNqe6FGPxVHweAeS6kTzG3weFi'
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

    # Access to user's access key and access secret 
    auth.set_access_token(access_token_key, access_token_secret) 

    # Calling api 
    api = tweepy.API(auth)

    # 200 tweets to be extracted 
    number_of_tweets=200
    user = api.get_user(screen_name=kk)
    twt_followers = []
    twt_friends = []

    #info
    followers = user.followers_count
    friends = user.friends_count
    twt_name = user.name 
    twt_desc = user.description
    twt_followers.append(followers)
    twt_friends.append(friends)
    profile_pic = user.profile_image_url

    #print(tweets)
    # Empty Array 
    tmp=[]
    twt_created = []
    tt_created = []
    twt_id = []
    twt_likes = []
    twt_retweet = []
    count = []
    if user.protected ==False:
        name = kk
    else:
        name = 'Twitter'  

    tweets = api.user_timeline(screen_name=name, count = 999 ,include_rts = False,exclude_replies=False)


    for x in tweets:
        j = x.text
        j = j + ''.join(c for c in j if c in emoji.UNICODE_EMOJI)
        c = len(x.text)
        if c > 1:
            c =1 
        else:
            c = 0
        twt_created_1 = (x.created_at).strftime("%d %m %Y")
        twt_created_2 = (x.created_at).strftime("%d %b %Y")
        twt_id_1 = x.id
        twt_likes_1 = x.favorite_count
        twt_retweet_1 =x.retweet_count
        tt_created.append(twt_created_2)
        count.append(c)
        tmp.append(j)
        twt_created.append(twt_created_1)
        twt_id.append(twt_id_1)
        twt_likes.append(twt_likes_1)
        twt_retweet.append(twt_retweet_1)

        #result1 = {'d':zip(twt_created,tmp,twt_id,twt_likes,twt_retweet),'kk':kk,'form':form,'profile_pic':profile_pic,'twt_followers':twt_followers[0],'twt_friends':twt_friends[0],'twt_name':twt_name,'twt_desc':twt_desc}
    #return render(request, 'base/home.html',result1)
    df = pd.DataFrame({'tweet':tmp,
            'tweet_count':(count),
            'tweet_send':twt_created,
            'twt_likes':twt_likes,
            'twt_retweet':twt_retweet,
            'twt_id':twt_id})
    
    top5 = df.sort_values(by='twt_likes', ascending=False,)[:5]
    t5_tweet = top5['tweet'].to_list()
    t5_send = top5['tweet_send'].to_list()
    t5_like = top5['twt_likes'].to_list()
    t5_retweet = top5['twt_retweet'].to_list()
    t5_id = top5['twt_id'].to_list()

    df['tweet_send'] = pd.to_datetime(df['tweet_send'],format='%d %m %Y')
    df = df.drop_duplicates()
    new_data = pd.pivot_table(index='tweet_send',values='tweet_count',data=df,aggfunc='sum')
    new_data = new_data.reset_index()
    result = new_data.sort_values(('tweet_send'), ascending=False)
    result['twt_send'] = result['tweet_send'].dt.strftime("%d %b")

# Today = pd.to_datetime('today',format='%Y-%m-%d')#.strftime("%Y-%m-%d")
    Today = datetime.utcnow().replace(minute=0, hour=0, second=0, microsecond=0)
    last_90days = start_date = Today - timedelta(days=90)

    last_14days = start_date = Today - timedelta(days=14)
    Yesterday = start_date = Today - timedelta(days=1)
    tweets_90days = df[(df['tweet_send']>(last_90days))]

    tweets_14days = result[(result['tweet_send']>(last_14days))]
    No_tweet_14_sum = tweets_14days['tweet_count'].sum()
    No_tweet_14_avg = round(tweets_14days['tweet_count'].mean(),0)
    try:
        tweet_today = result[(result['tweet_send']>Yesterday)]
    except:
        tweet_today = None
    twt_today = tweet_today['tweet_count'].sum()
    max_tweet = tweets_90days['tweet_count'].max()
    total_tweet = result['tweet_count'].sum()
    twt_90_total = tweets_90days['tweet_count'].sum()
    mean_tweet = round(tweets_90days['tweet_count'].mean(),1)
    context = {'twt_today':twt_today,'max_tweet':max_tweet,'total_tweet':twt_90_total,'No_tweet_14_avg':No_tweet_14_avg,'mean_tweet':mean_tweet,'d':zip(tt_created[:20],tmp[:20],twt_id[:20],twt_likes[:20],twt_retweet[:20]),'z':zip(t5_tweet,t5_send,t5_like,t5_retweet,t5_id),'kk':kk,'form':form,'profile_pic':profile_pic,'twt_followers':twt_followers[0],'twt_friends':twt_friends[0],'twt_name':twt_name,'twt_desc':twt_desc}
    return render(request, 'base/date7d.html',context)#


def get_data30(request):

    if request.method == 'POST':
        form = TwitterForm(request.POST)
        if form.is_valid():
                form.save()
    form = TwitterForm()
    
    twitters = Twitter_Model.objects.all()
    twttt_created  = []
    for tk in twitters:
        t1 = tk
    
        twttt_created.append(tk)
    kk =(twttt_created[-1])
    #print(kk)

    consumer_key = 'WURYy5DNwdoKNuq36C2ME9MG5'
    consumer_secret = 'GAFW5dHB7VJxtzefeZgi3YuSRIOBSILAIjzSZZqLYfaS2yFXJN'
    access_token_key = '1145240407229587458-WiSLolua6cpjAyeyPqAY7pfEkZegEv'
    access_token_secret = 'GA0h27EWeaucrnkSzRsYNqe6FGPxVHweAeS6kTzG3weFi'
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

    # Access to user's access key and access secret 
    auth.set_access_token(access_token_key, access_token_secret) 

    # Calling api 
    api = tweepy.API(auth) 

    # 200 tweets to be extracted 
    number_of_tweets=200
    user = api.get_user(screen_name=kk)

    twt_followers = []
    twt_friends = []

    #info
    followers = user.followers_count
    friends = user.friends_count
    twt_name = user.name 
    twt_desc = user.description
    twt_followers.append(followers)
    twt_friends.append(friends)
    profile_pic = user.profile_image_url

    #print(tweets)
    # Empty Array 
    tmp=[]
    twt_created = []
    twt_id = []
    twt_likes = []
    twt_retweet = []
    count = []

    if user.protected ==False:
        name = kk
    else:
        name = 'Twitter' 
    
    tweets = api.user_timeline(screen_name=name, count = 999, include_rts = False, retry_count=0)

    for x in tweets:
        j = x.text
        j = j + ''.join(c for c in j if c in emoji.UNICODE_EMOJI)
        c = len(x.text)
        if c > 1:
            c =1 
        else:
            c = 0
        twt_created_1 = ((x.created_at).strftime("%d %m %Y"))
        twt_id_1 = x.id
        twt_likes_1 = (x.favorite_count)
        twt_retweet_1 =x.retweet_count
        #twt_followers_1 = x.followers_count
        #twt_friends_1 = x.friends_count
        count.append(c)
        tmp.append(j)
        default_items =(tmp)
        #print(default_items)
        twt_created.append((twt_created_1))
        twt_created = (twt_created)#.sort(reverse=True)
        twt_id.append(twt_id_1)
        twt_likes.append(twt_likes_1)
        twt_retweet.append(twt_retweet_1)

    df = pd.DataFrame({'tweet':tmp,
                'tweet_count':(count),
                'tweet_send':twt_created})
    df['tweet_send'] = pd.to_datetime(df['tweet_send'],format='%d %m %Y')
    df = df.drop_duplicates()

    Today = datetime.utcnow().replace(minute=0, hour=0, second=0, microsecond=0)
    last_30days = start_date = Today - timedelta(days=30)
    Yesterday = start_date = Today - timedelta(days=1)
    #print(last_90days)
    tweets_30days = df[(df['tweet_send']>(last_30days))]
    #tweets_90days.to_csv('90.csv')
    new_data = pd.pivot_table(index='tweet_send',values='tweet_count',data=tweets_30days,aggfunc='sum')
    new_data = new_data.reset_index()
    result = new_data.sort_values(('tweet_send'), ascending=False)
    result['twt_send'] = result['tweet_send'].dt.strftime("%d %b")

    total = result['tweet_count'].to_list()
    send = result['twt_send'].to_list()
    #result.to_csv('result.csv')
    #send = sorted(send,key=lambda x: datetime.datetime.strptime(x, '%d %b'),reverse=True)

    data = {
    "labels": send,
    "default": total
    }
    return JsonResponse(data)


def get_data14(request):

    if request.method == 'POST':
        form = TwitterForm(request.POST)
        if form.is_valid():
                form.save()
    form = TwitterForm()
    
    twitters = Twitter_Model.objects.all()
    twttt_created  = []
    for tk in twitters:
        t1 = tk
    
        twttt_created.append(tk)
    kk =(twttt_created[-1])
    #print(kk)

    consumer_key = 'WURYy5DNwdoKNuq36C2ME9MG5'
    consumer_secret = 'GAFW5dHB7VJxtzefeZgi3YuSRIOBSILAIjzSZZqLYfaS2yFXJN'
    access_token_key = '1145240407229587458-WiSLolua6cpjAyeyPqAY7pfEkZegEv'
    access_token_secret = 'GA0h27EWeaucrnkSzRsYNqe6FGPxVHweAeS6kTzG3weFi'
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

    # Access to user's access key and access secret 
    auth.set_access_token(access_token_key, access_token_secret) 

    # Calling api 
    api = tweepy.API(auth) 

    # 200 tweets to be extracted 
    number_of_tweets=200
    user = api.get_user(screen_name=kk)

    twt_followers = []
    twt_friends = []

    #info
    followers = user.followers_count
    friends = user.friends_count
    twt_name = user.name 
    twt_desc = user.description
    twt_followers.append(followers)
    twt_friends.append(friends)
    profile_pic = user.profile_image_url

    #print(tweets)
    # Empty Array 
    tmp=[]
    twt_created = []
    twt_id = []
    twt_likes = []
    twt_retweet = []
    count = []

    if user.protected ==False:
        name = kk
    else:
        name = 'Twitter' 
    
    tweets = api.user_timeline(screen_name=name, count = 999, include_rts = False, retry_count=0)

    for x in tweets:
        j = x.text
        j = j + ''.join(c for c in j if c in emoji.UNICODE_EMOJI)
        c = len(x.text)
        if c > 1:
            c =1 
        else:
            c = 0
        twt_created_1 = ((x.created_at).strftime("%d %m %Y"))
        twt_id_1 = x.id
        twt_likes_1 = (x.favorite_count)
        twt_retweet_1 =x.retweet_count
        #twt_followers_1 = x.followers_count
        #twt_friends_1 = x.friends_count
        count.append(c)
        tmp.append(j)
        default_items =(tmp)
        #print(default_items)
        twt_created.append((twt_created_1))
        twt_created = (twt_created)#.sort(reverse=True)
        twt_id.append(twt_id_1)
        twt_likes.append(twt_likes_1)
        twt_retweet.append(twt_retweet_1)

    df = pd.DataFrame({'tweet':tmp,
                'tweet_count':(count),
                'tweet_send':twt_created})
    df['tweet_send'] = pd.to_datetime(df['tweet_send'],format='%d %m %Y')
    df = df.drop_duplicates()

    Today = datetime.utcnow().replace(minute=0, hour=0, second=0, microsecond=0)
    last_14days = start_date = Today - timedelta(days=14)
    Yesterday = start_date = Today - timedelta(days=1)
    #print(last_90days)
    tweets_14days = df[(df['tweet_send']>(last_14days))]
    #tweets_90days.to_csv('90.csv')
    new_data = pd.pivot_table(index='tweet_send',values='tweet_count',data=tweets_14days,aggfunc='sum')
    new_data = new_data.reset_index()
    result = new_data.sort_values(('tweet_send'), ascending=False)
    result['twt_send'] = result['tweet_send'].dt.strftime("%d %b")

    total = result['tweet_count'].to_list()
    send = result['twt_send'].to_list()
    #result.to_csv('result.csv')
    #send = sorted(send,key=lambda x: datetime.datetime.strptime(x, '%d %b'),reverse=True)

    data = {
    "labels": send,
    "default": total
    }
    return JsonResponse(data)

def get_data7(request):

    if request.method == 'POST':
        form = TwitterForm(request.POST)
        if form.is_valid():
                form.save()
    form = TwitterForm()
    
    twitters = Twitter_Model.objects.all()
    twttt_created  = []
    for tk in twitters:
        t1 = tk
    
        twttt_created.append(tk)
    kk =(twttt_created[-1])
    #print(kk)

    consumer_key = 'WURYy5DNwdoKNuq36C2ME9MG5'
    consumer_secret = 'GAFW5dHB7VJxtzefeZgi3YuSRIOBSILAIjzSZZqLYfaS2yFXJN'
    access_token_key = '1145240407229587458-WiSLolua6cpjAyeyPqAY7pfEkZegEv'
    access_token_secret = 'GA0h27EWeaucrnkSzRsYNqe6FGPxVHweAeS6kTzG3weFi'
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

    # Access to user's access key and access secret 
    auth.set_access_token(access_token_key, access_token_secret) 

    # Calling api 
    api = tweepy.API(auth) 

    # 200 tweets to be extracted 
    number_of_tweets=200
    user = api.get_user(screen_name=kk)

    twt_followers = []
    twt_friends = []

    #info
    followers = user.followers_count
    friends = user.friends_count
    twt_name = user.name 
    twt_desc = user.description
    twt_followers.append(followers)
    twt_friends.append(friends)
    profile_pic = user.profile_image_url

    #print(tweets)
    # Empty Array 
    tmp=[]
    twt_created = []
    twt_id = []
    twt_likes = []
    twt_retweet = []
    count = []

    if user.protected ==False:
        name = kk
    else:
        name = 'Twitter' 
    
    tweets = api.user_timeline(screen_name=name, count = 999, include_rts = False, retry_count=0)

    for x in tweets:
        j = x.text
        j = j + ''.join(c for c in j if c in emoji.UNICODE_EMOJI)
        c = len(x.text)
        if c > 1:
            c =1 
        else:
            c = 0
        twt_created_1 = ((x.created_at).strftime("%d %m %Y"))
        twt_id_1 = x.id
        twt_likes_1 = (x.favorite_count)
        twt_retweet_1 =x.retweet_count
        #twt_followers_1 = x.followers_count
        #twt_friends_1 = x.friends_count
        count.append(c)
        tmp.append(j)
        default_items =(tmp)
        #print(default_items)
        twt_created.append((twt_created_1))
        twt_created = (twt_created)#.sort(reverse=True)
        twt_id.append(twt_id_1)
        twt_likes.append(twt_likes_1)
        twt_retweet.append(twt_retweet_1)

    df = pd.DataFrame({'tweet':tmp,
                'tweet_count':(count),
                'tweet_send':twt_created})
    df['tweet_send'] = pd.to_datetime(df['tweet_send'],format='%d %m %Y')
    df = df.drop_duplicates()

    Today = datetime.utcnow().replace(minute=0, hour=0, second=0, microsecond=0)
    last_7days = start_date = Today - timedelta(days=7)
    Yesterday = start_date = Today - timedelta(days=1)
    #print(last_90days)
    tweets_7days = df[(df['tweet_send']>(last_7days))]
    #tweets_90days.to_csv('90.csv')
    new_data = pd.pivot_table(index='tweet_send',values='tweet_count',data=tweets_7days,aggfunc='sum')
    new_data = new_data.reset_index()
    result = new_data.sort_values(('tweet_send'), ascending=False)
    result['twt_send'] = result['tweet_send'].dt.strftime("%d %b")

    total = result['tweet_count'].to_list()
    send = result['twt_send'].to_list()
    #result.to_csv('result.csv')
    #send = sorted(send,key=lambda x: datetime.datetime.strptime(x, '%d %b'),reverse=True)

    data = {
    "labels": send,
    "default": total
    }
    return JsonResponse(data)

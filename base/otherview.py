from django.shortcuts import render,redirect
import tweepy
import emoji
import iso8601
from .forms import TwitterForm
from .models import Twitter_Model

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model

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
    twt_id = []
    twt_likes = []
    twt_retweet = []

    if user.protected ==False:
        name = kk
    else:
        name = 'Twitter'  

    tweets = api.user_timeline(screen_name=name)


    for x in tweets:
        j = x.text
        j = j + ''.join(c for c in j if c in emoji.UNICODE_EMOJI)
        twt_created_1 = (x.created_at).strftime("%d %b %Y")
        twt_id_1 = x.id
        twt_likes_1 = x.favorite_count
        twt_retweet_1 =x.retweet_count
        
        tmp.append(j)
        twt_created.append(twt_created_1)
        twt_id.append(twt_id_1)
        twt_likes.append(twt_likes_1)
        twt_retweet.append(twt_retweet_1)


        result = {'d':zip(twt_created,tmp,twt_id,twt_likes,twt_retweet),'kk':kk,'form':form,'profile_pic':profile_pic,'twt_followers':twt_followers[0],'twt_friends':twt_friends[0],'twt_name':twt_name,'twt_desc':twt_desc}

    return render(request, 'base/home.html',result)#
 

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
    
    tweets = api.user_timeline(screen_name=name)

    for x in tweets:
        j = x.text
        j = j + ''.join(c for c in j if c in emoji.UNICODE_EMOJI)
        c = len(x.text)
        if c > 1:
            c =1 
        else:
            c = 0
        twt_created_1 = ((x.created_at).strftime("%d %b"))
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

        data = {
        "labels": twt_created,
        "default": twt_likes,
        "retweet":twt_retweet,
        'tweet_count':count
        }
    return JsonResponse(data)














# class ChartData(APIView):
#     authentication_classes = []
#     permission_classes = []
    # def get_data(request):
    #     data = {'sales':100,
    #     'customer':218}
    #     return JsonResponse(data) #Rrender(request, 'base/home.html',data)

    # def get(request):
    #     qs_count = User.objects.all().count()
    #     labels = ["Users","Blue","Yellow","Green","Purple","Orange"]
    #     default_items = [qs_count, 12, 15, 15, 22, 23, 20]
    #     data = {
    #         "labels": labels,
    #         "default": default_items,
    #     }
    #     return JsonResponse(data)

# class LineChartJSONView(BaseLineChartView):
#     def home(request):

#         if request.method == 'POST':
#             form = TwitterForm(request.POST)
#             if form.is_valid():
#                     form.save()

#         form = TwitterForm()
        
#         twitters = Twitter_Model.objects.all()
#         twttt_created  = []
#         for tk in twitters:
#             t1 = tk
        
#             twttt_created.append(tk)
#         kk =(twttt_created[-1])
#         #print(kk)

#         consumer_key = 'WURYy5DNwdoKNuq36C2ME9MG5'
#         consumer_secret = 'GAFW5dHB7VJxtzefeZgi3YuSRIOBSILAIjzSZZqLYfaS2yFXJN'
#         access_token_key = '1145240407229587458-WiSLolua6cpjAyeyPqAY7pfEkZegEv'
#         access_token_secret = 'GA0h27EWeaucrnkSzRsYNqe6FGPxVHweAeS6kTzG3weFi'
#         # Authorization to consumer key and consumer secret 
#         auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

#         # Access to user's access key and access secret 
#         auth.set_access_token(access_token_key, access_token_secret) 

#         # Calling api 
#         api = tweepy.API(auth) 

#         # 200 tweets to be extracted 
#         number_of_tweets=200
#         tweets = api.user_timeline(screen_name=kk) 
#         #print(tweets)
#         # Empty Array 
#         tmp=[]
#         twt_created = []
#         twt_id = []
#         twt_likes = []
#         twt_retweet = []
#         twt_followers = []
#         twt_friends = []

#         # create array of tweet information: username,  
#         # tweet id, date/time, text
#         #tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created  


#         user = api.get_user(kk)

#         followers = user.followers_count
#         friends = user.friends_count
#         twt_name = user.name 
#         twt_desc = user.description
#         twt_followers.append(followers)
#         twt_friends.append(friends)
#         profile_pic = user.profile_image_url
        
#     #main = {'z': zip(twt_followers,twt_friends,profile_pic)}
#     #print(twt_followers[0])

#         for x in tweets:
#             j = x.text
#             j = j + ''.join(c for c in j if c in emoji.UNICODE_EMOJI)
#             twt_created_1 = (x.created_at).strftime('%d/%m/%Y %H:%M:%S')
#             twt_id_1 = x.id
#             twt_likes_1 = x.favorite_count
#             twt_retweet_1 =x.retweet_count
#             #twt_followers_1 = x.followers_count
#             #twt_friends_1 = x.friends_count
            
#             tmp.append(j)
#             twt_created.append(twt_created_1)
#             twt_id.append(twt_id_1)
#             twt_likes.append(twt_likes_1)
#             twt_retweet.append(twt_retweet_1)
     
#         def get_labels(self):
#             return self.twt_created
#         print(get_labels())

#         def get_providers(self):
#             """Return names of datasets."""
#             return ["Central", "Eastside", "Westside"]

#         def get_data(self):
#             """Return 3 datasets to plot."""

#             return [[75, 44, 92, 11, 44, 95, 35],
#                     [41, 92, 18, 3, 73, 87, 92],
#                     [87, 21, 94, 3, 90, 13, 65]]


# line_chart = TemplateView.as_view(template_name='base/home.html')
# line_chart_json = LineChartJSONView.as_view()
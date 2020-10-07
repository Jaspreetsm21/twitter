def like(request):
    counter = 0
    keyword = request.POST['search']
    api = get_api(request)
    # Getting the user
    user = api.me()
    print(user.screen_name)
    # Adding keyword to search the tweets for
    search = keyword
    # Specifying the tweets limit
    numberOfTweets = 5
    # Fetching the tweets and liking them
    for tweet in tweepy.Cursor(api.search,    search).items(numberOfTweets):
        try:
            tweet.favorite()
            print('Tweet Liked!')
            counter = counter + 1
            time.sleep(10)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break
    return render(request, "liked.html", {'counter': counter, 'keyword': search})
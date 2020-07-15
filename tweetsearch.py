import tweepy
import csv
import json

class TweetSearch(object):

    def __init__(self):
        with open('twitter_credentials.json') as cred_data:
            self.keys = json.load(cred_data)

        self.hashtag = 'coronavirus'
        self.maximum_number_of_tweets_to_be_extracted = 10
        self.scrape_tweets_by_hashtag()


    def scrape_tweets_by_hashtag(self):
        auth = tweepy.OAuthHandler(self.keys['CONSUMER_KEY'], self.keys['CONSUMER_SECRET'])
        api = tweepy.API(auth)

        with open('tweets_test' + self.hashtag + '.csv', 'w', newline='', encoding="utf8") as out_file:
            writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for tweet in tweepy.Cursor(api.search, q='#' + self.hashtag, tweet_mode='extended', rpp=100).items(self.maximum_number_of_tweets_to_be_extracted):
                    try:
                        #writer.writerow([tweet.full_text.replace('\n', ' ').replace('\r', '').encode('ascii',errors='ignore')])
                        writer.writerow([tweet.retweeted_status.full_text.replace('\n', ' ').replace('\r', '').encode('ascii',errors='replace').decode('ascii') if hasattr(tweet, 'retweeted_status') else tweet.full_text.replace('\n', ' ').replace('\r', '').encode('ascii',errors='replace'), tweet.user.followers_count])
                    except UnicodeEncodeError:
                        continue
                    except:
                        print('somethings gone very wrong: ' + tweet.full_text)

        print('Extracted ' + str(self.maximum_number_of_tweets_to_be_extracted) + ' tweets with hashtag #' + self.hashtag)

# maybe use pandas and jupyter to do the coding

app = TweetSearch()
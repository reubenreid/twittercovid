from TwitterAPI import TwitterAPI
import csv
import json


class PremiumTweetSearch(object):

    def __init__(self):
        with open('twitter_credentials.json') as cred_data:
            self.keys = json.load(cred_data)

        self.maximum_number_of_tweets_to_be_extracted = 10
        self.SEARCH_TERM = '(#coronavirus OR #covid19) lang:en'


    def scrape_tweets_by_hashtag(self):
        api = TwitterAPI(self.keys['CONSUMER_KEY'], self.keys['CONSUMER_SECRET'], self.keys['ACCESS_KEY'], self.keys['ACCESS_SECRET'])
        with open('tweets_march.csv', 'a', newline='') as out_file:
            writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            response = api.request('tweets/search/fullarchive/:dev', {'query': self.SEARCH_TERM, 'fromDate': 202006250000, 'toDate': 202006280000})
            for tweet in response:
                try:
                    if ('retweeted_status' in tweet and 'extended_tweet' in tweet['retweeted_status']):
                        writer.writerow([tweet['retweeted_status']['extended_tweet']['full_text'].replace('\n', ' ').replace('\r', '').encode('ascii', errors='replace'),
                                     tweet['user']['followers_count'],
                                     tweet['retweet_count'], tweet['user']['screen_name'], tweet['created_at'],
                                     tweet['favorite_count'],
                                     list(map(lambda x: x['text'], tweet['entities']['hashtags']))])

                    elif ('extended_tweet' in tweet):
                        writer.writerow([tweet['extended_tweet']['full_text'].replace('\n',' ').replace('\r', '').encode('ascii', errors='replace'),
                                         tweet['user']['followers_count'],
                                         tweet['retweet_count'], tweet['user']['screen_name'], tweet['created_at'],
                                         tweet['favorite_count'],
                                         list(map(lambda x: x['text'], tweet['entities']['hashtags']))])
                    else:
                        writer.writerow([tweet['text'].replace('\n',' ').replace('\r', '').encode('ascii', errors='replace'),
                                         tweet['user']['followers_count'],
                                         tweet['retweet_count'], tweet['user']['screen_name'], tweet['created_at'],
                                         tweet['favorite_count'],
                                         list(map(lambda x: x['text'], tweet['entities']['hashtags']))])
                except UnicodeEncodeError:
                    continue
                except Exception as e:
                    print('somethings gone very wrong: ' + str(e))




app = PremiumTweetSearch()
app.scrape_tweets_by_hashtag()

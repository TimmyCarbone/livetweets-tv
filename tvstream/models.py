import random
from datetime import datetime, timedelta
from django.db import models

from app import APP_KEY, APP_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, twitter


class ActiveTweetQueues():
  instances = set()

  def add_queue(self, queue):
    self.instances.add(queue)

  def get_queue(self, id, keyword):
    for queue in self.instances:
      if queue.id == id and queue.keyword == keyword: 
        return queue
    return None

  def purge(self):
    purge = set()
    for queue in self.instances:
      if (datetime.now() - queue.pulled_at) > timedelta(seconds=60): 
        purge.add(queue)

    for queue in purge:
      self.instances.remove(queue)

  def __repr__(self):
    res = []
    for i in self.instances: res.append(str(i.id) + ' - ' + i.keyword)
    return ','.join(res)


class TweetQueue():
  tweets_id_queue = set()
  tweets_dict = {}
  previous_tweets_ids = []
  keyword = None
  pulled_at = datetime.now()
  id = 0

  def __init__(self, keyword):
    self.id = random.randint(1, 999999)
    self.keyword = keyword

  def __repr__(self):
      return "TweetQueue(%d, %s)" % (self.id, self.keyword)

  def __eq__(self, other):
      if isinstance(other, Item):
          return ((self.id == other.id) and (self.keyword == other.keyword))
      else:
          return False

  def __ne__(self, other):
      return (not self.__eq__(other))

  def __hash__(self):
      return hash(self.__repr__())

  def refresh(self, refresh_by=5):
    self.last_tweets = twitter.search(q=self.keyword, count=refresh_by)

    for lt in self.last_tweets['statuses']:
      if lt['id'] not in self.tweets_id_queue.union(set(self.previous_tweets_ids)):
        self.tweets_id_queue.add(lt['id'])
        self.tweets_dict.update({lt['id']: lt})

    self.previous_tweets_ids = [t['id'] for t in self.last_tweets['statuses']]
    self.tweets_dict[self.previous_tweets_ids[0]] = self.last_tweets['statuses'][0]

  def pull(self):
    if len(self.tweets_id_queue) > 0:
      new_tweet = self.tweets_dict[min(self.tweets_id_queue)]
      self.tweets_id_queue.remove(new_tweet['id'])
      del self.tweets_dict[new_tweet['id']]
    else:
      new_tweet = self.tweets_dict[self.previous_tweets_ids[0]]
    self.pulled_at = datetime.now()
    return new_tweet

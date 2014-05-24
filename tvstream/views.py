import json, time
from django.shortcuts import render

from app.lib.util import cap

from tvstream.models import TweetQueue, ActiveTweetQueues

active_queues = ActiveTweetQueues()

def home(request):
  active_queues.purge()
  return render(request, 'tvstream/tpl/home.html');

def stream(request, keyword):
  if request.method == "POST":
    queue_id = int(request.POST['queue_id'])
    queue = active_queues.get_queue(queue_id, keyword)
  else:
    queue = TweetQueue(keyword)
    active_queues.add_queue(queue)

  queue.refresh()
  tweet = queue.pull()

  # Treatments
  tweet['user']['name'] = cap(tweet['user']['name'], 22)
  tweet['created_at'] = time.strptime(tweet['created_at'], '%a %b %y %H:%M:%S +0000 %Y')
  tweet['created_at'] = time.strftime('%H:%M - %d %b %Y', tweet['created_at'])
  for word in tweet['text'].split(' '):
    if word.startswith('@') or word.startswith('#'):
      word = word.replace('!','').replace('?', '').replace(':','')
      tweet['text'] = tweet['text'].replace(word, '<span class="hashtag">'+ word + '</span>')

  return render(request, 'tvstream/tpl/stream.html', {
    'queue_id': queue.id,
    'keyword': keyword,
    'tw': tweet,
    'user_image': tweet['user']['profile_image_url_https'].replace('_normal', '')
    });

import os
import sys
import urllib2
import re
import xml.etree.ElementTree as ElementTree
from datetime import datetime
import subprocess

class SubscriptionWriter:

    file_name = os.path.dirname(os.path.realpath(__file__)) + "/subscriptions.txt"

    def get_file(self):
        return open(self.file_name, 'a')

    def add_subscription(self):
        youtubeReader = YoutubeReader()
        youtubeReader.download_user_html()
        name = sys.argv[3]
        url = youtubeReader.get_feed_url()
        f = self.get_file()
        f.writelines([name + ',' + url + '\n'])
        f.close()


class YoutubeReader:

    user_raw_html = None

    def download_user_html(self):
        self.user_raw_html = urllib2.urlopen(sys.argv[2]).read()

    def get_youtube_user(self):
        pattern = r"https://www\.youtube\.com/user/\w*"
        user_url = re.search(pattern, self.user_raw_html).group()
        return user_url[29:]

    def get_feed_url(self):
        print "Finding feed URL"
        patern = r"https://www\.youtube\.com/feeds/videos\.xml\?channel_id=\w*"
        match = re.search(patern, self.user_raw_html)
        if match:
            print "Feed URL found"
            return re.search(patern, self.user_raw_html).group()
        else:
            print "Feed URL not found, trying to construct from channel URL"
            return "https://www.youtube.com/feeds/videos.xml?channel_id=" + sys.argv[2][sys.argv[2].index("channel/")+8:]


    def get_channel_videos(self, channel_url, videos):
        print "getting " + channel_url
        tree = ElementTree.parse(urllib2.urlopen(channel_url))
        for video in tree.getroot().findall('{http://www.w3.org/2005/Atom}entry'):
            videos.add(self.get_video_details(video))

    def get_video_details(self, video_details):
        video = Video()
        video.title = video_details[3].text
        video.set_publised_date(video_details[6].text)
        video.link = video_details[4].get('href')
        video.author = video_details[5][0].text
        return video




class SubscriptionController:

    file_name = os.path.dirname(os.path.realpath(__file__)) + "/subscriptions.txt"

    def list_subscriptions(self):
        outputWriter = OutputWriter()
        with open(self.file_name) as f:
            for line in f:
                outputWriter.print_subscription(line)

    def add(self):
        subscriptionWriter = SubscriptionWriter()
        subscriptionWriter.add_subscription()

    def list(self):
        youtubeReader = YoutubeReader()
        videos = Videos()
        outputWriter = OutputWriter()
        with open(self.file_name) as f:
            for line in f:
                if len(sys.argv) == 2 or line[:line.index(',')] == sys.argv[2]:
                    youtubeReader.get_channel_videos(line[line.index(',')+1:], videos)
        for index, video in enumerate(videos.get_videos()):
            outputWriter.print_video_listing(index, video)
        selected = []
        s = raw_input("Select video/s to download \n  (q) to quit (d) to download\nSelection: ")


        while re.match(r"\d", s):
            selected.append(videos.get_videos()[int(s)-1].link)
            s = raw_input("Selection: ")
        if s == 'd':
            print "Downloading..."
            command = ["youtube-dl", "-f", "140"]
            for v in selected:
                command.append(v)
            subprocess.call(command)
        subprocess.call(["clear"])

    def help(self):
        print "list_subscriptions: List your subscriptions"
        print "               add: Add to your subscriptions"
        print "                    E.g. https://www.youtube.com/user/[username]"
        print "              list: List subsciptions with prompts to download"


class OutputWriter:

    def print_video_listing(self, index, video):
        index = str(index + 1)
        space = ""
        if len(index) == 1:
            space = "  "
        elif len(index) == 2:
            space = " "
        print "(" + index + ") " + space + video.title
        print "      " + video.author
        print "      " + video.published.strftime("%a %d %b") + "\n"

    def print_subscription(self, line):
        comma_index = line.index(",")
        print "     Channel: " + line[:comma_index]
        print "Channel feed: " + line[comma_index+1:]



class Video:
    stars = None
    title = None
    published = None
    description = None
    link = None
    author = None

    def set_publised_date(self, date):
        date_string = date[:date.index('+')]
        self.published = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")


    def __cmp__(self, other):
        if hasattr(other, 'published'):
            return cmp(self.published, other.published)

class Videos:
    videos = []

    def add(self, video):
        self.videos.append(video)

    def get_videos(self):
        self.videos.sort()
        return self.videos








class InputReader:

    operation = None

    def __init__(self):
        subscriptionController = SubscriptionController()
        self.operation = getattr(subscriptionController, sys.argv[1])

print os.path.dirname(os.path.realpath(__file__))

inputReader = InputReader()
inputReader.operation()

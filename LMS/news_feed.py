import feedparser     

class NewsFeed:
    def getNews(self):
        rss_url = "https://www.thehindubusinessline.com/news/national/feeder/default.rss"
        parser = feedparser.parse(rss_url)
        return parser.entries



        #https://www.thehindu.com/news/feeder/default.rss
        #https://www.jagranjosh.com/rss/josh/current_affairs.xml
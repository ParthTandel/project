import feedparser
import html2text
from pprint import pprint
from bs4 import BeautifulSoup
from newspaper import Article
from pymongo import MongoClient
client = MongoClient()
db = client.clusters
# print count

def parseRSS( rss_url ):
    return feedparser.parse(rss_url)

def getHeadlines( rss_url , type):
    headlines = []
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.bypass_tables = False
    feed = parseRSS(rss_url)
    count = 0
    count = db.articles.find({}).count();

    for newsitem in feed['items']:
        try:
            # print "*************************DictStart**************************"
            url = newsitem['link']
            soup = BeautifulSoup(newsitem['summary']);
            article = Article(url)
            article.download()
            article.parse()


            soupText = BeautifulSoup(article.text);

            mongo_dict = {
                "title"     :   newsitem['title'],
                "link"      :   newsitem['link'],
                "summary"   :   soup.get_text(),
                "text"      :   soupText.get_text(),
                "type"      :   type
            }


            if(mongo_dict["summary"] != '' or mongo_dict["text"] != ''):
                # print soupText.get_text();
                db.articles.insert_one(mongo_dict);
                count = count + 1;
                print str(count) + " db saved"
                # pprint(str(article.text))

            # print "**************************DictEnd***************************"
        except Exception, e:
            # print "db not saved"
            print str(e)
    return headlines

allheadlines = []

newsurls = {
    # 'reuters'                       : "http://feeds.reuters.com/reuters/entertainment",
    # 'usatoday1'                     : "http://rssfeeds.usatoday.com/usatoday-LifeTopStories",
    # 'usatoday2'                     : "http://rssfeeds.usatoday.com/UsatodaycomMovies-TopStories",
    # "usatoday3"                     : "http://rssfeeds.usatoday.com/UsatodaycomMusic-TopStories",
    # "usatoday4"                     : "http://rssfeeds.usatoday.com/UsatodaycomTelevision-TopStories",
    # "usstoday5"                     : "http://rssfeeds.usatoday.com/UsatodaycomBooks-TopStories",
    # "usstoday6"                     : "http://rssfeeds.usatoday.com/toppeople",
    # "edition"                       : "http://rss.cnn.com/rss/edition_entertainment.rss",
    # "feedburnertv"                  : "http://feeds.feedburner.com/thr/television",
    # "feedburnermusic"               : "http://feeds.feedburner.com/thr/music",
    # "feedburner"                    : "http://feeds.feedburner.com/thr/boxoffice",
    # "feedaccess"                    : "http://feeds.accesshollywood.com/AccessHollywood/LatestNews?_ga=1.217997726.900419521.1492103763",
    # "xmlrss"                        : "http://www.tmz.com/rss.xml",
    # "usstodaywtps"                  : "http://rssfeeds.usatoday.com/UsatodaycomWorld-TopStories",
    # "newsopi"                       : "http://rssfeeds.usatoday.com/News-Opinion",
    # "usnewsopinion"                 : "https://www.usnews.com/rss/opinion",
    # "wstimes"                       : "http://www.washingtontimes.com/rss/headlines/news/national/",
    # "wstimespoliticaltheratre"      : "http://www.washingtontimes.com/rss/headlines/news/political-theater/",
    # "politics"                      : "http://www.washingtontimes.com/rss/headlines/news/politics/",
    # "thehillsenate"                 : "http://thehill.com/taxonomy/term/1130/feed",
    # "wtimesusrussia"                : "http://www.washingtontimes.com/rss/headlines/news/us-russia-crosstalk/",
    # "politics"                      : "http://feeds.reuters.com/Reuters/PoliticsNews",
    # "nytimepolitics"                : "http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
    # "wprss"                         : "http://feeds.washingtonpost.com/rss/politics",
    # "feedfox"                       : "http://feeds.foxnews.com/foxnews/politics"
    # "hillsenate"                    : "http://thehill.com/taxonomy/term/1131/feed",
    # "hillhouse"                     : "http://thehill.com/taxonomy/term/1130/feed",
    # "feedburnerpolitics"            : "http://feeds.feedburner.com/realclearpolitics/qlMj",
    # "newsMaxPolitics"               : "http://nm.nmcdn.us/rss/Politics/1/",
    # "wpplypowerpost"                : "http://feeds.washingtonpost.com/rss/rss_powerpost",
    # "wpplyfactchecker"              : "http://feeds.washingtonpost.com/rss/rss_fact-checker",
    # "wpplyressthefix"               : "http://feeds.washingtonpost.com/rss/rss_the-fix",
    # "wppyrsselection"               : "http://feeds.washingtonpost.com/rss/rss_election-2012",
    # "wppmonnkeycage"                : "http://feeds.washingtonpost.com/rss/rss_monkey-cage",
    # "rsssportstop"                  : "http://rssfeeds.usatoday.com/UsatodaycomSports-TopStories",
    # "rssnfl"                        : "http://rssfeeds.usatoday.com/UsatodaycomNfl-TopStories",
    # "rsstop fantasy"                : "http://rssfeeds.usatoday.com/topfantasy",
    # "rsssnbatopstories"             : "http://rssfeeds.usatoday.com/UsatodaycomNba-TopStories",
    # "rsssoccer"                     : "http://rssfeeds.usatoday.com/UsatodaycomSoccer-TopStories",
    # "rssolympics"                   : "http://rssfeeds.usatoday.com/UsatodaycomOlympicsCoverage-TopStories",
    # "rsstennis"                     : "http://rssfeeds.usatoday.com/UsatodayTennis-TopStories",
    # "sportsillustratednfl"          : "https://www.si.com/rss/si_nfl.rss",
    # "sportsillustratednfotball"     : "https://www.si.com/rss/si_ncaaf.rss",
    # "sportsillustratedtopstories"   : "https://www.si.com/rss/si_mlb.rss",
    # "sportsillustratednba"          : "https://www.si.com/rss/si_nba.rss",
    # "sportsillustratedsoccer"       : "https://www.si.com/rss/si_soccer.rss",
    # "sportsillustratedtennis"       : "https://www.si.com/rss/si_tennis.rss",
    # "sportsillustratedfantasy"      : "https://www.si.com/rss/si_fantasy.rss"

}

for key,url in newsurls.items():
    allheadlines.extend(getHeadlines(url, "sports"))

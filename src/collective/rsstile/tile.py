import operator
from itertools import ifilter, islice

from zope.interface import implements
from zope.schema import List, URI, Int, ASCII
from zope.schema._compat import u
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets.rss import RSSFeed
from Products.CMFCore.utils import getToolByName

from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile

# Copy approach from RSS Portlet
FEED_DATA = {}

class IRSSTileData(IPersistentCoverTile):

    feeds = List(
        title=u("Feeds"),
        unique=True,
        value_type=URI(title=u('URL')),
    )
    
    items_to_show = Int(
        title=u("Number of items to show"),
    )
    
    max_per_feed = Int(
        title=u("Maximum number of items from a given feed"),
    )
    
    blacklist = List(
        title=u("Blacklisted words"),
        unique=True,
        value_type=ASCII(title=u('Word')),
        required=False,
        missing_value=[],
    )
    
    whitelist = List(
        title=u("Whitelisted words"),
        unique=True,
        value_type=ASCII(title=u('Word')),
        required=False,
        missing_value=[],
    )
    


class RSSTile(PersistentCoverTile):
    implements(IRSSTileData)
    is_editable = True
    is_configurable = True
    short_name = "RSS"
    
    index = ViewPageTemplateFile('tile.pt')
    
    def get_feeds(self):
        for feed in self.data['feeds']:
            feed_obj = FEED_DATA.get(feed, None)
            if feed_obj is None:
                feed_obj = FEED_DATA[feed] = RSSFeed(feed, 120)
            yield feed_obj
    
    def matches_whitelist(self, item):
        if not self.data["whitelist"]:
            # No whitelist implies a match
            return True
        
        text = item.get('title', ' ') + " " + item.get('summary', ' ')
        text = text.lower()
        for word in self.data['whitelist']:
            word = word.lower()
            if word in text:
                return True
        return False
    
    def blacklist_permits(self, item):
        if not self.data["blacklist"]:
            # No blacklist implies acceptability
            return True
        
        text = item.get('title', ' ') + " " + item.get('summary', ' ')
        text = text.lower()
        for word in self.data['blacklist']:
            word = word.lower()
            if word in text:
                return False
        return True
    
    def fmt(self, date):
        return "(%s)" % date.strftime("%Y-%m-%d")
    
    def get_items(self):
        items = []
        if self.data['feeds'] is None:
            # We're unconfigured!
            return []
        
        total_slots = self.data.get("items_to_show", 4)
        total_per_feed = self.data.get("max_per_feed", 1)
        
        
        transformer = getToolByName(self.context, 'portal_transforms', None)
        def convert(text):
            try:
                result = transformer.convertTo("text/plain", text.encode("utf-8", "ignore"), mimetype="text/html").getData().decode("utf-8")
            except:
                result = None
       
            if result is None:
                result = text
            if len(result) > 200:
                result = result[:195] + "..."
            return result
                                
        items = []
        for feed in self.get_feeds():
            feed.update()
            for item in islice(
                            ifilter(self.matches_whitelist, ifilter(self.blacklist_permits, feed.items)),
                            0, total_per_feed):
                item = {"title": item['title'], "summary": item["summary"], "updated": item["updated"], "url": item["url"]}
                print "FOUND " + item['title']
                if transformer is not None:
                    item['title'] = convert(item['title'])
                    item['summary'] = convert(item['summary'])
                items.append(item)
        
        items = sorted(items, key=operator.itemgetter('updated'), reverse=True)
        items = items[0:total_slots]
        print "RETURNING " + repr(items)
        print 
        print 
        print 
        print 
        return items
    

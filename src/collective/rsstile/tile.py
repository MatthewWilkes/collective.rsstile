from zope.interface import Interface
from zope.interface import implements
from zope.schema import List, URI, Int, Bytes
from zope.schema._compat import u
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile

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
        value_type=Bytes(title=u('Word')),
        required=False,
        missing_value=[],
    )
    
    whitelist = List(
        title=u("Whitelisted words"),
        unique=True,
        value_type=Bytes(title=u('Word')),
        required=False,
        missing_value=[],
    )
    


class RSSTile(PersistentCoverTile):
    implements(IRSSTileData)
    is_editable = True
    is_configurable = True
    short_name = "RSS"
    
    index = ViewPageTemplateFile('tile.pt')
        
    def get_items(self):
        items = []
        if self.data['feeds'] is None:
            # We're unconfigured!
            return []
        
        for feed in self.data['feeds']:
            items.append({'title': feed})
        
        return items
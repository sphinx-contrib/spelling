def setup(app):
    """
    see: http://sphinx.pocoo.org/ext/appapi.html
    this is the primary extension point for Sphinx
    """
    from sphinx.application import Sphinx
    if not isinstance(app, Sphinx): return
    app.add_config_value('feed_base_url', '', '')
    app.add_config_value('feed_description', '', '')
    app.add_config_value('feed_filename', 'rss.xml', 'html')
    
    app.connect('html-page-context', create_feed_item)
    app.connect('build-finished', emit_feed)
    app.connect('builder-inited', create_feed_container)
    
    #env.process_metadata deletes most of the docinfo, and dates
    #in particular.

def create_feed_container(app):
    import feedgenerator
    feed_dict = {
      'title': app.config.project,
      'link': app.config.feed_base_url,
      'description': app.config.feed_description
    }
    if app.config.language:
        feed_dict['language'] = app.config.language
    if app.config.copyright:
        feed_dict['feed_copyright'] = app.config.copyright
    feed = feedgenerator.Rss201rev2Feed(**feed_dict)
    app.builder.env.feed_feed = feed
    if not hasattr(app.builder.env, 'feed_items'):
        app.builder.env.feed_items = {}

def create_feed_item(app, pagename, templatename, ctx, doctree):
    """
    Here we have access to nice HTML fragments to use in, say, an RSS feed.
    """    
    import dateutil.parser
    date_parser = dateutil.parser.parser()
    env = app.builder.env
    metadata = app.builder.env.metadata.get(pagename, {})
    
    if 'date' not in metadata:
        return #don't index dateless articles
    try:
        pub_date = date_parser.parse(metadata['date'])
    except ValueError:
        #probably a nonsensical date
        #TODO - do some kind of smart sphinxey error logging
        return
        
    # title, link, description, author_email=None,
    #     author_name=None, author_link=None, pubdate=None, comments=None,
    #     unique_id=None, enclosure=None, categories=(), item_copyright=None,
    #     ttl=None,
    
    item = {
      'title': ctx.get('title'),
      'link': app.config.feed_base_url + '/' + ctx['current_page_name'] + ctx['file_suffix'],
      'description': ctx.get('body'),
      'pubdate': pub_date
    }
    if 'author' in metadata:
        item['author'] = metadata['author']
    env.feed_items[pagename] = item
    #Additionally, we might like to provide our templates with a way to link to the rss output file
    ctx['rss_link'] = app.config.feed_base_url + '/' + app.config.feed_filename
  
def emit_feed(app, exc):
    import os.path
    ordered_items = app.builder.env.feed_items.values()
    feed = app.builder.env.feed_feed
    ordered_items.sort(
      cmp=lambda x,y: cmp(x['pubdate'],y['pubdate']),
      reverse=True)
    for item in ordered_items:
        feed.add_item(**item)     
    outfilename = os.path.join(app.builder.outdir,
      app.config.feed_filename)
    fp = open(outfilename, 'w')
    feed.write(fp, 'utf-8')
    fp.close()
    


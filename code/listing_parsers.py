def active_listing_parser(url):
    import pandas as pd, lxml
    from datetime import datetime
    tables = pd.read_html(url)
    auction_stats_table = tables[0]
    new_dict = dict(zip(auction_stats_table[0], auction_stats_table[1]))
    new_dict['Time Left'] = new_dict['Time Left'].split('  ')[0]
    new_dict['Ends On'] = new_dict['Ends On'].split('  ')[0]
    new_dict['listing_scrape_ts'] = datetime.now()
    del(new_dict['Place Bid'], new_dict['Time Left'])
    view_stats = tables[1].loc[0,1]
    new_dict['Views'], new_dict['Watchers'] = view_stats.replace(',','').replace(' views','').replace(' watchers','').split(' | ')[:]
    return(new_dict)

def closed_listing_parser(url):
    import pandas as pd, lxml
    from datetime import datetime
    tables = pd.read_html(url)
    auction_stats_table = tables[0]
    new_dict = dict(zip(auction_stats_table[0], auction_stats_table[1]))
    try:
        new_dict['Winner'] = new_dict['Winning Bid'].split(' by ')[1]
        new_dict['Winning Bid'] = new_dict['Winning Bid'].split(' by ')[0]
        new_dict['listing_scrape_ts'] = datetime.now()
    except KeyError:
        pass
    view_stats = tables[1].loc[0,0]
    new_dict['Views'], new_dict['Watchers'] = view_stats.replace(',','').replace(' views','').replace(' watchers','').split(' | ')[:]
    return(new_dict)
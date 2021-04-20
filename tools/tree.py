import bs4, re, wikipedia
from collections import defaultdict


def get_pages(genre_names):
    """
    Input
      genre_names - dict str:?

    Returns
      pages - dict str:page
    """
    pages = defaultdict()
    for genre in genre_names.keys():
        try:
            pages[genre] = wikipedia.page(genre)
        except wikiepedia.PageError:
            pages[genre] = "orphan"
        except wikipedia.DisambiguationError:
            pages[k] = "ambiguous"
    return pages

def parse_for_origin(info):    
    parents = set()
    tidyreg = re.compile('[^a-zA-Z ]')
    
    for row in info.find_all('tbody'):
        if 'stylistic origins' not in str(row).lower():
            continue

        for tr in row.find_all('tr'):
            if 'origins' in str(tr).lower():
                for genre in row.find_all('li'):
                    tidytext = tidyreg.sub('', genre.text)
                    parents.add(tidytext.lower())
                    
    return list(parents)
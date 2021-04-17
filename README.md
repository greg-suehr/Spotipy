# Introduction

Spotipy is a lightweight Python library for the Spotify Web API. Learn more:
  - https://spotipy.readthedocs.io/en/latest/
  - https://developer.spotify.com/documentation/general/guides/
  - https://developer.spotify.com/documentation/web-api/reference/object-model/

This is a light Django framework built over mongoDB to serve data to my React
playlist tools.


## Datastore

The datastore component of this application saves us some time and saves Spotify
a bit of compute in a way that I believe is in accordance with the Spotify Deve-
loper terms of service.
  - https://developer.spotify.com/terms/#v

I chose mongoDB due to the nature of the Spotify Web API's uri driven navigation
and mongo's schemaless features. This application will read a lot of key-based
non-sequential - more often reading - and I anticipate additional track fetaures
making their way into the model.
  - https://docs.mongodb.com/manual/


## Classifier

The Classifier object subclasses the Spotipy client API, adding additional meth-
ods to filter response data, cache it in the datastore, and return restrucured
objects.

The following data will eventually be cached on a server hosting these playlist
tools:
  [] A genre:subgenre mapping
  [] Artist genres
  [] Track features including 'energy', 'loudness', 


## Django REST API

This will be the newest tool I will use and don't know how to spec it!


## Playlist Tools

The following tools will evenutally be provided through a hosted React app:
  [] Sort a list of playlists by attributes:
  
      >  .sort( playlists, [{attribute: []}] )
      >  # sorts playlists by a numeric `attribute` 
      >
      > .sort( [{atrribute: [tier1, tier2, tier3]} , 
      >  # sorts playlists into a list of chunks defined by a max `tier` value
      >  # .sort([1, 2, 3, 5, 8, 11], [3, 6]) = [[1,2,3], [5,8], [11]] 

  [] Reorder a list of playlists to ramp up to the maximum attribute value:

      > .ramp( playlists, attribute, nodes=[0.50], edges='min' )
      >  # returns two lists of approximately equal size and average `attribute`
      >  # ascending and decending from the max `attribute` ordered [/,\]
      >
      > .ramp( playlists, attribute, nodes[0.2,0.8], edges='max' )
      > # returns four lists of approximately equal size and average `attribute`
      > # ascending and descending from the max `attribute` ordered [\,/,\,/]

  [] Recommend tracks to remove to move and attribute to a target value
      > .trim( playlists, attribute, targer, max)˚
      > # returns a list of the smallest possible list tracks to remove from the
      > # list to move the average `attribute` near `target` value, never larger
      > # than `max` elements
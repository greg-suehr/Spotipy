SpotiPI Schema
=================

# Datastore Schema

SpotiPI implements a CLAPP Datastore for local storage of discovered data. These
tables are necessary for Datastore. Their schema should not be modified.

### request_mappings
`request_mappings` must contain at least one record for every Service API method you 
wish to wrap with load_from_datastore() and load_from_service() methods. This table
maps Service API methods to the Datastore Stores to check and load. It also stores an
expiration interval for the stored data per request_format.

If your application remaps a single Service Data Object to multiple Stores, there
should be onerecord per Store per API call. 

If your application loads a set of Stores through multiple API calls, the rule remains
one record per Store per API call. Consider adding fields to the Store to indicate the
API calls returned the Service Data Object.

For example, the following request_mappings map five Spotify Web API endpoints across 
three Stores:
||request_mapping_id||request_format||store_table_name||expire_interval||
| 1                 | 'track'       | 'track_features'| '0001-00-00'   |
| 2                 | 'track'       | 'track_genres'  | '0001-00-00'   |
| 3                 | 'tracks'      | 'track_features'| '0001-00-00'   |
| 4                 | 'tracks'      | 'track_genres'  | '0001-00-00'   |
| 5   | 'user_playlist_tracks'      | 'user_tracks'   | '0000-00-07'   |
| 6   | 'current_user_top_tracks'   | 'user_tracks'   | '0000-00-07'   |
| 7   | 'current_user_saved_tracks' | 'user_tracks'   | '0000-00-07'   |

If your application remaps a multiple Service Data Objects to a single Store, there
should be *something clever and legible*.


### request_field_mappings
`request_field_mappings` maps multiple request_mappings to a shared set of `field_mappings`.

All `request_mappings` with the same `store_table_name` must map to the same set of
`field_mapping_ids`. If multiple calls return the same Service Data Object, store the
data in the same places. 

NOTE: This is not enforced at the database level. It could be with one more bridge
table: request_mappings > request_data_objects > request_field_mappings > field_mappings.


### field_mappings
`field_mappings` must contain one record per` field per Store.

If your application maps only a subset of the data returned for a Service Data Object,
map only the fields that you wish to store in Datastore.

If your application adds additional data to a Service Data Object, add a store_table_name
and store_table_field and leave request_mapping_id and request_object_name EMPTY.

For example, the folling field_mappings maps the Spotify Web API's track and audio_feature
Service Data Objects to the `track_features` Store. Note all `track_features` fields are
mapped except for `created_date` and `expire_date`, which are managing by Datastore.

||field_mapping_id||store_table_name ||store_table_field  ||request_object_name||request_field_name||
| 1               | 'track_features' |  'track_uri'       | 'track'            | 'uri'             |
| 2               | 'track_features' |  'track_name'      | 'track'            | 'name'            |
| 3               | 'track_features' |  'duration_ms'     | 'track'            | 'duration_ms'     |
| 4               | 'track_features' |  'popularity       | 'track'            | 'popularity'      |
| 5               | 'track_features' |  'acousticness'    | 'audio_features'   | 'acousticness'    |
| 6               | 'track_features' |  'danceability'    | 'audio_features'   | 'danceability'    |
| 7               | 'track_features' |  'energy'          | 'audio_features'   | 'energy'          |
| 8               | 'track_features' | 'instrumentalness' | 'audio_features'   | 'instrumentalness'|
| 9               | 'track_features' | 'key'              | 'audio_features'   | 'key'             |
| 10              | 'track_features' | 'liveness'         | 'audio_features'   | 'liveness'        |
| 11              | 'track_features' | 'loudness'         | 'audio_features'   | 'loudness'        |
| 12              | 'track_features' | 'mode'             | 'audio_features'   | 'mode'            |
| 13              | 'track_features' | 'speechiness'      | 'audio_features'   | 'speechiness'     |
| 14              | 'track_features' | 'tempo'            | 'audio_features'   | 'tempo'           |
| 15              | 'track_features' | 'time_signature'   | 'audio_features'   | 'time_signature   |
| 16              | 'track_features' | 'valence'          | 'audio_features'   | 'valence'         |



# SpotiPi Schema

These tables store data pulled from or created from the Spotify Web API. Each table
can be loaded as a Datastore Store. Feel free to modify, drop, or create new tables
*and update `request_mappings`, `request_field_mappings`, and `field_mappings`*.


### artist_genres
`artist_genres` stores an explicit mapping of genres associated with an `artist` Object.
[insert schema]


### track_features
`track_features` stores essential data from a `track` Object and its `audio_features`.
[insert schema]


### track_genres
`track_featurs` stores an expensive, calculated genre ranking for `track` Objects.
[insert schema]


### user_tracks
`track_featurs` a list of tracks saved or played by a user and several calculated fields.
[insert schema]






import matplotlib.pyplot as plt

# features = dict()
# pid      = playlists[0]
# for t in ptracks(pid):
#     features[t['name'] = audio_features(t['uri'])[0]
#
#
#
#

energy = [0.758, 0.726, 0.636, 0.953, 0.875, 0.765, 0.815, 0.63,
          0.754, 0.716, 0.13, 0.871, 0.473, 0.668, 0.661, 0.869]

valence = [0.644, 0.413, 0.286, 0.914, 0.961, 0.736, 0.689, 0.332,
           0.257, 0.744, 0.395, 0.273, 0.616, 0.523, 0.692, 0.602]

loudness = [-6.276, -5.395, -8.468, -2.951, -3.401, -7.209, -6.355, -9.019,
            -3.713, -3.083, -13.726, -1.792, -7.548, -5.858, -8.523, -3.764]

# plt.scatter(energy, valence, s=loudness) # c = genre_color
plt.scatter(energy, valence)
plt.show()

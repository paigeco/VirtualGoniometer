from sklearn.neighbors import NearestNeighbors

#Use SkLearn to get the nearest neighbors of an array
############################################
def NearestNeighbors3D(fit_data, selected_vertexes, n_neighbors):
    if len(fit_data) < n_neighbors:
        raise ValueError("""Error #11:
                         Please lower the size of your local neighbors patch or
                         increase the number of vertexes in your model""")
    else:
        distances, indices = NearestNeighbors(n_neighbors=n_neighbors,
                                              n_jobs=-1).fit(fit_data).kneighbors(selected_vertexes)
    return distances, indices

import numpy as np

from scipy.stats import binom


def mini_batches(inputs, batch_size=1, allow_dynamic_batch_size=False,
                 shuffle=True):
    """ Generator that inputs a group of examples in numpy.ndarray by the given batch size.

    Parameters
    ----------
    inputs : numpy.array
        The input features, every row is a example.
    batch_size : int
        The batch size.
    allow_dynamic_batch_size: boolean
        Allow the use of the last data batch in case the number of examples is
        not a multiple of batch_size, this may result in unexpected behaviour
        if other functions expect a fixed-sized batch-size.
    shuffle : boolean
        Indicating whether to use a shuffling queue, shuffle the dataset before
        return.

    Examples
    --------
    >>> X = np.asarray([['a','a'], ['b','b'], ['c','c'], ['d','d'], ['e','e'], ['f','f']])
    >>> for batch in mini_batches(inputs=X, batch_size=2, shuffle=False):
    >>>     print(batch)
    array([['a', 'a'], ['b', 'b']], dtype='<U1')
    array([['c', 'c'], ['d', 'd']], dtype='<U1')
    array([['e', 'e'], ['f', 'f']], dtype='<U1')

    Source
    ------
    https://github.com/tensorlayer/tensorlayer/blob/6fea9d9d165da88e3354f723c89a0a6ccf7d8e53/tensorlayer/iterate.py#L15
    """
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)

    # for start_idx in range(0, len(inputs) - batch_size + 1, batch_size):
    # chulei: handling the case where the number of samples is not a multiple
    # of batch_size, avoiding wasting samples
    for start_idx in range(0, len(inputs), batch_size):
        end_idx = start_idx + batch_size
        if end_idx > len(inputs):
            if allow_dynamic_batch_size:
                end_idx = len(inputs)
            else:
                break
        if shuffle:
            excerpt = indices[start_idx:end_idx]
        else:
            excerpt = slice(start_idx, end_idx)
        if isinstance(inputs, list) and shuffle:
            # zsdonghao: for list indexing when shuffle==True
            yield [inputs[i] for i in excerpt]
        else:
            yield inputs[excerpt]


def mini_batches_idx(inputs, batch_size=1, allow_dynamic_batch_size=False,
                     shuffle=True):
    """ Generator that inputs a group of examples in numpy.ndarray by the given batch size.

    Parameters
    ----------
    inputs : numpy.array
        The input features, every row is a example.
    batch_size : int
        The batch size.
    allow_dynamic_batch_size: boolean
        Allow the use of the last data batch in case the number of examples is
        not a multiple of batch_size, this may result in unexpected behaviour
        if other functions expect a fixed-sized batch-size.
    shuffle : boolean
        Indicating whether to use a shuffling queue, shuffle the dataset before
        return.

    Examples
    --------
    >>> X = np.asarray([['a','a'], ['b','b'], ['c','c'], ['d','d'], ['e','e'], ['f','f']])
    >>> for batch in mini_batches(inputs=X, batch_size=2, shuffle=False):
    >>>     print(batch)
    array([['a', 'a'], ['b', 'b']], dtype='<U1')
    array([['c', 'c'], ['d', 'd']], dtype='<U1')
    array([['e', 'e'], ['f', 'f']], dtype='<U1')

    Source
    ------
    https://github.com/tensorlayer/tensorlayer/blob/6fea9d9d165da88e3354f723c89a0a6ccf7d8e53/tensorlayer/iterate.py#L15
    """
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)

    # for start_idx in range(0, len(inputs) - batch_size + 1, batch_size):
    # chulei: handling the case where the number of samples is not a multiple
    # of batch_size, avoiding wasting samples
    for start_idx in range(0, len(inputs), batch_size):
        end_idx = start_idx + batch_size
        if end_idx > len(inputs):
            if allow_dynamic_batch_size:
                end_idx = len(inputs)
            else:
                break
        if shuffle:
            excerpt = indices[start_idx:end_idx]
        else:
            excerpt = slice(start_idx, end_idx)
        yield excerpt


def mini_batches_dist(inputs, distance_matrix, batch_size=1,
                      allow_dynamic_batch_size=False, shuffle=True):
    """ Generator that inputs a group of examples in numpy.ndarray and a respective distance matrix by the given batch
    size.

    Parameters
    ----------
    inputs : numpy.array
        The input features, every row is a example.
    distance_matrix : numpy.array
        The squared distance matrix matching the inputs.
    batch_size : int
        The batch size.
    allow_dynamic_batch_size: boolean
        Allow the use of the last data batch in case the number of examples is
        not a multiple of batch_size, this may result in unexpected behaviour
        if other functions expect a fixed-sized batch-size.
    shuffle : boolean
        Indicating whether to use a shuffling queue, shuffle the dataset before
        return.

    Examples
    --------
    >>> from sklearn.neighbors.dist_metrics import DistanceMetric
    >>> X = np.asarray([[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11]])
    >>> distance_matrix = DistanceMetric.get_metric("euclidean").pairwise(X)
    >>> for batch, batch_d in mini_batches_dist(inputs=X, distance_matrix=distance_matrix, batch_size=2, shuffle=False):
    >>>     print(batch, batch_d)
    (array([[0, 1], [2,   3]]), [[0., 2.82842712], [2.82842712, 0.]])
    (array([[4, 5], [6,   7]]), [[0., 2.82842712], [2.82842712, 0.]])
    (array([[8, 9], [10, 11]]), [[0., 2.82842712], [2.82842712, 0.]])

    Source
    ------
    https://github.com/tensorlayer/tensorlayer/blob/6fea9d9d165da88e3354f723c89a0a6ccf7d8e53/tensorlayer/iterate.py#L15
    """
    assert inputs.shape[0] == distance_matrix.shape[0] == distance_matrix.shape[1]

    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)

    # for start_idx in range(0, len(inputs) - batch_size + 1, batch_size):
    # chulei: handling the case where the number of samples is not a multiple
    # of batch_size, avoiding wasting samples
    for start_idx in range(0, len(inputs), batch_size):
        end_idx = start_idx + batch_size
        if end_idx > len(inputs):
            if allow_dynamic_batch_size:
                end_idx = len(inputs)
            else:
                break
        if shuffle:
            excerpt = indices[start_idx:end_idx]
        else:
            excerpt = slice(start_idx, end_idx)
        if (isinstance(inputs, list) or isinstance(distance_matrix, list)) and shuffle:
            # zsdonghao: for list indexing when shuffle==True
            yield [inputs[i] for i in excerpt], [distance_matrix[i] for i in excerpt]
        else:
            yield inputs[excerpt], distance_matrix[excerpt][:, excerpt]


def idx_to_elements(array, idx):
    """ Returns the elements of a 2d-array located at `idx`.
    :param array: 2d numpy array from which to extract the elements.
    :param idx: An iterable of desired indexes.
    """
    return array[idx]


def idx_to_r_elements(array, idx):
    """ Returns the elements of a 2d-array NOT located at `idx`.
    In short, it does the opposite of `idx_to_elements`. Thus concatenating results from `idx_to_elements` and
    `idx_to_r_elements` applied to the same array give you the original array.

    :param array: 2d numpy array from which to extract the elements.
    :param idx: An iterable of indexes
    """
    # Note: Reversed indexes/mask can also be retrieved in other ways, but this method is currently the best memory and
    # speed wise for large datasets.
    # Other methods are :
    # r_idx = np.setdiff1d(np.arange(array.shape[0]), idx)
    # r_idx = ~np.in1d(np.arange(array.shape[0]), idx)

    r_idx = np.ones(array.shape[0], np.bool)
    r_idx[idx] = 0
    return array[r_idx]


def flatten_id(affectations, noise_cluster_id=-1):
    """ Change clusters_id of a current affectation to the smallest value possible (removing holes between two clusters
    id).

    Exemple:
    >>> affectations = np.array([0, 1, 7, 1, -1, 4])
    >>> new_affectations = flatten_id(affectations, noise_cluster_id=-1)
    >>> new_affectations
    array([ 0,  1,  3,  1, -1,  2])
    >>> assert affectations.shape[0] == new_affectations.shape[0]
    >>> for cluster_id in np.unique(affectations):
    ...    new_cluster_id = new_affectations[np.where(affectations == cluster_id)[0]][0]
    ...    assert np.all(new_affectations[affectations == cluster_id] == new_cluster_id)
    """
    new_affectations = np.zeros_like(affectations)

    if noise_cluster_id is not None:
        id_current = 0
        for id_original in np.unique(affectations):
            if id_original == noise_cluster_id:
                continue
            new_affectations[affectations == id_original] = id_current
            id_current += 1
        new_affectations[affectations == noise_cluster_id] = noise_cluster_id
    else:
        for id_current, id_original in enumerate(np.unique(affectations)):
            new_affectations[affectations == id_original] = id_current
    return new_affectations


def contingency_matrix(labels_true, labels_pred, eps=None, sparse=False):
    """ Build a contingency matrix describing the relationship between labels.
    Parameters
    ----------
    labels_true : int array, shape = [n_samples]
        Ground truth class labels to be used as a reference
    labels_pred : array, shape = [n_samples]
        Cluster labels to evaluate
    eps : None or float, optional.
        If a float, that value is added to all values in the contingency
        matrix. This helps to stop NaN propagation.
        If ``None``, nothing is adjusted.
    sparse : boolean, optional.
        If True, return a sparse CSR continency matrix. If ``eps is not None``,
        and ``sparse is True``, will throw ValueError.
        .. versionadded:: 0.18
    Returns
    -------
    contingency : {array-like, sparse}, shape=[n_classes_true, n_classes_pred]
        Matrix :math:`C` such that :math:`C_{i, j}` is the number of samples in
        true class :math:`i` and in predicted class :math:`j`. If
        ``eps is None``, the dtype of this array will be integer. If ``eps`` is
        given, the dtype will be float.
        Will be a ``scipy.sparse.csr_matrix`` if ``sparse=True``.
    Source
    ------
    https://github.com/scikit-learn/scikit-learn/blob/7813f7efb/sklearn/metrics/cluster/supervised.py#L78
    """

    if eps is not None and sparse:
        raise ValueError("Cannot set 'eps' when sparse=True")

    classes, class_idx = np.unique(labels_true, return_inverse=True)
    clusters, cluster_idx = np.unique(labels_pred, return_inverse=True)
    n_classes = classes.shape[0]
    n_clusters = clusters.shape[0]
    # Using coo_matrix to accelerate simple histogram calculation,
    # i.e. bins are consecutive integers
    # Currently, coo_matrix is faster than histogram2d for simple cases
    contingency = sp.coo_matrix((np.ones(class_idx.shape[0]),
                                 (class_idx, cluster_idx)),
                                shape=(n_classes, n_clusters),
                                dtype=np.int)
    if sparse:
        contingency = contingency.tocsr()
        contingency.sum_duplicates()
    else:
        contingency = contingency.toarray()
        if eps is not None:
            # don't use += as contingency is integer
            contingency = contingency + eps
    return contingency


if __name__ == "__main__":
    pass

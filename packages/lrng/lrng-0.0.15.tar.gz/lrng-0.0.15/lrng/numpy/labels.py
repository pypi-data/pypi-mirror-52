import numpy as np
from numba import jit, njit, int32, int64, prange
from numba.types import boolean

from .conversions import (
    _ranges_np_to_nb, _ranges_nb_to_np, _ranges_np_to_py
)
from .coalesce import _coalesce, coalesce

# @njit(boolean(int64, int64, int64, int64))
# @njit(cache=True)
def keep_q(start_a, stop_a, start_b, stop_b):
    '''
    Determines whether or not to keep the second range for labeling the first
    i.e. whether or not the range indicated by [start_b, stop_b] overlaps with
    the range designated by [start_a, stop_a]

    Notes:
        assumes start < stop

    Arguments:
        start_a (int): start of range to test against
        stop_a (int): stop of range to test against
        start_b (int): start of range in question
        stop_b (int): stop of range in question

    Returns:
        (bool): whether or not the second range overlaps the first
    '''
    if stop_b < start_a: return False
    if start_b > stop_a: return False
    return True

# @njit(int64[:,:](int64, int64, int64[:,:]))
# @njit(cache=True)
def _relevant_labels(start, stop, reference_ranges):
    '''
    Filter a set of reference ranges for those relevant to the range spaned by
    `[start, stop]`

    Arguments:
        start (int): start of range to test against
        stop (int): stop of range to test against
        reference_ranges (np.array): an integer array of shape (-1, 3)
            indicating the type of range as well as its start and stop

    Returns:
        relevant_ranges (np.array): an integer array of shape (-1, 3)
            indicating the type of range as well as its start and stop that all
            overlap with the passed arguments start and stop
    '''
    results = np.array([0][:0]).reshape(-1, 3)
    # for i in prange(len(reference_ranges)):
    for i in range(len(reference_ranges)):
        _type, start_b, stop_b = reference_ranges[i]
        if keep_q(start, stop, start_b, stop_b):
            results = np.concatenate(
                (results, np.array([[_type, start_b, stop_b]]))
            )
    return results

# @jit(forceobj=True, cache=True)
def relevant_labels(start, stop, reference_ranges, labels_order):
    '''
    Filter a set of reference ranges for those relevant to the range spaned by
    `[start, stop]`

    Arguments:
        start (int): start of range to test against
        stop (int): stop of range to test against
        reference_ranges (np.array): an integer array of shape (-1, 3)
            indicating the type of range as well as its start and stop
        labels_order (list): a list of the types of ranges which might appear
            in reference_ranges.

    Returns:
        relevant_ranges (np.array): an integer array of shape (-1, 3)
        indicating the type of range as well as its start and stop that all
        overlap with the passed arguments start and stop
    '''
    # ensure np as input
    np_labels = np.array(labels_order)
    np_ranges = np.array(reference_ranges)
    # convert string labels to integers
    np_ranges = _ranges_np_to_nb(np_ranges, np_labels)
    # filtered and simplified
    np_result = _coalesce(_relevant_labels(start, stop, np_ranges))
    np_result = _ranges_nb_to_np(np_result, np_labels)
    return _ranges_np_to_py(np_result)

# @jit(forceobj=True, cache=True)
def relevant_labels_for_ranges(ranges, reference_ranges, labels_order):
    '''
    Filter a set of reference ranges for those relevant to the range spaned by
    `[start, stop]`

    Arguments:
        start (int): start of range to test against
        stop (int): stop of range to test against
        reference_ranges (np.array): an integer array of shape (-1, 3)
            indicating the type of range as well as its start and stop
        labels_order (list): a list of the types of ranges which might appear
            in reference_ranges.

    Returns:
        relevant_ranges (np.array): an integer array of shape (-1, 3)
        indicating the type of range as well as its start and stop that all
        overlap with the passed arguments start and stop
    '''
    results = []
    for (start, stop) in ranges:
        results.append(relevant_labels(start, stop, reference_ranges, labels_order))
    return results


# @njit(int64[:,:](int64, int64, int64[:, :], int64))
# @njit(cache=True)
def _label_range(start, stop, reference_ranges, number_of_range_types, use_other_q=True):
    '''
    Encodes the range into a hot-encoding

    Arguments:
        start (int): start of range to test against
        stop (int): stop of range to test against
        reference_ranges (np.array): an integer array of shape (-1, 3)
            indicating the type of range as well as its start and stop
        number_of_range_types (int): how many channels the encoding should have

    Returns:
        encoding (np.array): an integer array of shape
            `(stop-start, number_of_range_types)` indicating the type of range
            at index `i` is relevant to the range indicated by `[start, stop]`
            based on `reference_ranges`
    '''
    range_length = stop - start
    encoding = np.zeros((range_length, number_of_range_types), dtype=np.int64)
    boundaries = reference_ranges[:,1:].T
    if reference_ranges.size == 0:
        if use_other_q:
            encoding[:, -1] = 1
        return encoding

    for i in range(range_length):
        _i = i + start
        # ranges_to_apply = np.all([
        #     reference_ranges[:, 1] <= _i,
        #     reference_ranges[:, 2] >= _i
        # ], axis=0)
        # logical_test = np.array([boundaries[0,:] <= _i, boundaries[1,:] >= _i])
        logical_test = np.concatenate((
            (boundaries[0,:] <= _i).reshape(-1, boundaries.shape[-1]),
            (boundaries[1,:] >= _i).reshape(-1, boundaries.shape[-1])
        )).T

        ranges_to_apply = np.array([np.all(logical_test[j]) for j in range(len(logical_test))])
        indices = np.unique(reference_ranges[ranges_to_apply][:, 0])

        if indices.size:
            for j in indices:
                encoding[i, j] = 1
        else:
            if use_other_q:
                encoding[i, -1] = 1
        # encoding[i, reference_ranges[ranges_to_apply][:, 0]] = 1
    return encoding

# @jit(forceobj=True, cache=True)
def label_range(start, stop, reference_ranges, labels_order, use_other_q=True):
    '''
    Encodes the range into a hot-encoding

    Arguments:
        start (int): start of range to test against
        stop (int): stop of range to test against
        reference_ranges (np.array): an integer array of shape (-1, 3)
            indicating the type of range as well as its start and stop
        labels_order (list): a list of the types of ranges which might appear
            in reference_ranges.
    Returns:
        encoding (list): an integer array of shape
            `(stop-start, number_of_range_types)` indicating the type of range
            at index `i` is relevant to the range indicated by `[start, stop]`
            based on `reference_ranges`
    '''
    # ensure np as input
    np_labels = np.array(labels_order)
    np_ranges = np.array(reference_ranges)
    # convert string labels to integers
    np_ranges = _ranges_np_to_nb(np_ranges, np_labels)
    np_result = _label_range(start, stop, np_ranges, len(labels_order), use_other_q)
    return np_result.tolist()



def missing_ranges(start:int, stop:int, ranges:list):
    '''
    Determine what regions are not labeled.

    Arguments:
        start (int): start of range to test against
        stop (int): stop of range to test against
        ranges (np.array): an integer array of shape (-1, 3)
            indicating the type of range as well as its start and stop
    Returns:
        boundaries (list): a list of `[start, stop]` positions not covered by
            ranges _regardless_ of class type.
    '''
    np_ranges = np.array(ranges)
    # erase classes
    np_ranges[:, 0] = 0
    np_ranges = np_ranges.astype(int)


    simplified = coalesce(np_ranges.astype(int), [0])
    if not isinstance(simplified, np.ndarray):
        simplified = np.array(simplified)
    boundaries = simplified[:, 1:].astype(int)
    boundaries.sort(axis=0)

    found = []

    _a = _b = start
    for a, b in boundaries:
        if _b < a:
            if _a != a-1 and a != _a:
                _b = a-1
                found.append([_a, _b])
                _a = b+1
                _b = _a

    if _a <= stop:
        found.append([_a, stop])
    return found

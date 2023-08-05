#!/usr/bin/python3

from copy import deepcopy


_coverage_eval = {}
_cached = {}
_active_txhash = set()


def add_transaction(txhash, coverage_eval):
    '''Adds coverage eval data.'''
    _coverage_eval[txhash] = coverage_eval
    _active_txhash.add(txhash)


def add_cached_transaction(txhash, coverage_eval):
    '''Adds coverage data to the cache.'''
    _cached[txhash] = coverage_eval


def check_cached(txhash, active=True):
    '''Checks if a transaction hash is present within the cache, and if yes
    includes it in the active data.'''
    if txhash in _cached:
        _coverage_eval[txhash] = _cached.pop(txhash)
        if active:
            _active_txhash.add(txhash)
    return txhash in _coverage_eval


def get_active_txlist():
    '''Returns a list of coverage hashes that are currently marked as active.'''
    return sorted(_active_txhash)


def clear_active_txlist():
    '''Clears the active coverage hash list.'''
    _active_txhash.clear()


def get_coverage_eval():
    '''Returns all coverage data, active and cached.'''
    return {**_cached, **_coverage_eval}


def get_merged_coverage_eval():
    '''Merges and returns all active coverage data as a single dict.

    Returns: coverage eval dict.
    '''
    if not _coverage_eval:
        return {}
    coverage_eval_list = list(_coverage_eval.values())
    merged_eval = deepcopy(coverage_eval_list.pop())
    for coverage_eval in coverage_eval_list:
        for name in coverage_eval:
            if name not in merged_eval:
                merged_eval[name] = coverage_eval[name]
                continue
            for path, map_ in coverage_eval[name].items():
                if path not in merged_eval[name]:
                    merged_eval[name][path] = map_
                    continue
                for i in range(3):
                    merged_eval[name][path][i] = set(merged_eval[name][path][i]).union(map_[i])
    return merged_eval


def clear():
    '''Clears all coverage eval data.'''
    _coverage_eval.clear()
    _cached.clear()
    _active_txhash.clear()

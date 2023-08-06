from .query_context import QueryContext
from .query_components import Match, Terms, Term, And, Or
from .query_result import IdsQR, IdsScoresQR
from .combine_scores.wrapped import sorted_in1d, combine_must_should

import numpy as np

def filterHandler(value, qc):
    assert type(value) is list
    assert False not in [type(obj) is dict and len(obj) == 1 for obj in value] # must contain only queries
    qc.setSetting('filter')
    clauses = [query_part_handlers[list(obj.keys())[0]](obj[list(obj.keys())[0]], qc) for obj in value]
    return And(qc)._filter(clauses)

def mustNotHandler(value, qc):
    assert type(value) is list
    assert False not in [type(obj) is dict and len(obj) == 1 for obj in value] # must contain only queries
    qc.setSetting('filter')
    clauses = [query_part_handlers[list(obj.keys())[0]](obj[list(obj.keys())[0]], qc) for obj in value]
    return Or(qc)._filter(clauses)

def mustHandler(value, qc):
    assert type(value) is list
    assert False not in [type(obj) is dict and len(obj) == 1 for obj in value] # must contain only queries
    qc.setSetting('score')
    clauses = [query_part_handlers[list(obj.keys())[0]](obj[list(obj.keys())[0]], qc) for obj in value]
    return And(qc)._score(clauses)

def shouldHandler(value, qc):
    assert type(value) is list
    assert False not in [type(obj) is dict and len(obj) == 1 for obj in value] # must contain only queries
    qc.setSetting('score')
    clauses = [query_part_handlers[list(obj.keys())[0]](obj[list(obj.keys())[0]], qc) for obj in value]
    return Or(qc)._score(clauses)


def boolHandler(value, qc):

    # _filter = query_part_handlers['filter'](value.get('filter'), qc) if value.get('filter') else None
    # _must_not = query_part_handlers['must_not'](value.get('must_not'), qc) if value.get('must_not') else None
    # _must = query_part_handlers['must'](value.get('must'), qc) if value.get('must') else None
    # _should = query_part_handlers['should'](value.get('should'), qc) if value.get('should') else None

    has_filter = value.get('filter') is not None
    has_must_not = value.get('must_not') is not None
    has_must = value.get('must') is not None
    has_should = value.get('should') is not None

    has_any_filter = has_filter or has_must_not
    has_any_score = has_must or has_should

    has_filter_and_must_not = has_filter and has_must_not
    has_must_and_should = has_must and has_should

    if has_any_filter:

        combined_filter_ids = None
        combined_filter_invert = False
        if has_filter:
            if has_must_not:
                # if it has both, we can combine them to a single ids list
                _filter = query_part_handlers['filter'](value.get('filter'), qc)
                _must_not = query_part_handlers['must_not'](value.get('must_not'), qc)

                # using sorted_in1d with invert=True returns the ids in the first arg that are not in the second
                combined_filter_ids = _filter.getIds()[sorted_in1d(_filter.getIds(), _must_not.getIds(), invert=True, assume_sorted=True)]
                combined_filter_invert = False
            else:
                _filter = query_part_handlers['filter'](value.get('filter'), qc)
                combined_filter_ids = _filter.getIds()
                combined_filter_invert = False
        else:
            combined_filter_ids = query_part_handlers['must_not'](value.get('must_not'), qc).getIds()
            combined_filter_invert = True

        if has_must_and_should:
            _should = query_part_handlers['should'](value.get('should'), qc)
            _must = query_part_handlers['must'](value.get('must'), qc)

            filtered_must_mask = sorted_in1d(_must.getIds(), combined_filter_ids, invert=combined_filter_invert)
            _filtered_must_qr = IdsScoresQR(_must.getIds()[filtered_must_mask], _must.getScores()[filtered_must_mask])
            fm_s_ids, fm_s_scores = combine_must_should(_filtered_must_qr.getIds(), _filtered_must_qr.getScores(), _should.getIds(), _should.getScores(), assume_sorted=True)
            return IdsScoresQR(fm_s_ids, fm_s_scores)
        elif has_must:
            _must = query_part_handlers['must'](value.get('must'), qc)

            filtered_must_mask = sorted_in1d(_must.getIds(), combined_filter_ids, invert=combined_filter_invert, assume_sorted=True)
            _filtered_must_qr = IdsScoresQR(_must.getIds()[filtered_must_mask], _must.getScores()[filtered_must_mask])
            return _filtered_must_qr
        elif has_should:
            _should = query_part_handlers['should'](value.get('should'), qc)

            filtered_should_mask = sorted_in1d(_should.getIds(), combined_filter_ids, invert=combined_filter_invert, assume_sorted=True)
            _filtered_should_qr = IdsScoresQR(_should.getIds()[filtered_should_mask], _should.getScores()[filtered_should_mask])
            return _filtered_should_qr
        else:
            return IdsQR().fromIds(combined_filter_ids)
          
    else:
        # there are not filter / must_not
        # if there is must and should we combine, otherwise, return the one present
        if has_must_and_should:
            # combine must and should
            _should = query_part_handlers['should'](value.get('should'), qc)
            _must = query_part_handlers['must'](value.get('must'), qc)
            fm_s_ids, fm_s_scores = combine_must_should(_must.getIds(), _must.getScores(), _should.getIds(), _should.getScores(), assume_sorted=True)
            return IdsScoresQR(fm_s_ids, fm_s_scores)
        elif has_must:
            _must = query_part_handlers['must'](value.get('must'), qc)
            return _must
        else:
            _should = query_part_handlers['should'](value.get('should'), qc)
            return _should


# def boolHandler(value, qc):
#     assert type(value) is dict
#     # confirm only keys are filter, should, must, must_not
#     allowed_keys = {'filter', 'must', 'should', 'must_not'}
#     False not in [key in allowed_keys for key in value]
    
#     # TODO: think harder about this, make sure correct
#     qc.filter_ids = None
#     qc.not_filter_ids = None

#     filter_clause = value.get('filter')
#     filter_results = None
#     if filter_clause is not None:
#         filter_results = query_part_handlers['filter'](filter_clause, qc)
# #         qc.filter_ids = filter_results.getIds()
    
#     must_not_clause = value.get('must_not')
#     must_not_results = None
#     if must_not_clause is not None:
#         must_not_results = query_part_handlers['must_not'](must_not_clause, qc)
#         qc.not_filter_ids = must_not_results.getIds()
    
#     # if a filter or must_not is specified, the results of the must and should clauses
#     # are restricted to fitting those specs. thus we must first perform those first
    
    
#     must_clause = value.get('must')
#     must_results = None
#     if must_clause is not None:
#         must_results = query_part_handlers['must'](must_clause, qc)
    
    
#     if must_results is not None:
#         if qc.filter_ids is not None:
#             qc.filter_ids = filter_results.getIds()
#             return must_results.getFilteredQR(qc)
#         else:
#             return must_results
    
#     # if a must is specified, it will score documents which match all the filters + must_not
#     # as well as score for each clause in the must query
#     # thus documents resturned by the must clause already have had the filters applied
#     # since the should clause only adds scores to documents that have satisfied the others, 
#     # we pass in the must clause if there was one and do a min_should_match=2 combine with the should results
#     # with the must ids as the candidates
#     # if there was no must, we only pass in the filters/must_not ids
#     # if there were neither, we pass None
        
#     should_clause = value.get('should')
#     should_results = None
#     if should_clause is not None:
#         should_results = query_part_handlers['should'](should_clause)
    
   
    

def termHandler(value, qc):
    assert type(value) is dict and len(value) == 1
    
    field = [key for key in value][0]
    o = value[field]
    term = o.get('value')
    assert term is not None
    boost = o.get('boost')
    
    if qc.setting == 'filter':
        assert boost is None
        return Term(qc)._filter(field, term)
    elif qc.setting == 'score':
        return Term(qc)._score(field, term, score=boost)
    else:
        assert False

def matchHandler(value, qc):
    assert type(value) is dict and len(value) == 1
    field = [key for key in value][0]
    terms = value[field]
    
    if qc.setting == 'filter':
        return Match(qc)._filter(field, terms)
    elif qc.setting == 'score':
        return Match(qc)._score(field, terms)
    else:
        assert False
    

query_part_handlers = {
    'bool': boolHandler,
    'filter': filterHandler,
    'must': mustHandler,
    'should': shouldHandler,
    'must_not': mustNotHandler,
    'term': termHandler,
    'match': matchHandler
}

def doQuery(query, index=None):
    qc = QueryContext(index)
    qc.setSetting('filter')
    assert len(query) == 1
    entrypoint = [key for key in query][0]
    return query_part_handlers[entrypoint](query[entrypoint], qc)
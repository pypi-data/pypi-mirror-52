""" Metabolite Query
:Author: Bilal Shaikh <bilalshaikh42@gmail.com>
        Zhouyang Lian <zhouyang.lian@familian.life>
:Date: 2019-08-01
:Copyright: 2019, Karr Lab
:License: MIT
"""

from datanator_query_python.util import mongo_util, chem_util, file_util
from . import query_metabolites_meta

class QueryMetabolites(mongo_util.MongoUtil):
    '''Queries specific to metabolites (ECMDB, YMDB) collection
    '''

    def __init__(self, cache_dirname=None, MongoDB=None, replicaSet=None, db=None,
                 verbose=True, max_entries=float('inf'), username=None,
                 password=None, authSource='admin', readPreference='primary'):
        self.verbose = verbose
        super().__init__(cache_dirname=cache_dirname,
                         MongoDB=MongoDB,
                         replicaSet=replicaSet,
                         db=db,
                         verbose=verbose,
                         max_entries=max_entries,
                         username=username,
                         password=password,
                         authSource=authSource,
                         readPreference=readPreference)
        self.client_ecmdb, self.db_ecmdb, self.collection_ecmdb = self.con_db('ecmdb')
        self.client_ymdb, self.db_ymdb, self.collection_ymdb = self.con_db(
            'ymdb')
        self.metabolites_meta_manager = query_metabolites_meta.QueryMetabolitesMeta(
            cache_dirname=cache_dirname,
            MongoDB=MongoDB,
            replicaSet=replicaSet,
            db=db,
            collection_str='metabolites_meta',
            verbose=verbose,
            max_entries=max_entries,
            username=username,
            password=password,
            authSource=authSource,
            readPreference=readPreference)
        self.chem_manager = chem_util.ChemUtil()

    def get_conc_from_inchi(self, inchi, consensus=False):
        ''' Given inchi, find the metabolite's concentration
            values.
            Args: 
                inchi (`obj`: str): inchi of metabolite
                consensus (`obj`: bool): whether to return consensus values or list of
                                        individual values
            Return:
                result (`obj`: list of `obj`: dict): concentration values separated by collections
                e.g. [{'ymdb': }, {'ecmdb': }]
        '''
        inchi = 'InChI=' + inchi
        hashed_inchi = self.chem_manager.inchi_to_inchikey(inchi)
        query = {'InChI_Key': hashed_inchi}
        projection = {'_id': 0, 'concentrations': 1, 'name': 1, 'species': 1,
        'description': 1, 'inchikey': 1}
        result = []

        ids = self.metabolites_meta_manager.get_ids_from_hash(hashed_inchi)
        ecmdb_id = ids['m2m_id']
        ymdb_id = ids['ymdb_id']

        docs_ecmdb = self.collection_ecmdb.find_one(filter={'m2m_id': ecmdb_id}, projection=projection)
        docs_ymdb = self.collection_ymdb.find_one(filter={'ymdb_id': ymdb_id}, projection=projection)

        def calc_consensus(_list):
            conc_list = [float(x) for x in _list]
            cons_val = sum(conc_list) / len(conc_list)
            return cons_val

        def append_result(_dict):
            if _dict is not None:
                conc_ecmdb = _dict.get('concentrations', None)
                if consensus is True and conc_ecmdb is not None:
                    conc_list = _dict['concentrations']['concentration']
                    cons_val = calc_consensus(conc_list)
                    _dict['consensus_value'] = cons_val
                result.append(_dict)

        append_result(docs_ecmdb)
        append_result(docs_ymdb)

        if len(result) == 0:
            return [{
                'name': 'no available information',
                'species': 'no available information',
                'description': 'no available information',
                'inchikey': 'no available information'
            }]
        else:
            return result
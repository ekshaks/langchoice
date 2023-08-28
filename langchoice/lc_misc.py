#S.lang_check -> S.trigger, S.match, S.exception, S.eval, S.check, S.guardeval, guardcheck

class StoreFaiss:
    def __init__(self) -> None:
        pass
        '''
        vec_list = np.array([d["vec"] for d in self.mem])
        catid_list = np.array([d["catid"] for d in self.mem])
        
        self.index = faiss.IndexFlatL2(self.enc_dim) #or faiss. IndexIVF
        self.index2 = faiss.IndexIDMap(self.index)
        self.index2.add_with_ids(vec_list, catid_list) #vec with metadata

        write_index(self.index2, self.index_fname)
        '''

        #how reverse map? vec -> cat
        #store vec with metadata (min faiss dep) | add cat bits to vector (numpy based)

        #mem clusters. knn? lookup: vector -> cluster id

    def _find_nearest_cluster_id(self, qvec, index):
    
        qvec = qvec.reshape(1,-1)
        k = 1
        distances, indices  = index.search(qvec, k)
        nearest_cluster_index = nearest_neighbor_index = indices[0][0]
        return nearest_cluster_index


    def find_matches(self, qvec, index):
        cid = self._find_nearest_cluster_id(qvec, index)
        print(cid)
        category = self.category_list[cid]
        utterances = self.cat2sents[category]
        return category, utterances

    def get_index(self):
        import faiss
        from faiss import write_index, read_index
        assert Path(self.index_fname).exists()
        index = read_index(self.index_fname)
        return index

    def find_match_low (self, query_msg):
        qvec = text_embed(query_msg, self.encoder)
        index = self.get_index()

        category, utterances = self.find_matches(qvec, index)
        print(category, utterances)
        return category, utterances
    
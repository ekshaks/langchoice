from typing import List, Tuple, Union, Dict, Any
from typing import TypeVar
import numpy as np
from pathlib import Path


#from embed import text_embed
import chromadb
import numpy as np

Intent = TypeVar("Intent") #str
Utt = TypeVar("Utt") #str


class LangStore:
    def __init__(self, cat2sents: Dict[Intent, List[Utt]], 
                 index_path='/tmp/lc', name="all-docs", distance='l2', rebuild=False) -> None:
        self.cat2sents = cat2sents
        self.category_list = list(cat2sents.keys())
        self.cat2id = lambda cat: self.category_list.index(cat)
        self.distance = distance

        self.index_path = index_path
        self.client = chromadb.PersistentClient(path=self.index_path)
        
        if rebuild:
            try:
                #coll = self.client.get_collection(name=name)
                self.client.delete_collection(name=name)
            except:
                pass

        self.collection = self.client.get_or_create_collection(name)
        # metadata={"hnsw:space": "cosine"} # l2 default. ip | cosine

        if self.collection.count() == 0:
            self.index()

    def index(self, reset=False):
        print('Indexing..')
        if reset:
            self.client.reset()
            self.collection = self.client.get_or_create_collection("lc-all-docs")

        self.mem= [] #(catid | vec | doc_id)*

        for cat, utts in self.cat2sents.items():
            for i, utt in enumerate(utts):
                if not isinstance(utt, str): continue
                self.mem.append(dict(category=cat, text=utt, doc_id=f'{cat}_{i}'))

        self.collection.add(
            documents=[d['text'] for d in self.mem],
            metadatas=[dict(category= d['category'], label='') for d in self.mem],
            ids=[d['doc_id'] for d in self.mem]
        )

        self.topic2centroid = self.make_centroid_for_topics()

        if self.topic2centroid is not None:
            print('building centroids...')
            topics = list(self.topic2centroid.keys())
            self.collection.add(
                documents=[f'rep-{topic}' for topic in topics],
                metadatas=[dict(category=f'__lc__{topic}', ocategory=topic, label='centroid') for topic in topics],
                ids=[f'_{topic}' for topic in topics],
                embeddings= [self.topic2centroid[topic].tolist() for topic in topics]
            )
    
    def make_centroid_for_topics(self, topics=None):
        #include=['embeddings']
        #get all embeddings
        top2centroid = {}
        topics = topics or self.category_list
        for top in topics:
            top_docs = self.collection.get(
                include=['embeddings'],
                where={'category': top}
            )
            #print(top, top_docs)
            top_emb: 'n, d' = np.array(top_docs['embeddings'])
            #print(cat_emb.shape)
            centroid = top_emb.mean(axis=0)
            #print(f'centroid for {top}: {centroid.shape}')
            top2centroid[top] = centroid
        
        return top2centroid

    def show_match_debug(self, query, results):
        from .common import DD
        import pandas as pd
        print(f'query: {query}')
        print(f'nearest documents:')
        #print(results)
        results = DD(results)
        ids, distances, documents = results.ids[0], results.distances[0], results.documents[0]
        df = pd.DataFrame(dict(ids=ids, distances=distances, documents=documents) )
        print(df)

    def match_centroid(self, query_msg, threshold=None, debug=False, debug_k=None):

        results = self.collection.query(
            query_texts=[query_msg],
            n_results=len(self.category_list),
            where={"label": "centroid"}
            #where_document={"$contains":"rep-"}
        )

        if debug:
            self.show_match_debug(query_msg, results)


        return self.get_final_answer(results, threshold, topic_field='ocategory')


    def match(self, query_msg, threshold=None, n=1, debug=False, debug_k=None):
        '''
        1. min dist to cluster centroid. (match_centroid)
        2. min dist to vec. map vec to cluster id. (this function)

        debug_k: show nearest top k  for debugging
        '''
        if debug and debug_k is not None:
            n = debug_k

        results = self.collection.query(
            query_texts=[query_msg],
            n_results=n,
            where={"label": ''}

            # where={"metadata_field": "is_equal_to_this"}, # optional filter
            # where_document={"$contains":"search_string"}  # optional filter
        )

        if debug: 
            self.show_match_debug(query_msg, results)
        
        return self.get_final_answer(results, threshold, topic_field='category')
    
    def get_final_answer(self, results, threshold, topic_field='category'):
        '''
        Pick the lowest distance (nearest) result and return its fields.
        If threshold is specified and nearest result is farther than threshold, return None 
        '''
        doc_idx, query_txt_idx = 0, 0
        category = results['metadatas'][query_txt_idx][doc_idx][topic_field]
        distance = results['distances'][query_txt_idx][doc_idx]
        utterances = self.cat2sents[category]
        metadata = dict(distance=distance, utterances=utterances)

        if threshold is None: 
            return category, metadata
        else:
            if distance < threshold:
                return category, metadata
            else:
                return None




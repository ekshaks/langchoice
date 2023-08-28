from typing import List, Tuple, Union, Dict, Any
from typing import TypeVar
import numpy as np
from pathlib import Path


#from embed import text_embed
import chromadb

Category = TypeVar("Category") #str
Utt = TypeVar("Utt") #str


class LangStore:
    def __init__(self, cat2sents: Dict[Category, List[Utt]], index_path='/tmp/gm') -> None:
        self.cat2sents = cat2sents
        self.category_list = list(cat2sents.keys())
        self.cat2id = lambda cat: self.category_list.index(cat)

        self.index_path = index_path
        self.client = chromadb.PersistentClient(path=self.index_path)
        self.collection = self.client.get_or_create_collection("gm-all")


    def index(self):
        self.mem= [] #(catid | vec | doc_id)*

        for cat, utts in self.cat2sents.items():
            for i, utt in enumerate(utts):
                self.mem.append(dict(category=cat, text=utt, doc_id=f'{cat}_{i}'))

        self.collection.add(
            documents=[d['text'] for d in self.mem],
            metadatas=[dict(category= d['category']) for d in self.mem],
            ids=[d['doc_id'] for d in self.mem]
        )

    def find_match(self, query_msg, n=1):
        '''
        1. avg dist per cluster. pick cluster with min dist
        2. min dist to vec. map vec to cluster id. (implemented)
        '''
        results = self.collection.query(
            query_texts=[query_msg],
            n_results=n,
            # where={"metadata_field": "is_equal_to_this"}, # optional filter
            # where_document={"$contains":"search_string"}  # optional filter
        )
        doc_idx, query_txt_idx = 0, 0
        category = results['metadatas'][query_txt_idx][doc_idx]['category']
        utterances = self.cat2sents[category]
        return category, utterances

    def lang_check(self, query_msg): 
        '''
        TODO: ambiguity resolution:
        if top k topics very close (< dist d), then return all topics, distances to 
        decide later.
        '''
        return self.find_match(query_msg, n=1)


def index_or_query():

    #S.index()
    res = S.find_match('hi there', n=3)
    print(res)


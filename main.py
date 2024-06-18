
import requests, zipfile, io
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import itertools
import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
import os
import json
url_=os.environ['URL_COURSES']
print(url_)

def download_data():
    r= requests.get(url_)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("data/")

def download_configs():
    r= requests.get(os.environ['URL_CONFIGS'])
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall("configs/")
def post_data(data):
    url =os.environ['URL_POST']
    requests.post(url, data=json.dumps(data), headers={
    'Content-type':'application/json', 
    'Accept':'application/json'})

def run_model():
    download_data()
    download_configs()
    infernce_model=Recomedation()
    print(2222222222112222)
    post_data(infernce_model.get_model_recomendation_all())


class Recomedation:
    def __init__(self):
        self.queryes=pd.read_pickle('src/feature.pkl')
        self.model=SentenceTransformer("src/fine_tuned_model")
        self.courses=self.download_data('data/courses')
        self.dict_profeesional_roles=self.download_data('configs/dict_profeesional_roles')
        self.dict_level_position=self.download_data('configs/dict_level_position')
    def download_data(self,cname: str):
        return pd.read_csv(cname+'.csv', sep=';',encoding='IBM866')
    def download_pkl(self,cname: str):
        return pd.read_pickle(cname+'.pkl')
    def make_query(self,profession,level):
        if profession in self.queryes.professia.unique():
            exp =self.queryes[(self.queryes.professia==profession) & (self.queryes.level==level)].exp.values[0]
            skill_set = self.queryes[(self.queryes.professia==profession) & (self.queryes.level==level)].skill_set.values[0]
            query=' '.join(exp.split('|')).replace(',',' ')+ ' '.join(skill_set.split('|'))
            return query
        else:
            return profession
    def infrence_model(self,query):
        sentences_a1 = [query]+[str(row) for row in self.courses['Описание курса'][:]]
        sentences_embeddings_a1 = self.model.encode(sentences_a1)
        #let's calculate cosine similarity for sentence 0:
        similar_value_a1 = cosine_similarity(
            [sentences_embeddings_a1[0]],
            sentences_embeddings_a1[1:])
        return similar_value_a1.tolist()[0]  
    def get_model_recomendation_by_level_position(self,profession,level):
        query=self.make_query(profession,level)  
        return self.infrence_model(query)  
    def  get_model_recomendation_all(self):
        res_list=[]
        for i,row in self.dict_level_position[:].iterrows():
            tmp=self.courses[:].copy()
            tmp['est']=self.get_model_recomendation_by_level_position(row.profession_role,row.level)
            res_dict={"type":"career","subjectArea":row.profession_role,"level": row.level, 
            "courses":tmp.sort_values(by='est',ascending=0)['ID курса'].values[:30].tolist()}
            res_list.append(res_dict)
        return res_list     
if __name__ == "__main__":   
    run_model()

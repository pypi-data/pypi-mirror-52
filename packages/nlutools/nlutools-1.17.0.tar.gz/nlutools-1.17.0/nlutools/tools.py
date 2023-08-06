import subprocess

from config import mapConf, supportConf, bertModelConf
from online_bert_client import bert_vector
from rpc_client import doTask, doCustomTask, doNameEntity
from utils import *
import os


# Segment
def cut(sentence,pos=True,cut_all=False,mode='fast'):
    try:
        if mode in ['fast','accurate'] and pos in [True,False] and cut_all in [True,False]:
            data={'text':sentence,'mode':mode,'pos':pos,'cut_all':cut_all}
            serverName='segmentor'
            if sentence == "":
                return {"text":"", "items":[], "pos":[], "np":[], "entity":[]}
            res = doTask(serverName,data)
            return res
        else:
            raiseException('Advise:check parameters,make sure value of mode is fast or default , value of pos is true,false or default as well')
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%(serverName,supportConf[serverName],e))

# Word2Vector
def getW2VFile(version_key,localpath):
    try:
        if not version_key or not version_key.strip():
            cat = subprocess.Popen(['hadoop', 'fs', '-cat', mapConf['w2v_hdfs_version_file']], stdout=subprocess.PIPE)
            for line in cat.stdout:
                version_key=bytes.decode(line).strip()
                break
        if version_key and version_key.strip():
            try:
                subprocess.call(['hadoop','fs','-get',mapConf['w2v_hdfs_dir']+version_key.lower(),localpath])
            except Exception as e:
                raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%('w2v',supportConf['w2v'],e))
    except Exception as e:
        raise Exception('Advise: please install hadoop client before use getW2VFile')

def getSimiScore(word1,word2,type='ifchange'):
    try:
        data ={'type':type,'word1':word1,'word2':word2}
        serverName='w2v'
        return float(doTask(serverName,data))
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%(serverName,supportConf[serverName],e))
# alias
def simiscore(word1, word2, type='ifchange'):
    return getSimiScore(word1, word2, type)

def getWordVec(word,type='ifchange'):
    try:
        if isinstance(word,str):
            word = [word]
        data = {'words':word,'type':type}
        serverName='w2v'
        return doTask(serverName,data)
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%(serverName,supportConf[serverName],e))
# alias
def w2v(word, type='ifchange'):
    return getWordVec(word, type)

def getMostSimiWords(word,topn=10,type='ifchange'):
    try:
        data = {'words':word,'topn':topn,'type':type}
        serverName='w2v'
        return doTask(serverName,data)
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%(serverName,supportConf[serverName],e))
# alias
def simiwords(word, topn=10, type='ifchange'):
    return getMostSimiWords(word, topn, type)

def getCharacterVec(character):
    pass

# Sentence2Vector
def getSentenceVec(sentences,type='ifchange'):
    try:
        if isinstance(sentences,list):
            data = {'senlist':sentences,'type':type}
            serverName='sentencevec'
            return doTask(serverName,data)
        return None
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%(serverName,supportConf[serverName],e))
# alias
def senvec(sentences,type='ifchange'):
    return getSentenceVec(sentences, type)
    
# LanguageModel

# EmotionParser
def predictEmotion(sentences, prob=False):
    try:
        if sentences:
            data = {'text':sentences,'prob':prob}
            serverName='sentiment'
            res =  doTask(serverName,data)
            if prob:
                newlabel = []
                for l in res['labels']:
                    newlabel.append((l.split('_')[0], float(int(l.split('_')[1][:-1]) / 100)))
                res['labels'] = newlabel
                return res
            else:
                return res
        return None
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%(serverName,supportConf[serverName],e))
# alias
def emotion(sentences, prob=False):
    return predictEmotion(sentences, prob)

# SentenceSpliter
def getSubSentences(sentence,mode=0):
    try:
        if mode == 0 or mode == 1:
            data={'sentence':sentence,'mode':mode}
            serverName='sentence_spliter'
            return doTask(serverName,data)
        else:
            raiseException('Advise: make sure value of mode is 0 or 1')
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%(serverName,supportConf[serverName],e))
# alias
def split(sentence,mode=0):
    return getSubSentences(sentence, mode)

#EntityParser

#SentenceTypeParser

bertVector = bert_vector()
def getBertSentenceVec(texts,mode='wwm_ext'):
    try:
        bertVector.buildConnection()
        result = bertVector.parse(texts, mode)
        bertVector.close(mode)
        return result
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%('sentence vector',supportConf['bert_service'],e))
# alias
def bertvec(texts, mode='wwm_ext'):
    return getBertSentenceVec(texts, mode)

def getBertModels(model_name, output_dir=None):
    try:
        model_dir = bertModelConf.get(model_name)
        if not model_dir:
            print('Please check pass in valid model_name')
            print('Following models are available:')
            print('base_cn, wwm, wwm_ext, ernie_cv')
        else:
            print('Model Dir: ', model_dir)
            if output_dir:
                os.system('mkdir -p %s' % output_dir)
                ret = os.system('hadoop fs -get %s %s' % (model_dir, output_dir))
                if ret:
                    print('Ddownload succeed!')
                else:
                    print('Please check whether model exists and concat %s' % supportConf['bert_service'])
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%('sentence vector',supportConf['bert_service'],e))
# alias
def bertmodels(model_name, output_dir = None):
    getBertModels(model_name, output_dir)

def getKeywords(content,topk,with_weight):
    try:
        data = {'content':content,'topk':topk,'with_weight':with_weight}
        serverName = 'keywords'
        return doTask(serverName,data)
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%(serverName,supportConf[serverName],e))
# alias
def keywords(content, topk=3, with_weight=False):
    return getKeywords(content, topk, with_weight)

def getSentenceSimi(text1,text2,precision=100,type='ifchange'):
    try:
        data = {'text1':text1,'text2':text2,'precision':precision,'type':type}
        serverName = 'sentencesim'
        return doTask(serverName,data)
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%(serverName,supportConf[serverName],e))
# alias
def sensimi(text1,text2,precision=100,type='ifchange'):
    return getSentenceSimi(text1,text2,precision,type)

def getVOB(content,mode='fast'):
    try:
        data = {'content':content,'mode':mode}
        serverName = 'verbobject'
        return doTask(serverName,data)
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%(serverName,supportConf[serverName],e))
# alias
def vob(content, mode='fast'):
    return getVOB(content, mode)

def getSentenceRationality(text,with_word_prob = 'false'):
    try:
        data = {'text':text,'word_prob':with_word_prob}
        serverName = 'rationality'
        return doTask(serverName,data)
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%(serverName,supportConf[serverName],e))
# alias
def rationality(text, with_word_prob = 'false'):
    return getSentenceRationality(text, with_word_prob)

def doEntityTask(text,m):
    try:
        serverName = 'entity'
        return doCustomTask(serverName,text,m)
    except Exception as e:
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s'%(serverName,supportConf[serverName],e))
# alias
def ner(text, m):
    return doEntityTask(text, m)

def namener(text):
    return doNameEntity(text)

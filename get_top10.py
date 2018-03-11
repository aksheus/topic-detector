import argparse
import os
import sys 
import gc
from nltk import RegexpTokenizer,pos_tag
from collections import defaultdict
from operator import itemgetter
from multiprocessing import Pool
"""

       USAGE: python get_top10.py --mode <task1 or task2> --path <path to directory or file> --out <out file name> --stopw <path to stopwords file> [OPTIONAL] --top <top k topics default 10> 

       Example1: python get_top10.py --mode task1 --path ./ubuntu_dialogs/4  --out  ./top10from4.txt --stopw stopwords.txt

       Example2: python get_top10.py --mode task2 --path ./ubuntu_dialogs/4/3.tsv  --out  ./top10from4.txt --stopw stopwords.txt --top 5

       Returns: top 10 topics in the corpus by default (or) top k topics 
"""

def get_filenames(tsv_dir):
    """
         Args: directory containing corpus

         Returns: files in directory ireratively
    """
    for tsv_filename in os.listdir(tsv_dir):
        yield os.path.join(tsv_dir,tsv_filename) 


def get_topics_from_file(tsv_file):
    """
        Args: path to tsv file

        Returns: candidate topics from file
    """
    nouns = {'NN', 'NNS','NNPS','FW','JJ','JJR','JJS','VB','VBD','VBG','VBN','VBP','VBZ'}
    topics = []
    tokenizer = RegexpTokenizer(r'\w+')
    with open(tsv_file,'r',errors='ignore') as tsvin:
        for row in tsvin:
            text = row.split('\t')[-1].strip()
            tokens = tokenizer.tokenize(text)
            topics += [token.lower() for token,tag in pos_tag(tokens) if tag in nouns]
    return tuple(topics)


def get_stop_words(stop_words_file):
    """
         Args: path to stop words file

         Returns: set of stop words
    """
    stop_words = set()
    with open(stop_words_file,'r',errors='ignore') as stopw_file:
        for line in stopw_file:
            stop_words.add(line.strip())
    return stop_words



def get_top10(mode,tsv_path,out_file,stop_words_file,k=10):
    """
         Args: mode task1 (or) task2, path to coprus or file, output file name, path to stop words file, return top k topics

         Returns: top k topics in out file, by default 10  

    """
    stop_words = get_stop_words(stop_words_file)
    pool = Pool()
    vocab = defaultdict(lambda:0,{})

    if mode == 'task1':
        all_topics = pool.imap(get_topics_from_file,get_filenames(tsv_path))
        for topics in all_topics:
            for topic in topics:
                if topic not in stop_words:
                    vocab[topic]+=1
    elif mode=='task2':
        all_topics = get_topics_from_file(tsv_path)
        for topic in all_topics:
            if topic not in stop_words:
                vocab[topic]+=1

    topics_freq = [ (topic,vocab[topic]) for topic in vocab.keys()]
    vocab = {}
    gc.collect()
    topics_freq.sort(reverse=True,key=itemgetter(-1))

    with open(out_file,'w') as out:
        out.write('Top {} topics'.format(k))
        out.write('\n')
        #out.write('Index Topic Occurences')
        out.write('\n')
        if len(topics_freq) > k:
            for x in range(k):
                out.write('{}) {} '.format(x+1,topics_freq[x][0]))
                out.write('\n')
        else:
            for x in range(len(topics_freq)):
                out.write('{}) {} '.format(x+1,topics_freq[x][0]))
                out.write('\n')
        


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='python get_top10.py --path <path to directory containing .tsv files> --out <outfile> --stopw <path to stopwords file> [OPTIONAL] --top <top k topics default 10')
    parser.add_argument('-m','--mode',help='task1 or task2',required=True)
    parser.add_argument('-p','--path',help='path to directory containing .tsv files',required=True)
    parser.add_argument('-o','--out',help='output file name',required=True)
    parser.add_argument('-s','--stopw',help='path to stopwords file',required=True)
    parser.add_argument('-t','--top',help='[OPTIONAL] top k topics default 10',required=False)

    args= vars(parser.parse_args())

    if os.path.exists(args['path']):
        if args['top']!= None:
            get_top10(args['mode'],args['path'],args['out'],args['stopw'],int(args['top']))
        else:
            get_top10(args['mode'],args['path'],args['out'],args['stopw'])
    else:
        print('invalid argument for path, exiting with code 1')
        sys.exit(1)









    


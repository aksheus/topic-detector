import argparse
import os
import sys 
import gc
from nltk import word_tokenize,pos_tag
from collections import defaultdict
from operator import itemgetter
from multiprocessing import Pool

"""

       USAGE: python get_top10.py --path <path to directory containing .tsv files> --out <outfile> --stopw <path to stopwords file> [OPTIONAL] --top <top k topics default 10> 

       Example: python get_top10.py --path ./4  --out  ./top10from4.txt

       Returns: top 10 topics in the corpus
"""

def get_filenames(tsv_dir):
    for tsv_filename in os.listdir(tsv_dir):
        yield os.path.join(tsv_dir,tsv_filename) 


def get_topics_from_file(tsv_file):
    """
        Args: path to tsv file

        Returns: text field in tsv from tsv file
    """
    nouns = {'NN', 'NNS','NNPS'}
    topics = []
    with open(tsv_file,'r',errors='ignore') as tsvin:
        for row in tsvin:
            text = row.split('\t')[-1].strip()
            tokens = word_tokenize(text)
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



def get_top10(tsv_dir,out_file,stop_words_file,k=10):
    """
         Args: path to coprus, output file name, path to stop words file, return top k topics

         Returns: top k topics in out file, by default 10  

    """
    #nouns = {'NN', 'NNS','NNPS'} #NNP
    stop_words = get_stop_words(stop_words_file)
    pool = Pool()
    # later we will maintain vocab at length 10, by keeping it sorted at all times
    # saves a lot of memory
    vocab = defaultdict(lambda:0,{})

    all_topics = pool.imap(get_topics_from_file,get_filenames(tsv_dir))

    for topics in all_topics:
        for topic in topics:
            if topic not in stop_words:
                vocab[topic]+=1

    """for tsv_filename in os.listdir(tsv_dir):
        tsv_file = os.path.join(tsv_dir,tsv_filename)
        if os.path.isfile(tsv_file):
            for text in text_generator(tsv_file):
                tokens = word_tokenize(text)
                topics = [token.lower() for token,tag in pos_tag(tokens) if tag in nouns]
                topics = [topic for topic in topics if topic not in stop_words]
                for topic in topics:
                    vocab[topic]+=1"""

    topics_freq = [ (topic,vocab[topic]) for topic in vocab.keys()]
    vocab = {}
    gc.collect()
    topics_freq.sort(reverse=True,key=itemgetter(-1))

    with open(out_file,'w') as out:
        out.write('Top {} topics'.format(k))
        out.write('\n')
        for x in range(k):
            out.write('{}) {} {}'.format(x+1,topics_freq[x][0],topics_freq[x][1]))
            out.write('\n')
    


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='python get_top10.py --path <path to directory containing .tsv files> --out <outfile> --stopw <path to stopwords file> [OPTIONAL] --top <top k topics default 10')
    parser.add_argument('-p','--path',help='path to directory containing .tsv files',required=True)
    parser.add_argument('-o','--out',help='output file name',required=True)
    parser.add_argument('-s','--stopw',help='path to stopwords file',required=True)
    parser.add_argument('-t','--top',help='[OPTIONAL] top k topics default 10',required=False)

    args= vars(parser.parse_args())

    if os.path.isdir(args['path']):
        if args['top']!= None:
            get_top10(args['path'],args['out'],args['stopw'],int(args['top']))
        else:
            get_top10(args['path'],args['out'],args['stopw'])
    else:
        print('invalid directory for tsv file corpus, exiting with code 1')
        sys.exit(1)








    


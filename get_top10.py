import argparse
import os
import sys 
from nltk import word_tokenize,pos_tag
from collections import defaultdict

"""

       USAGE: python get_top10.py --path <path to directory containing .tsv files> --out <outfile>

       Example: python get_top10.py --path ./4  --out  ./top10from4.txt

       Returns: top 10 topics in the corpus
"""


def text_generator(tsv_file):
    """
        Args: path to tsv file

        Returns: text field in tsv from tsv file
    """
    with open(tsv_file,'r') as tsvin:
        for row in tsvin:
            yield row.split('\t')[-1].strip()


def get_top10(tsv_dir,out_file):

    nouns = {'NN', 'NNS', 'NNP', 'NNPS'}
    # later we will maintain vocab at length 10, by keeping it sorted at all times
    # saves a lot of memory
    vocab = defaultdict(lambda:0,{})

    for tsv_filename in os.listdir(tsv_dir):
        tsv_file = os.path.join(tsv_dir,tsv_filename)
        if os.path.isfile(tsv_file):
            for text in text_generator(tsv_file):
                tokens = word_tokenize(text)
                topics = [token for token,tag in pos_tag(tokens) if tag in nouns]
                for topic in topics:
                    vocab[topic]+=1

    print(len(vocab))
    for k in vocab:
        print(k,' : ',vocab[k])





if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='python get_top10.py --path <path to directory containing .tsv files> --out <outfile>')
    parser.add_argument('-p','--path',help='path to directory containing .tsv files',required=True)
    parser.add_argument('-o','--out',help='output file name',required=True)
    args= vars(parser.parse_args())

    if os.path.isdir(args['path']):
        get_top10(args['path'],args['out'])
    else:
        print('invalid directory for tsv file corpus, exiting with code 1')
        sys.exit(1)








    


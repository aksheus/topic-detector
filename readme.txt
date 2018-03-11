##############################################################################################################################################
1) GENERAL STRATEGY

- The given topic modelling task can be approached in numerous ways. The strategy is to begin with the most basic approaches then follow them up with more complex approaches if the accuracy is not reasonable.

- The following are the strategies (in order of complexity of solution), which I have already implemented (or) plan to use for this task.

  Strategy1, Frequency based topic detection; In this strategy we identify topics based on frquency of the words (filtering away non-alphanumeric tokens) that appear on the entire corpus or a test file. We count frequencies of words by using part-of-speech tags, considering only nouns, adjectives, certain verb forms and foreign words. Moreover, we exclude stop words using an extended stop word
  initially from https://www.ranks.nl/stopwords. Note that, this file is available as "stopwords.txt" in my submission.

  Strategy 2, Bag of Topics; In this we use a bag of topics (similar to bag of words) representation for training  (say 70% of the data in 4)and testing (30% of the data in 4). The topics that make up the bag of topics matrix can be obtained using Strategy1. Although, while labeling some manual review would enhance the accuracy of the topic labels. Thus, after building a Bag of Topics representation for the training data, further feature selection (InfoGain or ChiSquare maybe attempted). The top choice of classifiers for this representaiton 
  would be NaiveBayes classifier (or) a Linear SVM. 

  Strategy3, Concise Semantic Analysis (or) Pyramidal;  Concise Semantic Analysis is a semantic analysis tehcnique that can represent each file (or) document in a space of topics. For example if we have 10 topics, a 10 dimensional feature vector would represent a single tsv file or document. The Pyramidal is an extension of Concise Semantic Analysis which can compute Concise Semantic Analysis feature vectors
  at differnt levels of granularity using k-means clustering. These two representaitons may be tested on 70-30 split and if the accuracy is
  still suffciently high we can move to strategy 4. Top choice of classifiers for this approach, Random Forest, NaiveBayes classifier, SVM and Logistic Regeression.  

  Strategy 4, Sequence to Sequence model; An LSTM based encoder and decoder which takes as input a sequence of text from a tsv file and 
  generates a topic or a shorter sequence that describes the topic.   

######################################################################################################################
2) SUBMISSION DETAILS (Time Spent: 6+ hours approximately,30 mins to extract data, code run time: )

- For this submisison, I have implemented from scratch Strategy1 for both task1 and task2.

- Requirements to run the code; The solution is implemented in Python 3.6.0 (64 bit). 

- Module Dependencies; nltk (http://www.nltk.org/) (you may need to download sub modules for pos-tagging or tokenization using nltk.download()), multiprocessing and other modules used should be available with python default installation.

- File Dependices; The code requires the stopword file, I have mentioned in Strategy1 viz "stopwords.txt"

- Code Usage,
  
  For Task1;

      Example: python get_top10.py --mode task1 --path ./ubuntu_dialogs/4  --out  ./top10from4.txt --stopw stopwords.txt

      This returns, top 10 topics in 4 in the file top10from4.txt.

      optionally, one can specify 'top' parameter.

      python get_top10.py --mode task1 --path ./ubuntu_dialogs/4  --out  ./top10from4.txt --stopw stopwords.txt --top 5

      to return top '5' (or) 'k' topics.

  For Task2;

      Example: python get_top10.py --mode task2 --path ./ubuntu_dialogs/4/3.tsv  --out  ./top10from4.txt --stopw stopwords.txt --top 3

      This returns top 3 candidates for the topic being discussed.


  General Usage,

    USAGE: python get_top10.py --mode <task1 or task2> --path <path to directory or file> --out <out file name> --stopw <path to stopwords file> [OPTIONAL] --top <top k topics default 10>


- Results for Task1,




- Results for Taks2,



- Code efficiency,

  
 




      





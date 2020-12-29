#!/usr/bin/env python3

import os
import pickle
import sys
from transformers import BertTokenizer

squad_original_path     = sys.argv[1]
tokenization_vocab_path = sys.argv[2]
tokenized_squad_path    = sys.argv[3]

# Tokenization parameters:
max_seq_length = 384
max_query_length = 64
doc_stride = 128

BERT_CODE_ROOT=os.environ['CK_ENV_MLPERF_INFERENCE']+'/language/bert'

sys.path.insert(0, BERT_CODE_ROOT)
sys.path.insert(0, BERT_CODE_ROOT + '/DeepLearningExamples/TensorFlow/LanguageModeling/BERT')

from create_squad_data import read_squad_examples, convert_examples_to_features

print("Creating the tokenizer from {} ...".format(tokenization_vocab_path))
tokenizer = BertTokenizer(tokenization_vocab_path)

print("Reading examples from {} ...".format(squad_original_path))
eval_examples = read_squad_examples(input_file=squad_original_path, is_training=False, version_2_with_negative=False)

eval_features = []
def append_feature(feature):
    eval_features.append(feature)

print("Tokenizing examples to features...")
convert_examples_to_features(
    examples=eval_examples,
    tokenizer=tokenizer,
    max_seq_length=max_seq_length,
    doc_stride=doc_stride,
    max_query_length=max_query_length,
    is_training=False,
    output_fn=append_feature,
    verbose_logging=False)

print("Recording features to {} ...".format(tokenized_squad_path))
with open(tokenized_squad_path, 'wb') as cache_file:
    pickle.dump(eval_features, cache_file)


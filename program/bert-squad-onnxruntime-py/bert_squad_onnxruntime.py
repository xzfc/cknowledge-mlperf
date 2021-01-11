#!/usr/bin/env python3

import json
import os
import pickle
import subprocess
import sys
import numpy as np
import onnxruntime

BERT_CODE_ROOT=os.environ['CK_ENV_MLPERF_INFERENCE']+'/language/bert'

sys.path.insert(0, BERT_CODE_ROOT)
sys.path.insert(0, BERT_CODE_ROOT + '/DeepLearningExamples/TensorFlow/LanguageModeling/BERT')


## SQuAD dataset - original and tokenized
#
SQUAD_DATASET_ORIGINAL_PATH     = os.environ['CK_ENV_DATASET_SQUAD_ORIGINAL']
SQUAD_DATASET_TOKENIZED_PATH    = os.environ['CK_ENV_DATASET_SQUAD_TOKENIZED']

## BERT model:
#
BERT_MODEL_PATH                 = os.environ['CK_ENV_ONNX_MODEL_ONNX_FILEPATH']

## Processing by batches:
#
BATCH_COUNT             = int(os.getenv('CK_BATCH_COUNT', 1))


sess_options = onnxruntime.SessionOptions()
print("Loading BERT model and weights from {} ...".format(BERT_MODEL_PATH))
sess = onnxruntime.InferenceSession(BERT_MODEL_PATH, sess_options)


print("Loading tokenized SQuAD dataset as features from {} ...".format(SQUAD_DATASET_TOKENIZED_PATH))
with open(SQUAD_DATASET_TOKENIZED_PATH, 'rb') as tokenized_features_file:
    eval_features = pickle.load(tokenized_features_file)

print("Example width: {}".format(len(eval_features[0].input_ids)))

TOTAL_EXAMPLES  = len(eval_features)
print("Total examples available: {}".format(TOTAL_EXAMPLES))

## Processing by batches:
#
BATCH_COUNT             = int(os.getenv('CK_BATCH_COUNT')) or TOTAL_EXAMPLES

encoded_accuracy_log = []
for i in range(BATCH_COUNT):
    selected_feature = eval_features[i]

    fd = {
        "input_ids": np.array(selected_feature.input_ids).astype(np.int64)[np.newaxis, :],
        "input_mask": np.array(selected_feature.input_mask).astype(np.int64)[np.newaxis, :],
        "segment_ids": np.array(selected_feature.segment_ids).astype(np.int64)[np.newaxis, :]
    }

    scores = sess.run([o.name for o in sess.get_outputs()], fd)
    output = np.stack(scores, axis=-1)[0]

    encoded_accuracy_log.append({'qsl_idx': i, 'data': output.tobytes().hex()})
    print("Batch #{}/{} done".format(i+1, BATCH_COUNT))


with open('accuracy_log.json', 'w') as accuracy_log_file:
    json.dump(encoded_accuracy_log, accuracy_log_file)

cmd = "python3 "+BERT_CODE_ROOT+"/accuracy-squad.py --val_data={} --features_cache_file={} --log_file=accuracy_log.json --out_file=predictions.json --max_examples={}".format(SQUAD_DATASET_ORIGINAL_PATH, SQUAD_DATASET_TOKENIZED_PATH, BATCH_COUNT)
subprocess.check_call(cmd, shell=True)

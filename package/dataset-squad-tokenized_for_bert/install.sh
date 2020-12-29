#!/bin/bash

${CK_ENV_COMPILER_PYTHON_FILE} ${PACKAGE_DIR}/tokenize_and_pickle.py ${CK_ENV_DATASET_SQUAD_ORIGINAL} ${CK_ENV_DATASET_TOKENIZATION_VOCAB} ${INSTALL_DIR}/bert_tokenized_squad_v1_1.pickle

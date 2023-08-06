# datasets
A dataset utils repository based on `tf.data`. **For tensorflow>=2.0.0b only!**

## Requirements

* python 3.6
* tensorflow>=2.0.0b

## Installation

```bash
pip install nlp-datasets
```

## Contents

* Build dataset for seq2seq models. [seq2seq_dataset.py](nlp_datasets/seq2seq/seq2seq_dataset.py)
* Build dataset for NMT. [nmt_dataset.py](nlp_datasets/nmt/nmt_dataset.py)
* Build dataset for DSSM. [dssm_dataset.py](nlp_datasets/dssm/dssm_dataset.py)
* Build dataset for MatchPyramid. [matchpyramid_dataset.py](nlp_datasets/matchpyramid/match_pyramid_dataset.py)

## Usage

### For NMT task

```python
from nlp_datasets import NMTSameFileDataset

o = NMTSameFileDataset(config=None, logger_name=None)
train_files = [] # your files
# train_dataset is an instance of tf.data.Dataset
train_dataset = o.build_train_dataset(train_files)

```

```python
from nlp_datasets import NMTSeparateFileDataset

o = NMTSeparateFileDataset(config=None, logger_name=None)
feature_files = [] # your files
label_files = []
train_dataset = o.build_train_dataset(feature_files,label_files)
```

### For DSSM task

```python
from nlp_datasets import DSSMSameFileDataset

o = DSSMSameFileDataset(config=None, logger_name=None)
train_dataset = o.build_train_dataset(train_files=[])

```

```python
from nlp_datasets import DSSMSeparateFileDataset

o = DSSMSeparateFileDataset(config=None, logger_name=None)
query_files = []
doc_files = []
label_files = []
train_dataset = o.build_train_dataset(query_files, doc_files, label_files)

```

### For MatchPyramid task

```python
from nlp_datasets import MatchPyramidSameFileDataset

o = MatchPyramidSameFileDataset(config=None, logger_name=None)
train_dataset = o.build_train_dataset(train_files=[])

```

```python
from nlp_datasets import MatchPyramidSeparateFilesDataset

o = MatchPyramidSeparateFilesDataset(config=None, logger_name=None)
query_files = []
doc_files = []
label_files = []
train_dataset = o.build_train_dataset(query_files, doc_files, label_files)

```
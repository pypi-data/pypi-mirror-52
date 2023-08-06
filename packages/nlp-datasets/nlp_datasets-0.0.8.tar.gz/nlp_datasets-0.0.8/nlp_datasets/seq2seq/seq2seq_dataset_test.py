import tensorflow as tf
from nlp_datasets import Seq2SeqSameFileDataset, Seq2SeqSeparateFileDataset
from nlp_datasets.utils import data_dir_utils

config = {
    'x_vocab_file': data_dir_utils.get_data_file('iwslt15.vocab.100.en'),
    'y_vocab_file': data_dir_utils.get_data_file('iwslt15.vocab.100.vi'),
    'share_vocab_file': False,
    'train_batch_size': 4,
    'eval_batch_size': 4,
    'predict_batch_size': 4,
    'x_max_len': 40,
    'y_max_len': 40,
}


class Seq2SeqSameFileDatasetTest(tf.test.TestCase):

    def testBuildTrainDataset(self):
        o = Seq2SeqSameFileDataset(config=config, logger_name=None)
        files = [data_dir_utils.get_data_file('iwslt15.tst2013.100.envi')]
        dataset = o.build_train_dataset(train_files=files)
        v = next(iter(dataset))
        print(v)

    def testBuildEvalDataset(self):
        o = Seq2SeqSameFileDataset(config=config, logger_name=None)
        files = [data_dir_utils.get_data_file('iwslt15.tst2013.100.envi')]
        dataset = o.build_eval_dataset(eval_files=files)
        v = next(iter(dataset))
        print(v)

    def testBuildPredictDataset(self):
        o = Seq2SeqSameFileDataset(config=config, logger_name=None)
        files = [data_dir_utils.get_data_file('iwslt15.tst2013.100.envi')]
        dataset = o.build_predict_dataset(predict_files=files)
        v = next(iter(dataset))
        print(v)


class Seq2SeqSeparateFileDatasetTest(tf.test.TestCase):

    def testBuildTrainDataset(self):
        o = Seq2SeqSeparateFileDataset(config=config, logger_name=None)
        feature_files = [data_dir_utils.get_data_file('iwslt15.tst2013.100.en')]
        label_files = [data_dir_utils.get_data_file('iwslt15.tst2013.100.vi')]
        dataset = o.build_train_dataset(feature_files, label_files)
        v = next(iter(dataset))
        print(v)

    def testBuildEvalDataset(self):
        o = Seq2SeqSeparateFileDataset(config=config, logger_name=None)
        feature_files = [data_dir_utils.get_data_file('iwslt15.tst2013.100.en')]
        label_files = [data_dir_utils.get_data_file('iwslt15.tst2013.100.vi')]
        dataset = o.build_eval_dataset(feature_files, label_files)
        v = next(iter(dataset))
        print(v)

    def testBuildPredictDataset(self):
        o = Seq2SeqSeparateFileDataset(config=config, logger_name=None)
        feature_files = [data_dir_utils.get_data_file('iwslt15.tst2013.100.en')]
        dataset = o.build_predict_dataset(feature_files)
        v = next(iter(dataset))
        print(v)


if __name__ == '__main__':
    tf.test.main()

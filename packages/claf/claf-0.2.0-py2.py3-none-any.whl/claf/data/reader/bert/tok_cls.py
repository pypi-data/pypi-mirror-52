
from itertools import chain
import json
import logging
import uuid

from overrides import overrides
from tqdm import tqdm

from claf.data.dataset import TokClsBertDataset
from claf.data.dto import BertFeature, Helper
from claf.data.reader.base import DataReader
from claf.decorator import register
from claf.tokens.tokenizer import WordTokenizer
import claf.data.utils as utils

logger = logging.getLogger(__name__)


@register("reader:tok_cls_bert")
class TokClsBertReader(DataReader):
    """
    DataReader for Token Classification using BERT

    * Args:
        file_paths: .json file paths (train and dev)
        tokenizers: define tokenizers config (subword)

    * Kwargs:
        lang_code: language code: set as 'ko' if using BERT model trained with mecab-tokenized data
        tag_key: name of the label in .json file to use for classification
        ignore_tag_idx: prediction results that have this number as ground-truth idx are ignored
    """

    def __init__(
        self,
        file_paths,
        tokenizers,
        lang_code=None,
        sequence_max_length=None,
        tag_key="tags",
        cls_token="[CLS]",
        sep_token="[SEP]",
        ignore_tag_idx=-1,
    ):

        super(TokClsBertReader, self).__init__(file_paths, TokClsBertDataset)

        self.sequence_max_length = sequence_max_length
        self.text_columns = ["bert_input", "sequence"]

        if "subword" not in tokenizers:
            raise ValueError("WordTokenizer and SubwordTokenizer is required.")

        self.subword_tokenizer = tokenizers["subword"]

        self.sent_tokenizer = tokenizers["sent"]
        self.word_tokenizer = tokenizers["word"]
        if lang_code == "ko":
            self.mecab_tokenizer = WordTokenizer("mecab_ko", self.sent_tokenizer, split_with_regex=False)

        self.lang_code = lang_code
        self.tag_key = tag_key
        self.cls_token = cls_token
        self.sep_token = sep_token
        self.ignore_tag_idx = ignore_tag_idx

    def _get_data(self, file_path):
        data = self.data_handler.read(file_path)
        tok_cls_data = json.loads(data)

        return tok_cls_data["data"]

    def _get_tag_dicts(self, **kwargs):
        data = kwargs["data"]
        print(data)

        if type(data) == dict:
            tag_idx2text = {tag_idx: tag_text for tag_idx, tag_text in enumerate(data[self.tag_key])}
        elif type(data) == list:
            tags = sorted(list(set(chain.from_iterable(d[self.tag_key] for d in data))))
            tag_idx2text = {tag_idx: tag_text for tag_idx, tag_text in enumerate(tags)}
        else:
            raise ValueError("check _get_data return type.")

        tag_text2idx = {tag_text: tag_idx for tag_idx, tag_text in tag_idx2text.items()}

        return tag_idx2text, tag_text2idx

    @overrides
    def _read(self, file_path, data_type=None):
        """
        .json file structure should be something like this:

        {
            "data": [
                {
                    "sequence": "i'm looking for a flight from New York to London.",
                    "slots": ["O", "O", "O", "O", "O", "O", "B-city.dept", "I-city.dept" "O", "B-city.dest"]
                    // the number of tokens in sequence.split() and tags must match
                },
                ...
            ],
            "slots": [  // tag_key
                "O",    // tags should be in IOB format
                "B-city.dept",
                "I-city.dept",
                "B-city.dest",
                "I-city.dest",
                ...
            ]
        }
        """

        data = self._get_data(file_path)
        tag_idx2text, tag_text2idx = self._get_tag_dicts(data=data)

        helper = Helper(**{
            "file_path": file_path,
            "tag_idx2text": tag_idx2text,
            "ignore_tag_idx": self.ignore_tag_idx,
            "cls_token": self.cls_token,
            "sep_token": self.sep_token,
        })
        helper.set_model_parameter({
            "num_tags": len(tag_idx2text),
            "ignore_tag_idx": self.ignore_tag_idx,
        })
        helper.set_predict_helper({
            "tag_idx2text": tag_idx2text,
        })

        features, labels = [], []

        for example in tqdm(data, desc=data_type):
            sequence_text = example["sequence"].strip().replace("\n", "")

            sequence_tokens = self.word_tokenizer.tokenize(sequence_text)
            naive_tokens = sequence_text.split()
            is_head_word = utils.get_is_head_of_word(naive_tokens, sequence_tokens)

            sequence_sub_tokens = []
            tagged_sub_token_idxs = []
            curr_sub_token_idx = 1  # skip CLS_TOKEN
            for token_idx, token in enumerate(sequence_tokens):
                for sub_token_pos, sub_token in enumerate(
                        self.subword_tokenizer.tokenize(token, unit="word")
                ):
                    sequence_sub_tokens.append(sub_token)
                    if is_head_word[token_idx] and sub_token_pos == 0:
                        tagged_sub_token_idxs.append(curr_sub_token_idx)
                    curr_sub_token_idx += 1

            bert_input = [self.cls_token] + sequence_sub_tokens + [self.sep_token]

            if (
                    self.sequence_max_length is not None
                    and data_type == "train"
                    and len(bert_input) > self.sequence_max_length
            ):
                continue

            if "uid" in example:
                data_uid = example["uid"]
            else:
                data_uid = str(uuid.uuid1())

            tag_texts = example[self.tag_key]
            tag_idxs = [tag_text2idx[tag_text] for tag_text in tag_texts]

            utils.sanity_check_iob(naive_tokens, tag_texts)
            assert len(naive_tokens) == len(tagged_sub_token_idxs), \
                f"""Wrong tagged_sub_token_idxs: followings mismatch.
                naive_tokens: {naive_tokens}
                sequence_sub_tokens: {sequence_sub_tokens}
                tagged_sub_token_idxs: {tagged_sub_token_idxs}"""

            feature_row = {
                "id": data_uid,
                "bert_input": bert_input,
                "tagged_sub_token_idxs": tagged_sub_token_idxs,
                "num_tokens": len(naive_tokens),
            }
            features.append(feature_row)

            label_row = {
                "id": data_uid,
                "tag_idxs": tag_idxs,
                "tag_texts": tag_texts,
            }
            labels.append(label_row)

            helper.set_example(data_uid, {
                "sequence": sequence_text,
                "sequence_sub_tokens": sequence_sub_tokens,
                "tag_idxs": tag_idxs,
                "tag_texts": tag_texts,
            })

        return utils.make_batch(features, labels), helper.to_dict()

    def read_one_example(self, inputs):
        """ inputs keys: sequence """
        sequence_text = inputs["sequence"].strip().replace("\n", "")
        sequence_tokens = self.word_tokenizer.tokenize(sequence_text)
        naive_tokens = sequence_text.split()
        is_head_word = utils.get_is_head_of_word(naive_tokens, sequence_tokens)

        sequence_sub_tokens = []
        tagged_sub_token_idxs = []
        curr_sub_token_idx = 1  # skip CLS_TOKEN
        for token_idx, token in enumerate(sequence_tokens):
            for sub_token_pos, sub_token in enumerate(
                    self.subword_tokenizer.tokenize(token, unit="word")
            ):
                sequence_sub_tokens.append(sub_token)
                if is_head_word[token_idx] and sub_token_pos == 0:
                    tagged_sub_token_idxs.append(curr_sub_token_idx)
                curr_sub_token_idx += 1

        if len(sequence_sub_tokens) > self.sequence_max_length:
            sequence_sub_tokens = sequence_sub_tokens[:self.sequence_max_length]

        bert_input = [self.cls_token] + sequence_sub_tokens + [self.sep_token]
        assert len(naive_tokens) == len(tagged_sub_token_idxs), \
            f"""Wrong tagged_sub_token_idxs: followings mismatch.
            naive_tokens: {naive_tokens}
            sequence_sub_tokens: {sequence_sub_tokens}
            tagged_sub_token_idxs: {tagged_sub_token_idxs}"""

        bert_feature = BertFeature()
        bert_feature.set_input(bert_input)
        bert_feature.set_feature("tagged_sub_token_idxs", tagged_sub_token_idxs)
        bert_feature.set_feature("num_tokens", len(naive_tokens))

        features = [bert_feature.to_dict()]
        helper = {}
        return features, helper

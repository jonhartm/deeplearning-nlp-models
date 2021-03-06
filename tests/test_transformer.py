from argparse import Namespace

import torch
import numpy as np
from nlpmodels.models import transformer
from nlpmodels.utils import utils
from nlpmodels.utils.elt.transformer_batch import TransformerBatch
from nlpmodels.utils.elt.transformer_dataset import TransformerDataset
from nlpmodels.utils.vocabulary import NLPVocabulary
from tests.test_data import transformer_regression_test_data

utils.set_seed_everywhere()


def test_input_output_dims_transformer():
    test_1_args = Namespace(
        num_layers_per_stack=2,
        dim_model=512,
        dim_ffn=2048,
        num_heads=8,
        max_sequence_length=20,
        dropout=0.1,
    )

    # mock dataset
    src_tokens = [["the", "cow", "jumped", "over", "the", "moon"], ["the", "british", "are", "coming"]]
    tgt_tokens = [["la", "vache", "a", "sauté", "sur", "la", "lune"], ["les", "britanniques", "arrivent"]]
    batch_size = len(src_tokens)
    dictionary_source = NLPVocabulary.build_vocabulary(src_tokens)
    dictionary_target = NLPVocabulary.build_vocabulary(tgt_tokens)
    max_seq_length = 20
    src_padded = TransformerDataset.padded_string_to_integer(src_tokens, max_seq_length, dictionary_source)
    tgt_padded = TransformerDataset.padded_string_to_integer(tgt_tokens, max_seq_length + 1, dictionary_target)
    data = TransformerBatch(torch.LongTensor(src_padded), torch.LongTensor(tgt_padded))

    model = transformer.Transformer(len(dictionary_source), len(dictionary_target),
                                    test_1_args.num_layers_per_stack, test_1_args.dim_model,
                                    test_1_args.dim_ffn, test_1_args.num_heads, test_1_args.max_sequence_length,
                                    test_1_args.dropout)
    # push through model
    y_hat = model(data)

    # assert all dimensions are correct
    assert y_hat.size() == torch.Size([batch_size, max_seq_length, len(dictionary_target)])


def test_transformer_regression_test():
    utils.set_seed_everywhere()

    test_2_args = Namespace(
        num_layers_per_stack=2,
        dim_model=512,
        dim_ffn=2048,
        num_heads=8,
        max_sequence_length=20,
        dropout=0.1,
    )

    # mock dataset
    src_tokens = [["the", "cow", "jumped", "over", "the", "moon"], ["the", "british", "are", "coming"]]
    tgt_tokens = [["la", "vache", "a", "sauté", "sur", "la", "lune"], ["les", "britanniques", "arrivent"]]
    batch_size = len(src_tokens)
    dictionary_source = NLPVocabulary.build_vocabulary(src_tokens)
    dictionary_target = NLPVocabulary.build_vocabulary(tgt_tokens)
    max_seq_length = 20
    src_padded = TransformerDataset.padded_string_to_integer(src_tokens, max_seq_length, dictionary_source)
    tgt_padded = TransformerDataset.padded_string_to_integer(tgt_tokens, max_seq_length + 1, dictionary_target)
    data = TransformerBatch(torch.LongTensor(src_padded), torch.LongTensor(tgt_padded))

    model = transformer.Transformer(len(dictionary_source), len(dictionary_target),
                                    test_2_args.num_layers_per_stack, test_2_args.dim_model,
                                    test_2_args.dim_ffn, test_2_args.num_heads, test_2_args.max_sequence_length,
                                    test_2_args.dropout)
    # push through model
    y_hat = model(data)

    # expected output
    expected_output = transformer_regression_test_data.TRANSFORMER_REGRESSION_TEST_DATA

    # assert y_hat is within eps
    eps = 1.e-4
    assert np.allclose(y_hat.data.numpy(),expected_output.data.numpy(),atol=eps)
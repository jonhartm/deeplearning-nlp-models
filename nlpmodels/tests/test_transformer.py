from argparse import Namespace

import torch

from nlpmodels.models import transformer
from nlpmodels.utils import utils
from nlpmodels.utils.transformer_batch import TransformerBatch
from nlpmodels.utils.transformer_dataset import TransformerDataset
from nlpmodels.utils.vocabulary import NLPVocabulary

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
    yhat = model(data)

    # assert all dimensions are correct
    assert yhat.size() == torch.Size([batch_size, max_seq_length, len(dictionary_target)])


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
    yhat = model(data)

    # expected output
    expected_output = torch.Tensor([[[-2.9239, -3.0313, -3.5501, -2.3190, -1.1354, -2.9546, -2.5074,
          -2.8956, -3.1165, -2.1859, -2.6988, -3.3016],
         [-3.1632, -3.8270, -5.1175, -2.4648, -1.7739, -3.3248, -2.8746,
          -3.4151, -1.7133, -1.1062, -4.1403, -3.7738],
         [-3.4400, -4.3049, -1.7217, -3.9367, -1.0017, -2.2071, -3.8026,
          -4.1094, -2.3040, -2.2851, -3.7249, -4.2399],
         [-2.5877, -3.9502, -0.8627, -4.6694, -3.9749, -2.5659, -2.0790,
          -4.6141, -3.0293, -4.5241, -3.5600, -1.8584],
         [-4.3508, -4.2324, -1.8769, -3.4398, -1.5268, -4.5950, -2.6446,
          -3.6029, -2.4466, -1.7450, -3.8045, -1.7240],
         [-3.9353, -5.2104, -2.4906, -4.5325, -0.6086, -4.2718, -3.0106,
          -4.8917, -2.1567, -2.4628, -3.0864, -3.9122],
         [-3.8348, -3.5088, -1.8010, -4.6549, -2.8974, -2.6019, -1.4641,
          -4.4027, -3.7338, -1.2373, -3.6075, -2.8167],
         [-1.8728, -4.7085, -1.4622, -4.1130, -2.8933, -3.0699, -3.2775,
          -2.8059, -1.3429, -3.0821, -3.2599, -3.1264],
         [-2.0073, -5.3930, -1.9061, -3.4231, -4.1645, -1.5840, -2.9792,
          -3.4363, -1.1419, -5.3801, -3.1119, -4.8544],
         [-3.2074, -3.7399, -2.1039, -3.1192, -2.2490, -1.3365, -2.7134,
          -3.5299, -1.5717, -4.5555, -2.7116, -3.8586],
         [-2.6946, -3.5952, -1.1298, -3.9398, -2.6815, -2.3307, -4.0139,
          -3.8650, -1.4706, -3.6004, -2.4606, -4.1851],
         [-2.3360, -3.9403, -1.2158, -3.6496, -2.2116, -1.8024, -3.4826,
          -3.7037, -1.9094, -4.1599, -3.3624, -3.4067],
         [-2.0999, -3.9276, -1.2130, -3.2125, -1.9515, -2.5389, -2.5068,
          -3.9009, -2.3423, -3.7957, -2.8818, -3.7761],
         [-2.3619, -4.8862, -1.4032, -2.8835, -1.6687, -2.3101, -2.5548,
          -3.8520, -2.1029, -4.3414, -2.8687, -4.0240],
         [-1.2596, -4.0080, -2.0702, -3.0414, -2.6494, -2.1748, -2.9956,
          -2.3270, -2.2846, -4.2341, -2.8791, -3.9258],
         [-1.6545, -4.0814, -1.7632, -2.4270, -2.9824, -2.5345, -2.3063,
          -2.6240, -2.9446, -4.1576, -1.9793, -3.7475],
         [-0.8145, -3.9420, -2.5351, -3.0704, -2.7000, -2.2468, -3.3338,
          -3.1874, -2.4478, -4.8542, -3.0867, -3.8044],
         [-1.5094, -4.7853, -1.5760, -2.5996, -2.4378, -2.1664, -2.7609,
          -2.9881, -2.6952, -5.1288, -2.5066, -3.9666],
         [-2.0000, -3.9240, -1.4003, -3.8221, -2.7622, -1.8955, -2.8787,
          -2.9941, -1.7925, -4.2836, -2.7761, -4.2542],
         [-1.8216, -4.4362, -2.3624, -3.8346, -1.9357, -1.9645, -3.5151,
          -3.0095, -1.3315, -5.1505, -2.8617, -3.9148]],

        [[-3.3985, -3.7812, -0.4188, -3.2434, -4.2522, -3.1153, -2.8882,
          -5.9206, -4.3718, -4.2785, -2.6291, -3.4640],
         [-3.8380, -5.7278, -2.1378, -4.1021, -1.0834, -2.7728, -2.2876,
          -3.1935, -1.9287, -2.3167, -3.9948, -3.3540],
         [-1.9320, -6.4220, -0.8643, -4.7937, -2.6015, -4.5861, -4.0554,
          -4.5680, -4.5610, -2.9979, -1.3905, -5.9735],
         [-1.4687, -4.4103, -1.1099, -5.7462, -3.0261, -2.8311, -3.5447,
          -2.5581, -2.2672, -3.3228, -2.9054, -4.0944],
         [-0.5911, -5.1786, -3.5985, -4.7522, -4.0430, -1.7134, -3.5862,
          -5.5942, -1.9912, -5.4364, -3.6746, -4.6915],
         [-1.5844, -3.8936, -2.6901, -5.7817, -3.8275, -2.6756, -4.1031,
          -5.4935, -0.6688, -5.7448, -2.6226, -5.4694],
         [-0.8441, -4.1828, -2.7606, -5.1270, -3.1621, -2.5738, -3.4191,
          -5.2580, -1.4045, -3.7512, -2.9957, -4.5957],
         [-1.8972, -5.3261, -2.2415, -5.5923, -3.1253, -1.6715, -3.6321,
          -5.3732, -0.8798, -4.6987, -3.1154, -5.5723],
         [-1.5157, -3.8336, -3.5379, -4.4303, -3.5435, -2.0670, -3.6318,
          -5.7571, -1.0149, -5.2859, -1.8934, -4.2290],
         [-0.8497, -3.6478, -2.7997, -5.9485, -4.5742, -2.5902, -3.3631,
          -6.0378, -1.1376, -4.8931, -3.5002, -6.0591],
         [-1.9139, -5.3948, -3.7368, -5.1225, -3.8849, -0.9651, -4.0904,
          -5.9707, -1.0651, -4.3243, -3.5740, -4.4724],
         [-1.8270, -3.6221, -3.3599, -5.0632, -3.4828, -1.4305, -4.6899,
          -5.0103, -0.8898, -4.3562, -3.0336, -4.2811],
         [-1.0371, -5.5679, -2.7376, -5.0572, -3.9901, -1.9739, -4.0914,
          -5.1973, -1.1289, -5.2799, -2.9083, -4.8408],
         [-0.5162, -5.0408, -2.6849, -5.3081, -3.7309, -1.7947, -4.1349,
          -5.8153, -2.9863, -4.9595, -3.0901, -4.4715],
         [-1.7721, -4.6433, -2.7994, -6.1504, -4.1309, -1.9485, -3.4544,
          -6.0191, -0.6169, -4.4192, -4.6506, -5.6172],
         [-0.9674, -4.4105, -2.3811, -4.9998, -2.3014, -2.1747, -3.1688,
          -4.8304, -1.7029, -4.5403, -3.2177, -4.4303],
         [-0.9880, -4.1529, -2.5196, -3.8929, -3.2760, -1.4661, -4.1671,
          -6.2883, -1.7974, -4.6105, -3.3974, -4.1371],
         [-1.8392, -3.0553, -1.4823, -4.3767, -2.9767, -1.1398, -3.8008,
          -5.8905, -2.4552, -4.6033, -2.9139, -4.8050],
         [-1.1508, -5.0757, -2.8698, -4.6655, -3.1916, -1.6274, -4.5214,
          -4.8847, -1.2395, -5.0154, -2.9068, -5.4170],
         [-0.5747, -4.9462, -3.4027, -5.5209, -3.5246, -1.8115, -4.2710,
          -5.1074, -2.1169, -5.2213, -3.1305, -4.5721]]])

    # assert yhat is within eps
    eps = 1.e-3
    assert torch.sum(yhat - expected_output).data.numpy() < eps
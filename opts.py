import argparse
from onmt.modules.SRU import CheckSRU
from onmt.Utils import MODEL_TYPES


def model_opts(parser):
    """
    These options are passed to the construction of the model.
    Be careful with these as they will be used during translation.
    """

    # Embedding Options
    group = parser.add_argument_group('Model-Embeddings')
    group.add_argument('-src_word_vec_size', type=int, default=500,
                       help='Word embedding size for src.')
    group.add_argument('-tgt_word_vec_size', type=int, default=500,
                       help='Word embedding size for tgt.')
    group.add_argument('-word_vec_size', type=int, default=-1,
                       help='Word embedding size for src and tgt.')

    group.add_argument('-share_decoder_embeddings', action='store_true',
                       help="""Use a shared weight matrix for the input and
                       output word  embeddings in the decoder.""")
    group.add_argument('-share_embeddings', action='store_true',
                       help="""Share the word embeddings between encoder
                       and decoder. Need to use shared dictionary for this
                       option.""")
    group.add_argument('-position_encoding', action='store_true',
                       help="""Use a sin to mark relative words positions.
                       Necessary for non-RNN style models.
                       """)

    group = parser.add_argument_group('Model-Embedding Features')
    group.add_argument('-feat_merge', type=str, default='concat',
                       choices=['concat', 'sum', 'mlp'],
                       help="""Merge action for incorporating features embeddings.
                       Options [concat|sum|mlp].""")
    group.add_argument('-feat_vec_size', type=int, default=-1,
                       help="""If specified, feature embedding sizes
                       will be set to this. Otherwise, feat_vec_exponent
                       will be used.""")
    group.add_argument('-feat_vec_exponent', type=float, default=0.7,
                       help="""If -feat_merge_size is not set, feature
                       embedding sizes will be set to N^feat_vec_exponent
                       where N is the number of values the feature takes.""")

    # Encoder-Deocder Options
    group = parser.add_argument_group('Model- Encoder-Decoder')
    group.add_argument('-model_type', default='text',
                       help="""Type of source model to use. Allows
                       the system to incorporate non-text inputs.
                       Options are [text|img|audio].""")

    group.add_argument('-encoder_type', type=str, default='rnn',
                       choices=['rnn', 'brnn', 'mean', 'transformer', 'cnn'],
                       help="""Type of encoder layer to use. Non-RNN layers
                       are experimental. Options are
                       [rnn|brnn|mean|transformer|cnn].""")
    group.add_argument('-decoder_type', type=str, default='rnn',
                       choices=['rnn', 'transformer', 'cnn', 'doubly-attentive-rnn'],
                       help="""Type of decoder layer to use. Non-RNN layers
                       are experimental. Options are
                       [rnn|transformer|cnn|doubly-attentive-rnn].""")

    group.add_argument('-layers', type=int, default=-1,
                       help='Number of layers in enc/dec.')
    group.add_argument('-enc_layers', type=int, default=2,
                       help='Number of layers in the encoder')
    group.add_argument('-dec_layers', type=int, default=2,
                       help='Number of layers in the decoder')
    group.add_argument('-rnn_size', type=int, default=500,
                       help='Size of rnn hidden states')
    group.add_argument('-cnn_kernel_width', type=int, default=3,
                       help="""Size of windows in the cnn, the kernel_size is
                       (cnn_kernel_width, 1) in conv layer""")

    group.add_argument('-input_feed', type=int, default=1,
                       help="""Feed the context vector at each time step as
                       additional input (via concatenation with the word
                       embeddings) to the decoder.""")

    group.add_argument('-rnn_type', type=str, default='LSTM',
                       choices=['LSTM', 'GRU', 'SRU'],
                       action=CheckSRU,
                       help="""The gate type to use in the RNNs""")
    # group.add_argument('-residual',   action="store_true",
    #                     help="Add residual connections between RNN layers.")

    group.add_argument('-brnn', action=DeprecateAction,
                       help="Deprecated, use `encoder_type`.")
    group.add_argument('-brnn_merge', default='concat',
                       choices=['concat', 'sum'],
                       help="Merge action for the bidir hidden states")

    group.add_argument('-context_gate', type=str, default=None,
                       choices=['source', 'target', 'both'],
                       help="""Type of context gate to use.
                       Do not select for no context gate.""")

    # Attention options
    group = parser.add_argument_group('Model- Attention')
    group.add_argument('-global_attention', type=str, default='general',
                       choices=['dot', 'general', 'mlp'],
                       help="""The attention type to use:
                       dotprod or general (Luong) or MLP (Bahdanau)""")

    # Genenerator and loss options.
    group.add_argument('-copy_attn', action="store_true",
                       help='Train copy attention layer.')
    group.add_argument('-copy_attn_force', action="store_true",
                       help='When available, train to copy.')
    group.add_argument('-reuse_copy_attn', action="store_true",
                       help="Reuse standard attention for copy")
    group.add_argument('-coverage_attn', action="store_true",
                       help='Train a coverage attention layer.')
    group.add_argument('-lambda_coverage', type=float, default=1,
                       help='Lambda value for coverage.')


def preprocess_opts(parser):
    # Data options
    group = parser.add_argument_group('Data')
    group.add_argument('-data_type', default="text",
                       help="""Type of the source input.
                       Options are [text|img].""")

    group.add_argument('-train_src', required=True,
                       help="Path to the training source data")
    group.add_argument('-train_tgt', required=True,
                       help="Path to the training target data")
    group.add_argument('-valid_src', required=True,
                       help="Path to the validation source data")
    group.add_argument('-valid_tgt', required=True,
                       help="Path to the validation target data")

    group.add_argument('-src_dir', default="",
                       help="Source directory for image or audio files.")

    group.add_argument('-save_data', required=True,
                       help="Output file for the prepared data")

    group.add_argument('-max_shard_size', type=int, default=0,
                       help="""For text corpus of large volume, it will
                       be divided into shards of this size to preprocess.
                       If 0, the data will be handled as a whole. The unit
                       is in bytes. Optimal value should be multiples of
                       64 bytes.""")

    # Dictionary options, for text corpus

    group = parser.add_argument_group('Vocab')
    group.add_argument('-src_vocab', default="",
                       help="""Path to an existing source vocabulary. Format: one word per line.""")
    group.add_argument('-tgt_vocab', default="",
                       help="""Path to an existing target vocabulary. Format: one word per line.""")
    group.add_argument('-features_vocabs_prefix', type=str, default='',
                       help="Path prefix to existing features vocabularies")
    group.add_argument('-src_vocab_size', type=int, default=50000,
                       help="Size of the source vocabulary")
    group.add_argument('-tgt_vocab_size', type=int, default=50000,
                       help="Size of the target vocabulary")

    group.add_argument('-src_words_min_frequency', type=int, default=0)
    group.add_argument('-tgt_words_min_frequency', type=int, default=0)

    group.add_argument('-dynamic_dict', action='store_true',
                       help="Create dynamic dictionaries")
    group.add_argument('-share_vocab', action='store_true',
                       help="Share source and target vocabulary")

    # Truncation options, for text corpus
    group = parser.add_argument_group('Pruning')
    group.add_argument('-src_seq_length', type=int, default=50,
                       help="Maximum source sequence length")
    group.add_argument('-src_seq_length_trunc', type=int, default=0,
                       help="Truncate source sequence length.")
    group.add_argument('-tgt_seq_length', type=int, default=50,
                       help="Maximum target sequence length to keep.")
    group.add_argument('-tgt_seq_length_trunc', type=int, default=0,
                       help="Truncate target sequence length.")
    group.add_argument('-lower', action='store_true', help='lowercase data')

    # Data processing options
    group = parser.add_argument_group('Random')
    group.add_argument('-shuffle', type=int, default=1,
                       help="Shuffle data")
    group.add_argument('-seed', type=int, default=3435,
                       help="Random seed")

    group = parser.add_argument_group('Logging')
    group.add_argument('-report_every', type=int, default=100000,
                       help="Report status every this many sentences")

    # Options most relevant to speech
    group = parser.add_argument_group('Speech')
    group.add_argument('-sample_rate', type=int, default=16000,
                       help="Sample rate.")
    group.add_argument('-window_size', type=float, default=.02,
                       help="Window size for spectrogram in seconds.")
    group.add_argument('-window_stride', type=float, default=.01,
                       help="Window stride for spectrogram in seconds.")
    group.add_argument('-window', default='hamming',
                       help="Window type for spectrogram generation.")


def train_opts(parser):
    # Model loading/saving options

    group = parser.add_argument_group('General')
    group.add_argument('-data', required=True,
                       help="""Path prefix to the ".train.pt" and
                       ".valid.pt" file path from preprocess.py""")

    group.add_argument('-save_model', default='model',
                       help="""Model filename (the model will be saved as
                       <save_model>_epochN_PPL.pt where PPL is the
                       validation perplexity""")
    # GPU
    group.add_argument('-gpuid', default=[], nargs='+', type=int,
                       help="Use CUDA on the listed devices.")

    group.add_argument('-seed', type=int, default=-1,
                       help="""Random seed used for the experiments
                       reproducibility.""")

    # Early stopping
    group = parser.add_argument_group('Early stopping')
    group.add_argument('-early_stopping_criteria', required=False, choices=['perplexity', 'bleu', 'meteor'], type=str, default='perplexity',
                       help='Early stopping criteria, one of : [\'perplexity\', \'bleu\', \'meteor\']. Defaults to \'perplexity\'.')
    group.add_argument('-src',   required=False, type=str,
                       help="""Source (validation) sequence to decode (one line per sequence)""")
    group.add_argument('-tgt',   required=False, type=str,
                       help='True target (validation) sequence')
    group.add_argument('-evaluate_every_n_model_updates', default=500, type=int,
                       help='Evaluate model at every \'n\' model updates.')
    group.add_argument('-patience', default=20, type=int,
                       help='Early stop in case model did not improve on the validation set for more than dictated by patience.')
    group.add_argument('-beam_size',  type=int, default=1,
                       help='Beam size')
    group.add_argument('-start_early_stopping_at', default=0, type=int,
                       help='Start evaluations for early stopping after \'n\' model updates.')
    group.add_argument('-overwrite_model_file', action="store_true", required=False,
                       help='Whether to overwrite the saved model file (only save last/best one) or to store a checkpoint for every saved model.')

    # Init options
    group = parser.add_argument_group('Initialization')
    group.add_argument('-start_epoch', type=int, default=1,
                       help='The epoch from which to start')
    group.add_argument('-param_init', type=float, default=0.1,
                       help="""Parameters are initialized over uniform distribution
                       with support (-param_init, param_init).
                       Use 0 to not use initialization""")
    group.add_argument('-train_from', default='', type=str,
                       help="""If training from a checkpoint then this is the
                       path to the pretrained model's state_dict.""")
    group.add_argument('-finetune', action='store_true', required=False,
                       help="""Fine-tuning flag. If set to True, optimiser will be created from scratch.""")

    # Pretrained word vectors
    group.add_argument('-pre_word_vecs_enc',
                       help="""If a valid path is specified, then this will load
                       pretrained word embeddings on the encoder side.
                       See README for specific formatting instructions.""")
    group.add_argument('-pre_word_vecs_dec',
                       help="""If a valid path is specified, then this will load
                       pretrained word embeddings on the decoder side.
                       See README for specific formatting instructions.""")
    # Fixed word vectors
    group.add_argument('-fix_word_vecs_enc',
                       action='store_true',
                       help="Fix word embeddings on the encoder side.")
    group.add_argument('-fix_word_vecs_dec',
                       action='store_true',
                       help="Fix word embeddings on the encoder side.")

    # Optimization options
    group = parser.add_argument_group('Optimization- Type')
    group.add_argument('-batch_size', type=int, default=64,
                       help='Maximum batch size for training')
    group.add_argument('-batch_type', default='sents',
                       choices=["sents", "tokens"],
                       help="""Batch grouping for batch_size. Standard
                               is sents. Tokens will do dynamic batching""")
    group.add_argument('-normalization', default='sents',
                       choices=["sents", "tokens"],
                       help='Normalization method of the gradient.')
    group.add_argument('-accum_count', type=int, default=1,
                       help="""Accumulate gradient this many times.
                       Approximately equivalent to updating
                       batch_size * accum_count batches at once.
                       Recommended for Transformer.""")
    group.add_argument('-valid_batch_size', type=int, default=32,
                       help='Maximum batch size for validation')
    group.add_argument('-max_generator_batches', type=int, default=32,
                       help="""Maximum batches of words in a sequence to run
                        the generator on in parallel. Higher is faster, but
                        uses more memory.""")
    group.add_argument('-epochs', type=int, default=13,
                       help='Number of training epochs')
    group.add_argument('-optim', default='sgd',
                       choices=['sgd', 'adagrad', 'adadelta', 'adam'],
                       help="""Optimization method.""")
    group.add_argument('-adagrad_accumulator_init', type=float, default=0,
                       help="""Initializes the accumulator values in adagrad.
                       Mirrors the initial_accumulator_value option
                       in the tensorflow adagrad (use 0.1 for their default).
                       """)
    group.add_argument('-max_grad_norm', type=float, default=5,
                       help="""If the norm of the gradient vector exceeds this,
                       renormalize it to have the norm equal to
                       max_grad_norm""")
    group.add_argument('-dropout', type=float, default=0.3,
                       help="Dropout probability; applied in LSTM stacks.")
    group.add_argument('-word_dropout', type=float, default=0.0,
                       help="Word dropout probability; applied to source and target word embeddings.")
    group.add_argument('-truncated_decoder', type=int, default=0,
                       help="""Truncated bptt.""")
    group.add_argument('-adam_beta1', type=float, default=0.9,
                       help="""The beta1 parameter used by Adam.
                       Almost without exception a value of 0.9 is used in
                       the literature, seemingly giving good results,
                       so we would discourage changing this value from
                       the default without due consideration.""")
    group.add_argument('-adam_beta2', type=float, default=0.999,
                       help="""The beta2 parameter used by Adam.
                       Typically a value of 0.999 is recommended, as this is
                       the value suggested by the original paper describing
                       Adam, and is also the value adopted in other frameworks
                       such as Tensorflow and Kerras, i.e. see:
                       https://www.tensorflow.org/api_docs/python/tf/train/AdamOptimizer
                       https://keras.io/optimizers/ .
                       Whereas recently the paper "Attention is All You Need"
                       suggested a value of 0.98 for beta2, this parameter may
                       not work well for normal models / default
                       baselines.""")
    group.add_argument('-label_smoothing', type=float, default=0.0,
                       help="""Label smoothing value epsilon.
                       Probabilities of all non-true labels
                       will be smoothed by epsilon / (vocab_size - 1).
                       Set to zero to turn off label smoothing.
                       For more detailed information, see:
                       https://arxiv.org/abs/1512.00567""")
    # learning rate
    group = parser.add_argument_group('Optimization- Rate')
    group.add_argument('-learning_rate', type=float, default=1.0,
                       help="""Starting learning rate.
                       Recommended settings: sgd = 1, adagrad = 0.1,
                       adadelta = 1, adam = 0.001""")
    group.add_argument('-learning_rate_decay', type=float, default=0.5,
                       help="""If update_learning_rate, decay learning rate by
                       this much if (i) perplexity does not decrease on the
                       validation set or (ii) epoch has gone past
                       start_decay_at""")
    group.add_argument('-start_decay_at', type=int, default=8,
                       help="""Start decaying every epoch after and including this
                       epoch""")
    group.add_argument('-start_checkpoint_at', type=int, default=0,
                       help="""Start checkpointing every epoch after and including
                       this epoch""")
    group.add_argument('-decay_method', type=str, default="",
                       choices=['noam'], help="Use a custom decay rate.")
    group.add_argument('-warmup_steps', type=int, default=4000,
                       help="""Number of warmup steps for custom decay.""")

    group = parser.add_argument_group('Logging')
    group.add_argument('-report_every', type=int, default=50,
                       help="Print stats at this interval.")
    group.add_argument('-exp_host', type=str, default="",
                       help="Send logs to this crayon server.")
    group.add_argument('-exp', type=str, default="",
                       help="Name of the experiment for logging.")

    group = parser.add_argument_group('Speech')
    # Options most relevant to speech
    group.add_argument('-sample_rate', type=int, default=16000,
                       help="Sample rate.")
    group.add_argument('-window_size', type=float, default=.02,
                       help="Window size for spectrogram in seconds.")


def translate_opts(parser):
    group = parser.add_argument_group('Model')
    group.add_argument('-model', required=True,
                       help='Path to model .pt file')

    group = parser.add_argument_group('Data')
    group.add_argument('-data_type', default="text",
                       help="Type of the source input. Options: [text|img].")

    group.add_argument('-src',   required=True,
                       help="""Source sequence to decode (one line per
                       sequence)""")
    group.add_argument('-src_dir',   default="",
                       help='Source directory for image or audio files')
    group.add_argument('-tgt',
                       help='True target sequence (optional)')
    group.add_argument('-output', default='pred.txt',
                       help="""Path to output the predictions (each line will
                       be the decoded sequence""")
    group.add_argument('-report_bleu', action='store_true',
                       help="""Report bleu score after translation,
                       call tools/multi-bleu.perl on command line""")
    group.add_argument('-report_rouge', action='store_true',
                       help="""Report rouge 1/2/3/L/SU4 score after translation
                       call tools/test_rouge.py on command line""")

    # Options most relevant to summarization.
    group.add_argument('-dynamic_dict', action='store_true',
                       help="Create dynamic dictionaries")
    group.add_argument('-share_vocab', action='store_true',
                       help="Share source and target vocabulary")

    group = parser.add_argument_group('Beam')
    group.add_argument('-beam_size',  type=int, default=5,
                       help='Beam size')
    group.add_argument('-min_length', type=int, default=0,
                       help='Minimum prediction length')
    group.add_argument('-max_length', type=int, default=100,
                       help='Maximum prediction length.')
    group.add_argument('-max_sent_length', action=DeprecateAction,
                       help="Deprecated, use `-max_length` instead")

    # Alpha and Beta values for Google Length + Coverage penalty
    # Described here: https://arxiv.org/pdf/1609.08144.pdf, Section 7
    group.add_argument('-alpha', type=float, default=0.,
                       help="""Google NMT length penalty parameter
                        (higher = longer generation)""")
    group.add_argument('-beta', type=float, default=-0.,
                       help="""Coverage penalty parameter""")
    group.add_argument('-replace_unk', action="store_true",
                       help="""Replace the generated UNK tokens with the
                       source token that had highest attention weight. If
                       phrase_table is provided, it will lookup the
                       identified source token and give the corresponding
                       target token. If it is not provided(or the identified
                       source token does not exist in the table) then it
                       will copy the source token""")

    group = parser.add_argument_group('Logging')
    group.add_argument('-verbose', action="store_true",
                       help='Print scores and predictions for each sentence')
    group.add_argument('-attn_debug', action="store_true",
                       help='Print best attn for each word')
    group.add_argument('-dump_beam', type=str, default="",
                       help='File to dump beam information to.')
    group.add_argument('-n_best', type=int, default=1,
                       help="""If verbose is set, will output the n_best
                       decoded sentences""")

    group = parser.add_argument_group('Efficiency')
    group.add_argument('-batch_size', type=int, default=30,
                       help='Batch size')
    group.add_argument('-gpu', type=int, default=-1,
                       help="Device to run on")

    # Options most relevant to speech.
    group = parser.add_argument_group('Speech')
    group.add_argument('-sample_rate', type=int, default=16000,
                       help="Sample rate.")
    group.add_argument('-window_size', type=float, default=.02,
                       help='Window size for spectrogram in seconds')
    group.add_argument('-window_stride', type=float, default=.01,
                       help='Window stride for spectrogram in seconds')
    group.add_argument('-window', default='hamming',
                       help='Window type for spectrogram generation')


def add_md_help_argument(parser):
    parser.add_argument('-md', action=MarkdownHelpAction,
                        help='print Markdown-formatted help text and exit.')


#####################################################################
# Variational multi-modal NMT command-line parameters
#####################################################################

def _train_mm_vi_opts(parser):
    """Hyperparameters common to all VI models."""
    parser.add_argument('-path_to_train_img_feats', required=True,
                        help="""Path to hdf5 file containing training image features""")
    parser.add_argument('-path_to_valid_img_feats', required=True,
                        help="""Path to hdf5 file containing validation image features""")
    parser.add_argument('-dropout_imgs', type=float, default=0.5,
                        help="Dropout probability applied to image features.")
    parser.add_argument('--multimodal_model_type', required=True, type=str,
                        choices=MODEL_TYPES, default='vi-model1',
                        help="""Variational multi-modal NMT model type. For details, check `onmt/VI_ModelX.py`.""")
    parser.add_argument('--z_latent_dim', required=True,
			type=int, help="""Dimensionality of the latent variables Z.""")
    parser.add_argument('--use_standardised_image_features', required=False, action='store_true',
                        help="""Use standardised image features? `std_feat = (orig_feat - mean) / variance` """)
    parser.add_argument('-path_to_mean_train_img_feats', required=False,
                        help="""Path to hdf5 file containing the mean training image features. Must be set in case --use_standardised_image_features is being used.""")
    parser.add_argument('-path_to_std_train_img_feats', required=False,
                        help="""Path to hdf5 file containing the standard deviation of the training image features. Must be set in case --use_standardised_image_features is being used.""")
    parser.add_argument('--conditional', required=False,
			action='store_true', help="""Whether we are using a conditional or fixed prior. If using a conditional prior, we also use additional features to predict Z.""")
    parser.add_argument('--use_kl_annealing', required=False, action='store_true',
                        help="""Whether to use KL annealing or not. Defaults to False.""")
    parser.add_argument('--use_kl_freebits', required=False, action='store_true',
                        help="""Whether to use free-bits to clamp the KL above a minimum (larger than 0.) or not. Defaults to False.""")
    parser.add_argument('--kl_freebits_margin', required=False, type=float, default=0.0,
                        help="""KL free-bits margin. Used when applying KL free-bits. Defaults to 0.0""")
    parser.add_argument('--kl_annealing_warmup_steps', required=False, type=int, default=500,
                        help="""Number of initial model updates without incrementing the KL. Used when applying KL annealing. Defaults to 500""")
    parser.add_argument('--kl_annealing_start', required=False, type=float, default=0.0,
                        help="""KL starting value. Used when applying KL annealing. Defaults to 0.0""")
    parser.add_argument('--kl_annealing_increment', required=False, type=float, default=0.0001,
                        help="""KL increment added to the KL multiplier at each mini-batch. Used when applying KL annealing. Defaults to 0.0001""")
    parser.add_argument('--image_loss', required=False, type=str, default='logprob',
                        choices=['cosine', 'logprob', 'categorical', 'none'], help="""How to compute the image loss. Use cosine distance ('cosine') or log probability ('logprob') to predict image features. If set to 'categorical', latent variable is used to predict the entire image (not its features); in this case, one must provide -path_to_train_img_vecs and -path_to_valid_img_vecs. If set to 'none', this means there is no image loss (latent variables are not used to predict image features, just as random noise).""")
    parser.add_argument('-two_step_image_prediction', action='store_true', required=False,
                        help="""Whether to use latent variable to predict image features and pixels, or only one or another. If set to True, image features prediction loss type is 'logprob' and image pixels prediction loss type is 'categorical'. If set to False, either only image features (--image_loss in ['cosine', 'logprob']) or image pixels (--image_loss in ['categorical']) are predicted.""")
    parser.add_argument('-use_rgb_images', action='store_true', required=False,
                        help="""Whether to use RGB images or not (3 x size x size). If not set, default is False, i.e. grayscale images (size x size)""")
    parser.add_argument('-path_to_train_img_vecs', required=False,
                        help="""Path to hdf5 file containing training images (i.e. pixels). Must be set in case --image_loss is 'categorical'.""")
    parser.add_argument('-path_to_valid_img_vecs', required=False,
                        help="""Path to hdf5 file containing validation images (i.e. pixels). Must be set in case --image_loss is 'categorical'.""")
    group= parser.add_argument_group('Image features type')
    gme = group.add_mutually_exclusive_group(required=True)
    gme.add_argument('--use_posterior_image_features', action='store_true', 
                     help="""Use image features with the image's posterior class probabilities?""")
    gme.add_argument('--use_global_image_features', action='store_true',
                     help="""Use global image features?""")
    gme.add_argument('--use_local_image_features', action='store_true',
                     help="""Use local image features?""")
    parser.add_argument('-non_shared_inference_network', action='store_true',
                        help='Whether to use an inference network with independent parameters (no parameter sharing with generative network).')

def train_mm_vi_model1_opts(parser):
    """Hyperparameters of the VI model 1."""
    # add general NMT-VI hyperparameters
    _train_mm_vi_opts(parser)

def translate_mm_vi_opts(parser):
    parser.add_argument('-path_to_test_img_feats', required=True,
                        help="""Path to hdf5 file containing test image features""")



# MARKDOWN boilerplate

# Copyright 2016 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
class MarkdownHelpFormatter(argparse.HelpFormatter):
    """A really bare-bones argparse help formatter that generates valid markdown.
    This will generate something like:
    usage
    # **section heading**:
    ## **--argument-one**
    ```
    argument-one help text
    ```
    """

    def _format_usage(self, usage, actions, groups, prefix):
        return ""

    def format_help(self):
        print(self._prog)
        self._root_section.heading = '# Options: %s' % self._prog
        return super(MarkdownHelpFormatter, self).format_help()

    def start_section(self, heading):
        super(MarkdownHelpFormatter, self)\
            .start_section('### **%s**' % heading)

    def _format_action(self, action):
        if action.dest == "help" or action.dest == "md":
            return ""
        lines = []
        lines.append('* **-%s %s** ' % (action.dest,
                                        "[%s]" % action.default
                                        if action.default else "[]"))
        if action.help:
            help_text = self._expand_help(action)
            lines.extend(self._split_lines(help_text, 80))
        lines.extend(['', ''])
        return '\n'.join(lines)


class MarkdownHelpAction(argparse.Action):
    def __init__(self, option_strings,
                 dest=argparse.SUPPRESS, default=argparse.SUPPRESS,
                 **kwargs):
        super(MarkdownHelpAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        parser.formatter_class = MarkdownHelpFormatter
        parser.print_help()
        parser.exit()


class DeprecateAction(argparse.Action):
    def __init__(self, option_strings, dest, help=None, **kwargs):
        super(DeprecateAction, self).__init__(option_strings, dest, nargs=0,
                                              help=help, **kwargs)

    def __call__(self, parser, namespace, values, flag_name):
        help = self.help if self.help is not None else ""
        msg = "Flag '%s' is deprecated. %s" % (flag_name, help)
        raise argparse.ArgumentTypeError(msg)

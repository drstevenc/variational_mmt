# variational\_mmt

## TL-DR

This is the code base one should use to reproduce results reported in the ACL 2019 paper [Latent variable model for multi-modal translation](https://www.aclweb.org/anthology/papers/P/P19/P19-1642/).
We propose a conditional variational auto-encoder model for multi-modal translation,
i.e. to model the interaction between visual and textual features for multi-modal neural machine translation (MMT) through a latent variable model.
This latent variable can be seen as a multi-modal stochastic embedding of an image and its description in a foreign language.
It is used in a target-language decoder and also to predict image features.
Importantly, our model formulation utilises visual and textual inputs during training but does not require that images be available at test time.
Please refer to the paper for more details.

## Before you start

Before you start, please ensure that:

- You have installed the right version of PyTorch and all the dependencies according to `requirements.txt`;
- If you want to use your own version of the Multi30k data set, that you changed the respective variable names in the `run_*.sh` files as required.

If you want to use the exact version of the Multi30k data set used in the paper:

- download image features for the Translated Multi30k data set:
    - [`flickr30k_train_resnet50_cnn_features.hdf5`](ADD LINK): training set, 29K examples.
    - [`flickr30k_valid_resnet50_cnn_features.hdf5`](ADD LINK): validation set, 1,014 examples.
    - [`flickr30k_test_resnet50_cnn_features.hdf5`](ADD LINK): 2016 test set, 1K examples.
    - [`flickr30k_test_2017_flickr_resnet50_cnn_features.hdf5`](ADD LINK): 2017 test set, 1K examples.
    - [`flickr30k_test_2017_mscoco_resnet50_cnn_features.hdf5`](ADD LINK): ambiguous MSCOCO test set, 461 examples.
- download additional image features for the Translated+Backtranslated Comparable Multi30k data set:
    - [`flickr30k_train_translated-5x-comparable-1x_resnet50_cnn_features.shuffled.hdf5`](ADD LINK): this file contains features for 290,000 images, i.e. 29K translated Multi30k images five times each (145K) and 29K comparable Multi30k images also five times each (145K). We upsample images for the translated Multi30k to keep them about half of the images used when training the model in this setting.
- ensure that variable names are correct in the corresponding `run_translated_m30k_only.sh` and `run_additional_data.sh` files. Image features were extracted as described in the paper, i.e. using a pretrained ResNet-50.
- use the PyTorch binaries under
`./data/m30k.*.pt` (translated Multi30k) or
`./data/concat-multi30k-translational-5times-comparable-1time-shuffled.*.pt` (back-translated comparable + translated Multi30k).

## Training

To see how to call the `train_mm_vi_model1.py` script, please refer to the `run_*.sh` scripts or run `train_mm_vi_model1.py --help`.

### Training a model on the translated Multi30k

To train a model using the Translated Multi30k data set only (~29K source/target/image triplets), run:
```bash
run_translated_m30k_only.sh
```

This bash script assumes you have a GPU available with at least 12GBs, e.g. TitanX, 1080Ti, etc., and sets all the hyperparameters to reproduce the results in the paper.

### Training a model on the back-translated comparable and translated Multi30k

To train a model using the back-translated comparable Multi30k in addition to the translated Multi30k data set (total of ~145K source/target/image triplets), simply run:
```bash
run_additional_data.sh
```

This bash script also assumes you have a GPU available with at least 12GBs (e.g. TitanX, 1080Ti, etc.) and sets all the hyperparameters to reproduce the results in the paper.

## Decoding a translation

By calling the bash scripts above, you will not only train, but after finishing training will also decode the Multi30k's validation, test 2016, test 2017, and the ambiguous MSCOCO 2017 test set.
By default, the model used to translate is the one selected according to best BLEU4 scores on the validation set.

To see how to use the `translate_mm_vi.py` script directly, please refer to the `run_*.sh` scripts or call `translate_mm_vi.py --help`.

## Citation

If you use this code base, please consider citing our paper.

    @inproceedings{calixto-etal-2019-latent,
        title = "Latent Variable Model for Multi-modal Translation",
        author = "Calixto, Iacer and Rios, Miguel  and Aziz, Wilker",
        booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
        month = jul,
        year = "2019",
        address = "Florence, Italy",
        publisher = "Association for Computational Linguistics",
        url = "https://www.aclweb.org/anthology/P19-1642",
        pages = "6392--6405",
    }

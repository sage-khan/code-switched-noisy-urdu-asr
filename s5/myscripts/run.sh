#!/bin/bash

. ./cmd.sh
[ -f path.sh ] && . ./path.sh
set -e

numLeavesTri1=2000
numGaussTri1=10000

numLeavesMLLT=3500
numGaussMLLT=20000

numLeavesSAT=4200
numGaussSAT=40000

# speakers >= no.of jobs
feats_nj=4
train_nj=4
decode_nj=4


echo "============================================================================"
echo "                Data & Lexicon & Language Preparation                       "
echo "============================================================================"

utils/fix_data_dir.sh data/train
utils/fix_data_dir.sh data/test

utils/prepare_lang.sh data/local/lang '<oov>' data/local data/lang

# utils/format_lm.sh data/lang data/local/lm/LM1.gz data/local/lang/lexicon.txt data/lang_test

#utils/format_lm.sh data/lang data/local/lm/LM2.gz data/local/lang/lexicon.txt data/lang_test
#utils/format_lm.sh data/lang data/local/lm/lm.gz data/local/lang/lexicon.txt data/lang_test


echo "============================================================================"
echo "         MFCC Feature Extraction & CMVN for Training and Test set           "
echo "============================================================================"

mfccdir=mfcc

steps/make_mfcc.sh --cmd $train_cmd --nj 5 data/train exp/make_mfcc/train $mfccdir
steps/compute_cmvn_stats.sh data/train exp/make_mfcc/train $mfccdir

steps/make_mfcc.sh --cmd $train_cmd --nj 5 data/test exp/make_mfcc/test $mfccdir
steps/compute_cmvn_stats.sh data/test exp/make_mfcc/test $mfccdir

utils/validate_data_dir.sh data/train
utils/fix_data_dir.sh data/train

utils/validate_data_dir.sh data/test
utils/fix_data_dir.sh data/test
echo "============================================================================"
echo "                              FINISHED DATA PREP                            "
echo "============================================================================"

echo "============================================================================"
echo "                           MonoPhone Training                               "
echo "============================================================================"

steps/train_mono.sh --boost-silence 1.25 --beam 6 --totgauss 2000 --num-iters 50 --nj "$train_nj" --cmd "$train_cmd" data/train data/lang exp/mono
../../../src/gmmbin/gmm-info exp/mono/final.mdl

utils/mkgraph.sh --mono data/lang exp/mono exp/mono/graphD
steps/decode.sh --nj 5 exp/mono/graphD data/test exp/mono/decode


echo "============================================================================"
echo "                          Word Error Rate - Monophones                      "
echo "============================================================================"

cd exp/mono/decode
cat wer_*|grep "WER"| sort -n
cd ../../..
 
echo "============================================================================"
echo "                  Align Monophones                                          "
echo "============================================================================"


# Align delta-based triphones with boost silence
steps/align_si.sh --boost-silence 1.25 --nj "$train_nj" --cmd "$train_cmd" --beam 10 --retry-beam 40 data/train data/lang exp/mono exp/mono_ali

echo "============================================================================"
echo "                  tri1 : Deltas + Delta-Deltas Training                     "
echo "============================================================================"

# Train delta + delta-delta triphones 
steps/train_deltas.sh --num-iters 40--beam 10 --cmd "$train_cmd" $numLeavesTri1 $numGaussTri1 data/train data/lang exp/mono_ali exp/tri1

../../../src/gmmbin/gmm-info exp/tri1/final.mdl

utils/mkgraph.sh data/lang exp/tri1 exp/tri/graph
steps/decode.sh --nj 5 exp/tri1/graph data/test exp/tri1/decode

echo "============================================================================"
echo "                         TRIPHONE WORD ERROR RATE                           "
echo "============================================================================"

cd exp/tri1/decode
cat wer_*|grep "WER"| sort -n
cd ../../..

echo "============================================================================"
echo "                       Align Triphone                           "
echo "============================================================================"

# Align
steps/align_si.sh --boost-silence 1.25 --beam 10 --retry-beam 40 --nj "$train_nj" --cmd "$train_cmd" data/train data/lang exp/tri1 exp/tri1_ali

echo "============================================================================"
echo "                       tri2 : LDA + MLLT Training                           "
echo "============================================================================"
# LDA + MLLT training
steps/train_lda_mllt.sh --splice-opts "--left-context=3 --right-context=3" --cmd "$train_cmd" $numLeavesMLLT $numGaussMLLT data/train data/lang exp/tri1_ali exp/tri2

../../../src/gmmbin/gmm-info exp/tri2/final.mdl

echo "============================================================================"
echo "                       Align Triphone LDA + MLLT                            "
echo "============================================================================"

#Align
steps/align_si.sh --boost-silence 1.25 --beam 10 --retry-beam 40 --nj "$train_nj" --cmd "$train_cmd" --use-graphs true data/train data/lang exp/tri2 exp/tri2_ali

echo "============================================================================"
echo "               tri3 : LDA + MLLT + SAT Training & Decoding                  "
echo "============================================================================"

#Train SAT
steps/train_sat.sh --cmd "$train_cmd" $numLeavesSAT $numGaussSAT data/train data/lang exp/tri2_ali exp/tri3

# Make final language model graph for tri3 and decode
utils/mkgraph.sh data/lang_test exp/tri3 exp/tri3/graph

steps/decode_fmllr.sh --nj "$decode_nj" --cmd "$decode_cmd" exp/tri3/graph data/test exp/tri3/decode

../../../src/gmmbin/gmm-info exp/tri3/final.mdl

echo "============================================================================"
echo "                         tri3 : LDA + MLLT + SAT WORD ERROR RATE            "
echo "============================================================================"

cd exp/tri3/decode
cat wer_*|grep "WER"| sort -n
cd ../../..

echo "============================================================================"
echo "                       Align Triphone LDA + MLLT + SAT                      "
echo "============================================================================"

#Align
#steps/align_si.sh --boost-silence 1.25 --beam 10 --retry-beam 40 --nj "$train_nj" --cmd "$train_cmd" --use-graphs true data/train data/lang exp/tri3 exp/tri3_ali

steps/align_fmllr.sh --cmd "$train_cmd" --nj "$train_nj" data/train data/lang exp/tri3 exp/tri3_ali

echo "============================================================================"
echo "                          DNN Training                                      "
echo "============================================================================"

steps/nnet3/train_tdnn.sh --initial-learning-rate 0.0075 --final-learning-rate 0.001 --num-hidden-layers 4 --minibatch-size 64 --hidden-layer-dim 512 --num-jobs-nnet 12 --num-epochs 15 data/train data/lang exp/tri3_ali exp/DNN
steps/nnet3/decode.sh --nj 4 exp/tri3/graph data/test exp/nnet3/decode

echo "============================================================================"
echo "                         DNN WORD ERROR RATE                                "
echo "============================================================================"


cd exp/DNN/decode
cat wer_*|grep "WER"| sort -n
cd ../../..

echo "============================================================================"
echo "                       Align NNET3                                          "
echo "============================================================================"

steps/nnet3/align.sh data/train data/lang exp/nnet3 exp/nnet3_ali

echo "============================================================================"
echo "                          BEST WER CALCULATION                              "
echo "============================================================================"

decode_beam=5
decode_lattice_beam=3
decode_max_active_states=200


graph= exp/tri3/graph
model= exp/tri3
test_dir= data/test
suffix=$(date) 
num_jobs= 4

if [ "$#" -ne 5 ]; then
    echo "ERROR: $0"
    echo "USAGE: $0 <graph> <model> <test_dir> <suffix>"
    exit 1
fi

if [ 1 ]; then
    
    printf "\n####================####\n";
    printf "#### BEGIN DECODING ####\n";
    printf "####================####\n\n";
    
    # DECODE WITH TRIPHONES WITH SAT ADJUSTED FEATURES
    
    # steps/decode_fmllr.sh --cmd "$cmd" \
    #     --nj $num_processors \
    #     ${exp_dir}/triphones_lda_mllt_sat/graph \
    #     ${data_dir}/${test_dir} \
    #     "${exp_dir}"'/triphones_lda_mllt_sat/decode_'"${test_dir}" \
    #     $unknown_phone \
    #     $silence_phone \
    #     || exit 1;

    
    # DECODE WITH REGULAR TRIPHONES WITH VANILLA DELTA FEATURES

    printf "\n ### Decoding with $num_jobs jobs  ### "
    
    steps/decode.sh \
        --cmd "$train_cmd" \
        --nj $num_jobs \
        --beam $decode_beam \
        --lattice-beam $decode_lattice_beam \
        --max-active $decode_max_active_states \
        $graph \
        $model \
        $test_dir \
        $test_dir/decode \
        "SPOKEN_NOISE" \
        "SIL" \
        || printf "\n####\n#### ERROR: decode.sh \n####\n\n" \
        || exit 1;
    

    printf "#### BEGIN CALCULATE WER ####\n";
    
    for x in $test_dir/decode; do
        [ -d $x ] && grep "WER" $x/wer_* | utils/best_wer.sh > WER_triphones_${suffix}.txt;
    done

    printf "\n####==============####\n";
    printf "#### END DECODING ####\n";
    printf "####==============####\n\n";

    echo "###"
    echo "graph = $graph" >> WER_triphones_${suffix}.txt

    echo "###"
    echo "acoustic model = $model" >> WER_triphones_${suffix}.txt
    ../../../src/gmmbin/gmm-info $model >> WER_triphones_${suffix}.txt
    
    echo "###"
    echo "test dir = $test_dir" >> WER_triphones_${suffix}.txt
    
fi

exit;

echo "============================================================================"
echo "                          Saving Language Model                             "
echo "============================================================================"

#### Copy all necessary files to use new LM with this acoustic model
### and only necessary files to save space
    
#cp data_${corpus_name} ${corpus_name}_${run}

#### delete unneeded files
#rm -rf ${corpus_name}_${run}/train ${corpus_name}_${run}/test ${corpus_name}_${run}/lang_decode

lang= echo "Enter Language name:"
read lang

# copy acoustic model and decision tree to new dir
mkdir LM/$lang/model
cp exp/tri3/final.mdl LM/${lang}/model/final.mdl
cp exp/tri3/tree exp/LM/${lang}/model/tree

tar -zcvf LM-${lang}.tar.gz LM/$lang

# clean up
#rm -rf ${corpus_name}_${run}

# move for storage
mkdir compressed_experiments
    
mv LM-${lang}.tar.gz compressed_experiments/LM-${lang}-${suffix}.tar.gz

echo "============================================================================"
echo "                          Finished Successfully                             "
echo "============================================================================"

exit 0

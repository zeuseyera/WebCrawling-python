from __future__ import print_function
import numpy as np
import tensorflow as tf

import argparse
import time
import os
from six.moves import cPickle

from utils import TextLoader
from model import Model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='save',
                       help='model directory to load stored checkpointed models from')
    parser.add_argument('-n', type=int, default=200,
                       #help='number of words to sample')
                       help='샘플단어의 개수' )
    parser.add_argument('--prime', type=str, default=' ',
                       help='prime text')
    parser.add_argument('--pick', type=int, default=1,
                       help='1 = weighted pick, 2 = beam search pick')
    parser.add_argument('--width', type=int, default=4,
                       help='width of the beam search')
    parser.add_argument('--sample', type=int, default=1,
                       help='0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')

    args = parser.parse_args()
    sample( args )

def sample( args ):
    with open( os.path.join( args.save_dir, 'config.pkl' ), 'rb' ) as f:
        saved_args = cPickle.load( f )

    with open( os.path.join( args.save_dir, 'words_vocab.pkl' ), 'rb' ) as f:
        words, vocab = cPickle.load( f )

    model = Model( saved_args, True )

    # -------------------------------------------------
    # GPU 문제 발생: failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED
    #with tf.Session() as sess:

    # -------------------------------------------------
    # GPU 문제 해결방법: failed to create cublas handle: CUBLAS_STATUS_ALLOC_FAILED
    SeolJeong_GPU = tf.ConfigProto()
    SeolJeong_GPU.gpu_options.allow_growth = True

    with tf.Session( config=SeolJeong_GPU ) as sess:

        tf.global_variables_initializer().run()
        saver = tf.train.Saver( tf.global_variables() )
        ckpt = tf.train.get_checkpoint_state( args.save_dir )

        if ckpt and ckpt.model_checkpoint_path:
            saver.restore( sess, ckpt.model_checkpoint_path )
            print( model.sample( sess, words, vocab, args.n, args.prime, args.sample, args.pick, args.width ) )

if __name__ == '__main__':
    main()

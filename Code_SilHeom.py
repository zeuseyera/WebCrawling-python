# ========================================================================================
# 파이썬코드를 확인한다
# ========================================================================================

# ----------------------------------------------------------------------------------------
# 코드에 필요한 라이브러리를 불러와 탑재한다
# ----------------------------------------------------------------------------------------
# 기본 라이브러리
from __future__ import print_function
import argparse
import time
import os

# 연관된 라이브러리
import numpy as np
import tensorflow as tf

from six.moves import cPickle       # six.moves 모듈에서 cPickle 클래스만 탑재

# 설계자가 필요에따라 구현한 모듈(파일)을 탑재한다
# 예1: 모듈명, 예2: 폴더명.모듈명 예3: 폴더명.폴더명.모듈명 등등
from utils import TextLoader        # utils 모듈에서 TextLoader 클래스만 탑재
from model import Model
    # from beam import BeamSearch


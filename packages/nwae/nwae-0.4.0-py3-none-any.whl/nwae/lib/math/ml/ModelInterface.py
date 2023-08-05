# -*- coding: utf-8 -*-

import threading
import time
import nwae.utils.Log as log
from inspect import currentframe, getframeinfo
import pandas as pd
import numpy as np
import nwae.lib.math.ml.TrainingDataModel as tdm
import os


#
# Interfaces that a Model must implement
#
class ModelInterface(threading.Thread):

    # Terms for dataframe, etc.
    TERM_CLASS      = 'class'
    TERM_SCORE      = 'score'
    TERM_CONFIDENCE = 'confidence'
    TERM_DIST       = 'dist'
    TERM_DISTNORM   = 'distnorm'
    TERM_RADIUS     = 'radius'

    # Matching
    MATCH_TOP = 10

    # From rescoring training data (using SEARCH_TOPX_RFV=5), we find that
    #    5% quartile score  = 55
    #    25% quartile score = 65
    #    50% quartile score = 70
    #    75% quartile score = 75
    #    95% quartile score = 85
    # Using the above information, we set
    CONFIDENCE_LEVEL_5_SCORE = 75
    CONFIDENCE_LEVEL_4_SCORE = 65
    CONFIDENCE_LEVEL_3_SCORE = 55
    # For confidence level 0-2, we run the bot against non-related data and we found
    #    99% quartile score = 32
    #    95% quartile score = 30
    #    75% quartile score = 20
    CONFIDENCE_LEVEL_2_SCORE = 40   # Means <1% of non-related data will go above it
    CONFIDENCE_LEVEL_1_SCORE = 20   # This means 25% of non-related data will go above it

    class predict_class_retclass:
        def __init__(
                self,
                predicted_classes,
                top_class_distance = None,
                match_details = None
        ):
            self.predicted_classes = predicted_classes
            # The top class and shortest distances (so that we can calculate sum of squared error
            self.top_class_distance = top_class_distance
            self.match_details = match_details
            return

    def __init__(
            self,
            model_name,
            identifier_string,
            dir_path_model,
            training_data,
            # Train only by y/labels and store model files in separate y_id directories
            is_partial_training
    ):
        super(ModelInterface, self).__init__()

        self.model_name = model_name
        self.identifier_string = identifier_string
        self.dir_path_model = dir_path_model
        self.training_data = training_data
        self.is_partial_training = is_partial_training

        self.stoprequest = threading.Event()

        self.__mutex_load_model = threading.Lock()

        # Training data for testing back only
        # This value must be initialized by the derived class
        self.training_data = None
        # This value must be initialized by the derived class
        self.y_id = None

        return

    def initialize_training_data_paths(self):
        prefix = ModelInterface.get_model_file_prefix(
            dir_path_model      = self.dir_path_model,
            model_name          = self.model_name,
            identifier_string   = self.identifier_string,
            is_partial_training = self.is_partial_training
        )
        if self.is_partial_training:
            if type(self.y_id) not in (int, str):
                raise Exception(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Cannot set training paths without a single y_id! Got y_id: ' + str(self.y_id)
                    + ' as type "' + str(type(self.y_id)) + '".'
                )
            prefix = prefix + '/' + str(self.y_id)
        self.fpath_training_data_x          = prefix + '.training_data.x.csv'
        self.fpath_training_data_x_friendly = prefix + '.training_data.x_friendly.csv'
        # self.fpath_training_data_x_friendly_json = prefix + '.training_data.x_friendly.json'
        self.fpath_training_data_x_name     = prefix + '.training_data.x_name.csv'
        self.fpath_training_data_y          = prefix + '.training_data.y.csv'

    @staticmethod
    def get_model_file_prefix(
            dir_path_model,
            model_name,
            identifier_string,
            is_partial_training
    ):
        # Prefix or dir
        prefix_or_dir = dir_path_model + '/' + model_name + '.' + identifier_string
        if is_partial_training:
            # Check if directory exists
            if not os.path.isdir(prefix_or_dir):
                log.Log.important(
                    str(ModelInterface.__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Path "' + str(prefix_or_dir) + '" does not exist. Trying to create this directory...'
                )
                try:
                    os.mkdir(
                        path = prefix_or_dir
                    )
                    log.Log.important(
                        str(ModelInterface.__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                        + ': Path "' + str(prefix_or_dir) + '" successfully created.'
                    )
                except Exception as ex:
                    errmsg =\
                        str(ModelInterface.__name__) + ' ' + str(getframeinfo(currentframe()).lineno)\
                        + ': Error creating directory "' + str(prefix_or_dir) + '". Exception ' + str(ex) + '.'
                    log.Log.error(errmsg)
                    raise Exception(errmsg)
            return prefix_or_dir
        else:
            return prefix_or_dir

    def join(self, timeout=None):
        log.Log.critical(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Model Identifier "' + str(self.identifier_string) + '" join called..'
        )
        self.stoprequest.set()
        super(ModelInterface, self).join(timeout=timeout)
        log.Log.critical(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Model Identifier "' + str(self.identifier_string) + '" Background Thread ended..'
        )

    def run(self):
        log.Log.critical(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Model Identifier "' + str(self.identifier_string) + '" Background Thread started..'
        )
        if not self.is_model_ready():
            self.load_model_parameters()

        sleep_time = 10
        while True:
            if self.stoprequest.isSet():
                log.Log.important(
                    str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                    + ': Model Identifier "' + str(self.identifier_string) + '" Breaking from forever thread...'
                )
                break
            if self.check_if_model_updated():
                try:
                    self.__mutex_load_model.acquire()
                    self.load_model_parameters()
                    if not self.is_model_ready():
                        log.Log.important(
                            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                            + ': Model "' + self.identifier_string
                            + '" failed to load. Try again in ' + str(sleep_time) + ' secs..'
                        )
                finally:
                    self.__mutex_load_model.release()
            time.sleep(sleep_time)

    def is_model_ready(self):
        raise Exception(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Not implemented by derived class!'
        )

    def wait_for_model(self):
        count = 1
        sleep_time_wait_rfv = 0.1
        wait_max_time = 10
        while not self.is_model_ready():
            log.Log.warning(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Waiting for model with identifier "' + str(self.identifier_string)
                + ', sleep for ' + str(count * sleep_time_wait_rfv) + ' secs now..'
            )
            if count * sleep_time_wait_rfv > wait_max_time:
                errmsg = str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                         + ': Waited too long for model "' + str(self.identifier_string) \
                         + '" total wait time ' + str(count * sleep_time_wait_rfv) + ' secs. Raising exception..'
                raise Exception(errmsg)
            time.sleep(sleep_time_wait_rfv)
            count = count + 1

    def get_model_features(
            self
    ):
        raise Exception(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Not implemented by derived class!'
        )

    def predict_classes(
            self,
            # ndarray type of >= 2 dimensions
            x
    ):
        raise Exception(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Not implemented by derived class!'
        )

    def predict_class(
            self,
            # ndarray type of >= 2 dimensions, single point/row array
            x
    ):
        raise Exception(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Not implemented by derived class!'
        )

    #
    # Train from partial model files
    #
    def train_from_partial_models(
            self,
            write_model_to_storage = True,
            write_training_data_to_storage = False,
            model_params = None,
    ):
        raise Exception(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Not implemented by derived class!'
        )

    def train(
            self,
            write_model_to_storage = True,
            write_training_data_to_storage = False,
            model_params = None,
            # Option to train a single y ID/label
            y_id = None
    ):
        raise Exception(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Not implemented by derived class!'
        )

    def persist_model_to_storage(
            self
    ):
        raise Exception(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Not implemented by derived class!'
        )

    def load_model_parameters(
            self
    ):
        raise Exception(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Not implemented by derived class!'
        )

    def check_if_model_updated(
            self
    ):
        raise Exception(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Not implemented by derived class!'
        )

    def persist_training_data_to_storage(
            self,
            td
    ):
        self.initialize_training_data_paths()
        #
        # Write back training data to file, for testing back the model only, not needed for the model
        #
        if not self.is_partial_training:
            df_td_x = pd.DataFrame(
                data    = td.get_x(),
                columns = td.get_x_name(),
                index   = td.get_y()
            )
            df_td_x.sort_index(inplace=True)
            df_td_x.to_csv(
                path_or_buf = self.fpath_training_data_x,
                index       = True,
                index_label = 'INDEX'
            )
            log.Log.critical(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Saved Training Data x with shape ' + str(df_td_x.shape)
                + ' filepath "' + self.fpath_training_data_x + '"'
            )

        try:
            x_friendly = td.get_print_friendly_x()

            # This file only for debugging
            f = open(file=self.fpath_training_data_x_friendly, mode='w', encoding='utf-8')
            for i in x_friendly.keys():
                line = str(x_friendly[i])
                f.write(str(line) + '\n\r')
            f.close()
            log.Log.important(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Saved training data x friendly to file "' + self.fpath_training_data_x_friendly + '".'
            )
        except Exception as ex:
            log.Log.error(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Could not create x_ref friendly file "' + self.fpath_training_data_x_friendly
                + '". ' + str(ex)
            )

        if not self.is_partial_training:
            df_td_x_name = pd.DataFrame(td.get_x_name())
            df_td_x_name.to_csv(
                path_or_buf = self.fpath_training_data_x_name,
                index       = True,
                index_label = 'INDEX'
            )
            log.Log.critical(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Saved Training Data x_name with shape ' + str(df_td_x_name.shape)
                + ' filepath "' + self.fpath_training_data_x_name + '"'
            )

            df_td_y = pd.DataFrame(
                data  = td.get_y_name(),
                index = td.get_y()
            )
            df_td_y.to_csv(
                path_or_buf = self.fpath_training_data_y,
                index       = True,
                index_label = 'INDEX'
            )
            log.Log.critical(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Saved Training Data y with shape ' + str(df_td_y.shape)
                + ' filepath "' + self.fpath_training_data_y + '"'
            )
        return

    def load_training_data_from_storage(
            self
    ):
        self.initialize_training_data_paths()
        try:
            df_td_x = pd.read_csv(
                filepath_or_buffer=self.fpath_training_data_x,
                sep=',',
                index_col='INDEX'
            )
            df_td_x_name = pd.read_csv(
                filepath_or_buffer=self.fpath_training_data_x_name,
                sep=',',
                index_col='INDEX'
            )
            df_td_y = pd.read_csv(
                filepath_or_buffer=self.fpath_training_data_y,
                sep=',',
                index_col='INDEX'
            )

            td = tdm.TrainingDataModel(
                x      = np.array(df_td_x.values),
                x_name = np.array(df_td_x_name.values).transpose()[0],
                # y is the index remember, the column is y_name
                y      = np.array(df_td_y.index),
                y_name = np.array(df_td_y.values).transpose()[0],
            )
            log.Log.important(
                str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Training Data x read ' + str(df_td_x.shape) + ' shape'
                + ', x_name read ' + str(df_td_x_name.shape)
                + '\n\r' + str(td.get_x_name())
                + ', y read ' + str(df_td_y.shape)
                + '\n\r' + str(td.get_y())
            )
            self.training_data = td
        except Exception as ex:
            errmsg = str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)\
                     + ': Load training data from file failed for identifier "' + self.identifier_string\
                     + '". Error msg "' + str(ex) + '".'
            log.Log.critical(errmsg)
            raise Exception(errmsg)

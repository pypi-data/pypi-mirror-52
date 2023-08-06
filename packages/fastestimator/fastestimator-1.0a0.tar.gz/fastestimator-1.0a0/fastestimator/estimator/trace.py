# Copyright 2019 The FastEstimator Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Trace contains metrics and other information users want to track."""
import datetime
import os
import time

import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from tensorflow.python.framework import ops as tfops
from tensorflow.python.keras import backend
from tensorflow.python.keras.layers import embeddings
from tensorflow.python.ops import array_ops, summary_ops_v2

from fastestimator.network.lrschedule import LRSchedule
from fastestimator.util.util import is_number


class Trace:
    """Trace base class.
    User can use `Trace` to customize their own operations during training, validation and testing.
    The `Network` instance can be accessible by `self.network`. Trace execution order will attempt to be inferred
    whenever possible based on the provided inputs and outputs variables.
    """
    def __init__(self, inputs=None, outputs=None, mode=None):
        """
        Args:
            inputs (str, list, set): A set of keys that this trace intends to read from the state dictionary as inputs
            outputs (str, list, set): A set of keys that this trace intends to write into the state dictionary
            mode (string): Restrict the trace to run only on given modes ('train', 'eval', 'test'). None will always
                            execute
        """
        self.network = None
        self.mode = mode
        self.inputs = set(filter(None, inputs or {})) if not isinstance(inputs, str) else {inputs}
        self.outputs = set(filter(None, outputs or {})) if not isinstance(outputs, str) else {outputs}

    def on_begin(self, state):
        """Runs once at the beginning of training

        Args:
            state (dict): dictionary of run time that has the following key(s):
                * "num_devices": number of devices(mainly gpu) that are being used, if cpu only, the number is 1
                * any keys written by 'on_begin' of previous traces
        """
    def on_epoch_begin(self, state):
        """Runs at the beginning of each epoch of the mode.

        Args:
            state (dict): dictionary of run time that has the following key(s):
                * "mode":  current run time mode, can be "train", "eval" or "test"
                * "epoch": current epoch index starting from 0
                * "train_step": current global training step starting from 0
                * any keys written by 'on_epoch_begin' of previous traces
        """
    def on_batch_begin(self, state):
        """Runs at the beginning of every batch of the mode.

        Args:
            state (dict): dictionary of run time that has the following key(s):
                * "mode": current run time mode, can be "train", "eval" or "test"
                * "epoch": current epoch index starting from 0
                * "train_step": current global training step starting from 0
                * "batch_idx": current local step of the epoch starting from 0
                * "batch_size": current global batch size
                * any keys written by 'on_batch_begin' of previous traces
        """
    def on_batch_end(self, state):
        """Runs at the end of every batch of the mode. Anything written to the top level of the state dictionary will be
            printed in the logs. Things written only to the batch sub-dictionary will not be logged

        Args:
            state (ChainMap): dictionary of run time that has the following key(s):
                * "mode":  current run time mode, can be "train", "eval" or "test"
                * "epoch": current epoch index starting from 0
                * "train_step": current global training step starting from 0
                * "batch_idx": current local step of the epoch starting from 0
                * "batch_size": current global batch size
                * "batch": the batch data after the Network execution
                * <loss_name> defined in FEModel: loss of current batch (only available when mode is "train")
                * any keys written by 'on_batch_end' of previous traces
        """
    def on_epoch_end(self, state):
        """Runs at the end of every epoch of the mode. Anything written into the state dictionary will be logged

        Args:
            state (ChainMap): dictionary of run time that has the following key(s):
                * "mode":  current run time mode, can be "train", "eval" or "test"
                * "epoch": current epoch index starting from 0
                * "train_step": current global training step starting from 0
                * <loss_name> defined in FEModel: average loss of the epoch (only available when mode is "eval")
                * any keys written by 'on_epoch_end' of previous traces
        """
    def on_end(self, state):
        """Runs once at the end training. Anything written into the state dictionary will be logged

        Args:
            state (ChainMap): dictionary of run time that has the following key(s):
                * "train_step":  current global training step starting from 0
                * "num_devices": number of devices (mainly gpu) that are being used. If cpu only, the number is 1
                * "elapsed_time": time since the start of training in seconds
                * any keys written by 'on_end' of previous traces
        """


class MonitorLoss(Trace):
    def __init__(self):
        super().__init__()
        self.epochs_since_best = 0
        self.best_loss = None
        self.epoch_losses = []
        self.eval_results = None

    def on_epoch_begin(self, state):
        self.epoch_losses = self.network.epoch_losses
        if state["mode"] == "eval":
            self.eval_results = None

    def on_batch_end(self, state):
        if state["mode"] == "train":
            for key in self.epoch_losses:
                state[key] = self._reduce_loss(state["batch"][key], state["batch_size"])
        elif state["mode"] == "eval":
            if self.eval_results is None:
                self.eval_results = dict(
                    (key, [self._reduce_loss(state["batch"][key], state["batch_size"])]) for key in self.epoch_losses)
            else:
                for key in self.eval_results.keys():
                    self.eval_results[key].append(self._reduce_loss(state["batch"][key], state["batch_size"]))

    def on_epoch_end(self, state):
        if state["mode"] == "eval":
            for key in self.eval_results.keys():
                state[key] = np.mean(np.array(self.eval_results[key]), axis=0)
            if len(self.eval_results) == 1:
                key = list(self.eval_results.keys())[0]
                if self.best_loss is None or state[key] < self.best_loss:
                    self.best_loss = state[key]
                    self.epochs_since_best = 0
                else:
                    self.epochs_since_best += 1
                state["min_" + key] = self.best_loss
                state["since_best_loss"] = self.epochs_since_best

    @staticmethod
    @tf.function
    def _reduce_loss(element_wise_loss, global_batch_size):
        return tf.reduce_sum(element_wise_loss) / global_batch_size


class TrainInfo(Trace):
    """Essential training information for logging during training
    """
    def __init__(self, log_steps):
        super().__init__(mode="train")
        self.log_steps = log_steps
        self.elapse_times = []
        self.num_example = 0
        self.time_start = None
        self.train_start = None

    def on_begin(self, state):
        self.train_start = time.perf_counter()
        for model_name, model in self.network.model.items():
            state[model_name + "_lr"] = round(backend.get_value(model.optimizer.lr), 6)

    def on_epoch_begin(self, state):
        self.time_start = time.perf_counter()

    def on_batch_end(self, state):
        self.num_example += state["batch_size"]
        if state["train_step"] % self.log_steps == 0:
            if state["train_step"] > 0:
                self.elapse_times.append(time.perf_counter() - self.time_start)
                state["examples/sec"] = round(self.num_example / np.sum(self.elapse_times), 2)
            self.elapse_times = []
            self.num_example = 0
            self.time_start = time.perf_counter()

    def on_epoch_end(self, state):
        self.elapse_times.append(time.perf_counter() - self.time_start)

    def on_end(self, state):
        state['total_time'] = "{} sec".format(round(time.perf_counter() - self.train_start, 2))
        for model_name, model in self.network.model.items():
            state[model_name + "_lr"] = round(backend.get_value(model.optimizer.lr), 6)


class LRController(Trace):
    def __init__(self,
                 model_name,
                 lr_schedule=None,
                 reduce_on_eval=False,
                 reduce_patience=10,
                 reduce_factor=0.1,
                 reduce_mode="min",
                 min_lr=1e-6):
        if isinstance(reduce_on_eval, str):
            super().__init__(inputs=reduce_on_eval)
        else:
            super().__init__()
        self.model_name = model_name
        self.lr_schedule = lr_schedule
        self.reduce_on_eval = reduce_on_eval
        self.reduce_patience = reduce_patience
        self.reduce_factor = reduce_factor
        self.reduce_mode = reduce_mode
        self.min_lr = min_lr
        self.reduce_lr_ratio = 1.0
        self.base_lr = None
        self.current_lr = None
        self.log_steps = None
        self.model = None
        self.change_lr = False
        self.wait = 0
        if self.lr_schedule:
            assert isinstance(self.lr_schedule, LRSchedule), "lr_schedule must be instance of LRSchedule"
        if self.reduce_mode == "min":
            self.reduce_metric_best = np.Inf
            self.monitor_op = np.less
        elif self.reduce_mode == "max":
            self.reduce_metric_best = -np.Inf
            self.monitor_op = np.greater
        else:
            raise ValueError("reduce_mode must be either 'min' or 'max'")

    def on_begin(self, state):
        self.log_steps = state["log_steps"]
        self.model = self.network.model[self.model_name]
        self.base_lr = backend.get_value(self.model.optimizer.lr)
        self.current_lr = max(self.base_lr * self.reduce_lr_ratio, self.min_lr)
        if self.reduce_on_eval is True:
            self.reduce_on_eval = self.model.loss_name
        if self.lr_schedule:
            self.lr_schedule.total_epochs = state["total_epochs"]
            self.lr_schedule.total_train_steps = state["total_train_steps"]
            self.lr_schedule.initial_lr = self.current_lr

    def on_epoch_begin(self, state):
        if self.lr_schedule and self.lr_schedule.schedule_mode == "epoch":
            self.base_lr = self.lr_schedule.schedule_fn(state["epoch"], self.base_lr)
            self.change_lr = True

    def on_batch_begin(self, state):
        if state["mode"] == "train":
            if self.lr_schedule and self.lr_schedule.schedule_mode == "step":
                self.base_lr = self.lr_schedule.schedule_fn(state["train_step"], self.base_lr)
                self.change_lr = True
            if self.change_lr:
                self._update_lr()

    def on_batch_end(self, state):
        if state["mode"] == "train" and self.log_steps and state["train_step"] % self.log_steps == 0:
            state[self.model_name + "_lr"] = round(self.current_lr, 6)

    def on_epoch_end(self, state):
        if state["mode"] == "eval" and self.reduce_on_eval:
            current_value = state[self.reduce_on_eval]
            if self.monitor_op(current_value, self.reduce_metric_best):
                self.reduce_metric_best = current_value
                self.wait = 0
            else:
                self.wait += 1
                if self.wait >= self.reduce_patience:
                    self.reduce_lr_ratio *= self.reduce_factor
                    self.change_lr = True
                    print("FastEstimator-LRController: learning rate reduced by factor of {}".format(
                        self.reduce_factor))

    def _update_lr(self):
        self.current_lr = max(self.base_lr * self.reduce_lr_ratio, self.min_lr)
        backend.set_value(self.model.optimizer.lr, self.current_lr)
        self.change_lr = False


class Logger(Trace):
    """Logger, automatically applied by default.
    """
    def __init__(self, log_steps):
        """
        Args:
            log_steps (int, optional): Logging interval. Default value is 100.
        """
        super().__init__(inputs="*")
        self.log_steps = log_steps

    def on_begin(self, state):
        self._print_message("FastEstimator-Start: step: {}; ".format(state["train_step"]), state.maps[0])

    def on_batch_end(self, state):
        if state["mode"] == "train" and state["train_step"] % self.log_steps == 0:
            self._print_message("FastEstimator-Train: step: {}; ".format(state["train_step"]), state.maps[0])

    def on_epoch_end(self, state):
        if state["mode"] == "eval":
            self._print_message("FastEstimator-Eval: step: {}; epoch: {}; ".format(state["train_step"], state["epoch"]),
                                state.maps[0])

    def on_end(self, state):
        self._print_message("FastEstimator-Finish: step: {}; ".format(state["train_step"]), state.maps[0])

    @staticmethod
    def _print_message(header, results):
        log_message = header
        for key, val in results.items():
            if hasattr(val, "numpy"):
                val = val.numpy()
            if isinstance(val, np.ndarray):
                log_message += "\n{}:\n{};".format(key, np.array2string(val, separator=','))
            else:
                log_message += "{}: {}; ".format(key, str(val))
        print(log_message)


class Accuracy(Trace):
    """Calculates accuracy for classification task and report it back to logger.

    Args:
        true_key (str): Name of the key that corresponds to ground truth in batch dictionary
        pred_key (str): Name of the key that corresponds to predicted score in batch dictionary
    """
    def __init__(self, true_key, pred_key, mode="eval", output_name="accuracy"):
        super().__init__(outputs=output_name, mode=mode)
        self.true_key = true_key
        self.pred_key = pred_key
        self.total = 0
        self.correct = 0
        self.output_name = output_name

    def on_epoch_begin(self, state):
        self.total = 0
        self.correct = 0

    def on_batch_end(self, state):
        groundtruth_label = np.array(state["batch"][self.true_key])
        if groundtruth_label.shape[-1] > 1 and len(groundtruth_label.shape) > 1:
            groundtruth_label = np.argmax(groundtruth_label, axis=-1)
        prediction_score = np.array(state["batch"][self.pred_key])
        binary_classification = prediction_score.shape[-1] == 1
        if binary_classification:
            prediction_label = np.round(prediction_score)
        else:
            prediction_label = np.argmax(prediction_score, axis=-1)
        assert prediction_label.size == groundtruth_label.size
        self.correct += np.sum(prediction_label.ravel() == groundtruth_label.ravel())
        self.total += len(prediction_label.ravel())

    def on_epoch_end(self, state):
        state[self.output_name] = self.correct / self.total


class ConfusionMatrix(Trace):
    """Computes confusion matrix between y_true and y_predict.

    Args:
        num_classes (int): Total number of classes of the confusion matrix.
        true_key (str): Name of the key that corresponds to ground truth in batch dictionary
        pred_key (str): Name of the key that corresponds to predicted score in batch dictionary
    """
    def __init__(self, true_key, pred_key, num_classes, mode="eval", output_name="confusion_matrix"):
        super().__init__(outputs=output_name, mode=mode)
        self.true_key = true_key
        self.pred_key = pred_key
        self.num_classes = num_classes
        self.confusion = None
        self.output_name = output_name

    def on_epoch_begin(self, state):
        self.confusion = None

    def on_batch_end(self, state):
        groundtruth_label = np.array(state["batch"][self.true_key])
        if groundtruth_label.shape[-1] > 1 and groundtruth_label.ndim > 1:
            groundtruth_label = np.argmax(groundtruth_label, axis=-1)
        prediction_score = np.array(state["batch"][self.pred_key])
        binary_classification = prediction_score.shape[-1] == 1
        if binary_classification:
            prediction_label = np.round(prediction_score)
        else:
            prediction_label = np.argmax(prediction_score, axis=-1)
        assert prediction_label.size == groundtruth_label.size
        batch_confusion = confusion_matrix(groundtruth_label, prediction_label, labels=list(range(0, self.num_classes)))
        if self.confusion is None:
            self.confusion = batch_confusion
        else:
            self.confusion += batch_confusion

    def on_epoch_end(self, state):
        state[self.output_name] = self.confusion


class Precision(Trace):
    """Calculates precision for classification task and report it back to logger.
    Args:
        true_key (str): Name of the keys in the ground truth label in data pipeline.
        pred_key (str, optional): If the network's output is a dictionary, name of the keys in predicted label.
                                  Default is `None`.
    """
    def __init__(self,
                 true_key,
                 pred_key=None,
                 labels=None,
                 pos_label=1,
                 average='auto',
                 sample_weight=None,
                 mode="eval",
                 output_name="precision"):
        super().__init__(outputs=output_name, mode=mode)
        self.true_key = true_key
        self.pred_key = pred_key
        self.labels = labels
        self.pos_label = pos_label
        self.average = average
        self.sample_weight = sample_weight
        self.y_true = []
        self.y_pred = []
        self.binary_classification = None
        self.output_name = output_name

    def on_epoch_begin(self, state):
        self.y_true = []
        self.y_pred = []

    def on_batch_end(self, state):
        groundtruth_label = np.array(state["batch"][self.true_key])
        if groundtruth_label.shape[-1] > 1 and len(groundtruth_label.shape) > 1:
            groundtruth_label = np.argmax(groundtruth_label, axis=-1)
        prediction_score = np.array(state["batch"][self.pred_key])
        binary_classification = prediction_score.shape[-1] == 1
        if binary_classification:
            prediction_label = np.round(prediction_score)
        else:
            prediction_label = np.argmax(prediction_score, axis=-1)
        assert prediction_label.size == groundtruth_label.size
        self.binary_classification = binary_classification or prediction_score.shape[-1] == 2
        self.y_pred.append(list(prediction_label.ravel()))
        self.y_true.append(list(groundtruth_label.ravel()))

    def on_epoch_end(self, state):
        if self.average == 'auto':
            if self.binary_classification:
                score = precision_score(np.ravel(self.y_true),
                                        np.ravel(self.y_pred),
                                        self.labels,
                                        self.pos_label,
                                        average='binary',
                                        sample_weight=self.sample_weight)
            else:
                score = precision_score(np.ravel(self.y_true),
                                        np.ravel(self.y_pred),
                                        self.labels,
                                        self.pos_label,
                                        average=None,
                                        sample_weight=self.sample_weight)
        else:
            score = precision_score(np.ravel(self.y_true),
                                    np.ravel(self.y_pred),
                                    self.labels,
                                    self.pos_label,
                                    self.average,
                                    self.sample_weight)
        state[self.output_name] = score


class Recall(Trace):
    """Calculates recall for classification task and report it back to logger.
    Args:
        true_key (str): Name of the keys in the ground truth label in data pipeline.
        pred_key (str, optional): If the network's output is a dictionary, name of the keys in predicted label.
                                  Default is `None`.
    """
    def __init__(self,
                 true_key,
                 pred_key=None,
                 labels=None,
                 pos_label=1,
                 average='auto',
                 sample_weight=None,
                 mode="eval",
                 output_name="recall"):
        super().__init__(outputs=output_name, mode=mode)
        self.true_key = true_key
        self.pred_key = pred_key
        self.labels = labels
        self.pos_label = pos_label
        self.average = average
        self.sample_weight = sample_weight
        self.y_true = []
        self.y_pred = []
        self.binary_classification = None
        self.output_name = output_name

    def on_epoch_begin(self, state):
        self.y_true = []
        self.y_pred = []

    def on_batch_end(self, state):
        groundtruth_label = np.array(state["batch"][self.true_key])
        if groundtruth_label.shape[-1] > 1 and len(groundtruth_label.shape) > 1:
            groundtruth_label = np.argmax(groundtruth_label, axis=-1)
        prediction_score = np.array(state["batch"][self.pred_key])
        binary_classification = prediction_score.shape[-1] == 1
        if binary_classification:
            prediction_label = np.round(prediction_score)
        else:
            prediction_label = np.argmax(prediction_score, axis=-1)
        assert prediction_label.size == groundtruth_label.size
        self.binary_classification = binary_classification or prediction_score.shape[-1] == 2
        self.y_pred.append(list(prediction_label.ravel()))
        self.y_true.append(list(groundtruth_label.ravel()))

    def on_epoch_end(self, state):
        if self.average == 'auto':
            if self.binary_classification:
                score = recall_score(np.ravel(self.y_true),
                                     np.ravel(self.y_pred),
                                     self.labels,
                                     self.pos_label,
                                     average='binary',
                                     sample_weight=self.sample_weight)
            else:
                score = recall_score(np.ravel(self.y_true),
                                     np.ravel(self.y_pred),
                                     self.labels,
                                     self.pos_label,
                                     average=None,
                                     sample_weight=self.sample_weight)
        else:
            score = recall_score(np.ravel(self.y_true),
                                 np.ravel(self.y_pred),
                                 self.labels,
                                 self.pos_label,
                                 self.average,
                                 self.sample_weight)
        state[self.output_name] = score


class F1Score(Trace):
    """Calculates F1 score for classification task and report it back to logger.
    Args:
        true_key (str): Name of the keys in the ground truth label in data pipeline.
        pred_key (str, optional): If the network's output is a dictionary, name of the keys in predicted label.
                                  Default is `None`.
    """
    def __init__(self,
                 true_key,
                 pred_key=None,
                 labels=None,
                 pos_label=1,
                 average='auto',
                 sample_weight=None,
                 mode="eval",
                 output_name="f1score"):
        super().__init__(outputs=output_name, mode=mode)
        self.true_key = true_key
        self.pred_key = pred_key
        self.labels = labels
        self.pos_label = pos_label
        self.average = average
        self.sample_weight = sample_weight
        self.y_true = []
        self.y_pred = []
        self.binary_classification = None
        self.output_name = output_name

    def on_epoch_begin(self, state):
        self.y_true = []
        self.y_pred = []

    def on_batch_end(self, state):
        groundtruth_label = np.array(state["batch"][self.true_key])
        if groundtruth_label.shape[-1] > 1 and len(groundtruth_label.shape) > 1:
            groundtruth_label = np.argmax(groundtruth_label, axis=-1)
        prediction_score = np.array(state["batch"][self.pred_key])
        binary_classification = prediction_score.shape[-1] == 1
        if binary_classification:
            prediction_label = np.round(prediction_score)
        else:
            prediction_label = np.argmax(prediction_score, axis=-1)
        self.binary_classification = binary_classification or prediction_score.shape[-1] == 2
        assert prediction_label.size == groundtruth_label.size
        self.y_pred.append(list(prediction_label.ravel()))
        self.y_true.append(list(groundtruth_label.ravel()))

    def on_epoch_end(self, state):
        if self.average == 'auto':
            if self.binary_classification:
                score = f1_score(np.ravel(self.y_true),
                                 np.ravel(self.y_pred),
                                 self.labels,
                                 self.pos_label,
                                 average='binary',
                                 sample_weight=self.sample_weight)
            else:
                score = f1_score(np.ravel(self.y_true),
                                 np.ravel(self.y_pred),
                                 self.labels,
                                 self.pos_label,
                                 average=None,
                                 sample_weight=self.sample_weight)
        else:
            score = f1_score(np.ravel(self.y_true),
                             np.ravel(self.y_pred),
                             self.labels,
                             self.pos_label,
                             self.average,
                             self.sample_weight)
        state[self.output_name] = score


class Dice(Trace):
    """Computes Dice score for binary classification between y_true and y_predict.

    Args:
        true_key (str): Name of the keys in the ground truth label in data pipeline.
        pred_key (str, optional): If the network's output is a dictionary, name of the keys in predicted label.
                                  Default is `None`.
    """
    def __init__(self, true_key, pred_key, threshold=0.5, mode="eval", output_name="dice"):
        super().__init__(outputs=output_name, mode=mode)
        self.true_key = true_key
        self.pred_key = pred_key
        self.smooth = 1e-7
        self.threshold = threshold
        self.dice = None
        self.output_name = output_name

    def on_epoch_begin(self, state):
        self.dice = None

    def on_batch_end(self, state):
        groundtruth_label = np.array(state["batch"][self.true_key])
        if groundtruth_label.shape[-1] > 1 and groundtruth_label.ndim > 1:
            groundtruth_label = np.argmax(groundtruth_label, axis=-1)
        prediction_score = np.array(state["batch"][self.pred_key])
        prediction_label = (prediction_score >= self.threshold).astype(np.int)
        intersection = np.sum(groundtruth_label * prediction_label, axis=(1, 2, 3))
        area_sum = np.sum(groundtruth_label, axis=(1, 2, 3)) + np.sum(prediction_label, axis=(1, 2, 3))
        dice = (2. * intersection + self.smooth) / (area_sum + self.smooth)
        if self.dice is None:
            self.dice = dice
        else:
            self.dice = np.append(self.dice, dice, axis=0)

    def on_epoch_end(self, state):
        state[self.output_name] = np.mean(self.dice)


class TerminateOnNaN(Trace):
    """
    End Training if a NaN value is detected. By default (inputs=None) it will monitor all loss values at the end of each
     batch. If one or more inputs are specified, it will only monitor those values. Inputs may be loss keys and/or the
     keys corresponding to the outputs of other traces (ex. accuracy) but then the other traces must be given before
     TerminateOnNaN in the trace list
    """
    def __init__(self, monitor_names=None):
        """
        Args:
            monitor_names (str, list): What key(s) to monitor for NaN values.
                                         - None (default) will monitor all loss values.
                                         - "*" will monitor all state keys and losses.
        """
        self.monitored_keys = monitor_names if monitor_names is None else set(monitor_names)
        super().__init__(inputs=self.monitored_keys)
        self.all_loss_keys = {}
        self.monitored_loss_keys = {}
        self.monitored_state_keys = {}

    def on_epoch_begin(self, state):
        self.all_loss_keys = set(self.network.epoch_losses)
        if self.monitored_keys is None:
            self.monitored_loss_keys = self.all_loss_keys
        elif "*" in self.monitored_keys:
            self.monitored_loss_keys = self.all_loss_keys
            self.monitored_state_keys = {"*"}
        else:
            self.monitored_loss_keys = self.monitored_keys & self.all_loss_keys
            self.monitored_state_keys = self.monitored_keys - self.monitored_loss_keys

    def on_batch_end(self, state):
        for key in self.monitored_loss_keys:
            loss = state["batch"][key]
            if tf.reduce_any(tf.math.is_nan(loss)):
                self.network.stop_training = True
                print("FastEstimator-TerminateOnNaN: NaN Detected in Loss: {}".format(key))
        for key in state.keys() if "*" in self.monitored_state_keys else self.monitored_state_keys:
            val = state.get(key, None)
            if self._is_floating(val) and tf.reduce_any(tf.math.is_nan(val)):
                self.network.stop_training = True
                print("FastEstimator-TerminateOnNaN: NaN Detected in: {}".format(key))

    def on_epoch_end(self, state):
        for key in state.keys() if "*" in self.monitored_state_keys else self.monitored_state_keys:
            val = state.get(key, None)
            if self._is_floating(val) and tf.reduce_any(tf.math.is_nan(val)):
                self.network.stop_training = True
                print("FastEstimator-TerminateOnNaN: NaN Detected in: {}".format(key))

    @staticmethod
    def _is_floating(val):
        return isinstance(val, float) or (isinstance(val, tf.Tensor)
                                          and val.dtype.is_floating) or (isinstance(val, np.ndarray)
                                                                         and np.issubdtype(val.dtype, np.floating))


class EarlyStopping(Trace):
    """
    Stop training when a monitored quantity has stopped improving.

    Args:
            monitor (str): Quantity to be monitored.
            min_delta (float): Minimum change in the monitored quantity
              to qualify as an improvement, i.e. an absolute
              change of less than min_delta, will count as no
              improvement.
            patience (int): Number of epochs with no improvement
              after which training will be stopped.
            verbose (int): verbosity mode.
            compare (str): One of `{"min", "max"}`. In `min` mode,
              training will stop when the quantity
              monitored has stopped decreasing; in `max`
              mode it will stop when the quantity
              monitored has stopped increasing.
            baseline (float): Baseline value for the monitored quantity.
              Training will stop if the model doesn't show improvement over the
              baseline.
            restore_best_weights (bool): Whether to restore model weights from
              the epoch with the best value of the monitored quantity.
              If False, the model weights obtained at the last step of
              training are used.
            mode (str): Restrict the trace to run only on given modes ('train', 'eval', 'test'). None will always
                        execute
    """
    def __init__(self,
                 monitor="loss",
                 min_delta=0,
                 patience=0,
                 verbose=0,
                 compare='min',
                 baseline=None,
                 restore_best_weights=False,
                 mode='eval'):
        super().__init__(inputs=monitor, mode=mode)

        if len(self.inputs) != 1:
            raise ValueError("EarlyStopping supports only one monitor key")
        if compare not in ['min', 'max']:
            raise ValueError("compare_mode can only be `min` or `max`")

        self.monitored_key = monitor
        self.min_delta = abs(min_delta)
        self.wait = 0
        self.best = 0
        self.patience = patience
        self.baseline = baseline
        self.verbose = verbose
        self.restore_best_weights = restore_best_weights
        self.best_weights = None
        if compare == 'min':
            self.monitor_op = np.less
            self.min_delta *= -1
        else:
            self.monitor_op = np.greater

    def on_begin(self, state):
        self.wait = 0
        if self.baseline is not None:
            self.best = self.baseline
        else:
            self.best = np.Inf if self.monitor_op == np.less else -np.Inf

    def on_epoch_end(self, state):
        current = state.get(self.monitored_key, None) or state['batch'].get(self.monitored_key, None)
        if current is None:
            return
        if self.monitor_op(current - self.min_delta, self.best):
            self.best = current
            self.wait = 0
            if self.restore_best_weights:
                self.best_weights = dict(map(lambda x: (x[0], x[1].get_weights()), self.network.model.items()))
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.network.stop_training = True
                if self.restore_best_weights:
                    if self.verbose > 0:
                        print('FastEstimator-EarlyStopping: Restoring best model weights')
                    for name, model in self.network.model.items():
                        model.set_weights(self.best_weights[name])
                print("FastEstimator-EarlyStopping: '{}' triggered an early stop. Its best value was {} at epoch {}\
                      ".format(self.monitored_key, self.best, state['epoch'] - self.wait))


class CSVLogger(Trace):
    def __init__(self, filename, monitor_names=None, separator=", ", append=False, mode="eval"):
        self.keys = monitor_names if monitor_names is None else list(monitor_names)
        super().__init__(inputs="*" if self.keys is None else monitor_names, mode=mode)
        self.separator = separator
        self.file = open(filename, 'a' if append else 'w')
        self.file_empty = os.stat(filename).st_size == 0

    def on_epoch_end(self, state):
        if self.keys is None:
            self._infer_keys(state)
        vals = [state.get(key, "") for key in self.keys]
        vals = [str(val.numpy()) if hasattr(val, "numpy") else str(val) for val in vals]
        self.file.write("\n" + self.separator.join(vals))

    def on_end(self, state):
        self.file.flush()
        self.file.close()

    def _infer_keys(self, state):
        monitored_keys = []
        for key, val in state.items():
            if isinstance(val, str) or is_number(val):
                monitored_keys.append(key)
            elif hasattr(val, "numpy") and len(val.numpy().shape) == 1:
                monitored_keys.append(key)
        self.keys = sorted(monitored_keys)
        if self.file_empty:
            self.file.write(self.separator.join(self.keys))
            self.file_empty = False


class TensorBoard(Trace):
    """
    Output data for use in TensorBoard.
    """
    def __init__(
            self,
            log_dir='logs',
            histogram_freq=0,
            write_graph=True,
            write_images=False,
            update_freq='epoch',
            profile_batch=2,
            embeddings_freq=0,
            embeddings_metadata=None,
    ):
        """
        Args:
            log_dir (str): the path of the directory where to save the log files to be parsed by TensorBoard.
            histogram_freq (int): frequency (in epochs) at which to compute activation and weight histograms for the
                                    layers of the model. If set to 0, histograms won't be computed.
            write_graph (bool): whether to visualize the graph in TensorBoard. The log file can become quite large when
                            write_graph is set to True.
            write_images (bool, str, list): If True will write model weights to visualize as an image in TensorBoard. If
                                            a string or list of strings is provided, the corresponding keys will be
                                            written to tensorboard images. To get weights and specific keys use
                                            [True, 'key1', 'key2',...]
            update_freq (str, int): 'batch' or 'epoch' or integer. When using 'batch', writes the losses and metrics to
                            TensorBoard after each batch. The same applies for 'epoch'. If using an integer, let's say
                            1000, the callback will write the metrics and losses to TensorBoard every 1000 samples. Note
                            that writing too frequently to TensorBoard can slow down your training.
            profile_batch (int): Which batch to run profiling on. 0 to disable. Note that FE batch numbering starts from
                                 0 rather than 1
            embeddings_freq (int): frequency (in epochs) at which embedding layers will be visualized. If set to 0,
                                    embeddings won't be visualized.
            embeddings_metadata (str, dict): a dictionary which maps layer name to a file name in which metadata for
                                            this embedding layer is saved. See the details about metadata files format.
                                            In case if the same metadata file is used for all embedding layers, string
                                            can be passed.
        """
        super().__init__(inputs="*")
        current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.train_log_dir = os.path.join(os.path.join(log_dir, current_time), 'train')
        eval_log_dir = os.path.join(os.path.join(log_dir, current_time), 'eval')
        self.summary_writers = {
            'train': tf.summary.create_file_writer(self.train_log_dir),
            'eval': tf.summary.create_file_writer(eval_log_dir)
        }
        self.update_freq = 1 if update_freq == 'batch' else update_freq
        assert (self.update_freq == 'epoch' or (isinstance(self.update_freq, int) and self.update_freq > 0)), \
            "TensorBoard update_freq must be either 'epoch', 'batch', or a positive integer"
        self.ignore_keys = {'mode', 'epoch', 'train_step', 'batch_idx', 'batch_size', 'batch'}
        self.write_graph = write_graph
        self.write_images = {write_images} if isinstance(write_images, (str, bool)) else set(write_images)
        self.histogram_freq = histogram_freq
        self.profile_batch = profile_batch
        self.is_tracing = False
        self.embeddings_freq = embeddings_freq
        self.embeddings_metadata = embeddings_metadata

    def on_begin(self, state):
        if self.write_graph:
            with self.summary_writers['train'].as_default():
                with summary_ops_v2.always_record_summaries():
                    summary_ops_v2.graph(backend.get_graph(), step=0)
                    for name, model in self.network.model.items():
                        summary_writable = (model._is_graph_network or model.__class__.__name__ == 'Sequential')
                        if summary_writable:
                            summary_ops_v2.keras_model(name, model, step=0)
        if self.embeddings_freq:
            self._configure_embeddings()

    def on_batch_end(self, state):
        if state['mode'] != 'train':
            return
        if self.is_tracing:
            self._log_trace(state['train_step'])
        elif state['train_step'] == self.profile_batch - 1:
            self._enable_trace()
        if self.update_freq == 'epoch' or state['train_step'] % self.update_freq != 0:
            return
        with self.summary_writers[state['mode']].as_default():
            for key in state.keys() - self.ignore_keys:
                val = state[key]
                if is_number(val):
                    tf.summary.scalar("batch_" + key, val, step=state['train_step'])
            for key in self.write_images - {True, False}:
                data = state.get(key)
                if data is not None:
                    tf.summary.image(key, data, step=state['train_step'])

    def on_epoch_end(self, state):
        with self.summary_writers[state['mode']].as_default():
            for key in state.keys() - self.ignore_keys:
                val = state[key]
                if is_number(val):
                    tf.summary.scalar("epoch_" + key, val, step=state['epoch'])
            for key in self.write_images - {True, False}:
                data = state.get(key)
                if data is not None:
                    tf.summary.image(key, data, step=state['epoch'])
            if state['mode'] == 'train' and self.histogram_freq and state['epoch'] % self.histogram_freq == 0:
                self._log_weights(epoch=state['epoch'])
            if state['mode'] == 'train' and self.embeddings_freq and state['epoch'] % self.embeddings_freq == 0:
                self._log_embeddings(state)

    def on_end(self, state):
        if self.is_tracing:
            self._log_trace(state['train_step'])
        for writer in self.summary_writers.values():
            writer.close()

    def _enable_trace(self):
        summary_ops_v2.trace_on(graph=True, profiler=True)
        self.is_tracing = True

    def _log_trace(self, global_batch_idx):
        with self.summary_writers['train'].as_default(), summary_ops_v2.always_record_summaries():
            summary_ops_v2.trace_export(name='batch_{}'.format(global_batch_idx),
                                        step=global_batch_idx,
                                        profiler_outdir=self.train_log_dir)
        self.is_tracing = False

    def _log_embeddings(self, state):
        for model_name, model in self.network.model.items():
            embeddings_ckpt = os.path.join(self.train_log_dir,
                                           '{}_embedding.ckpt-{}'.format(model_name, state['epoch']))
            model.save_weights(embeddings_ckpt)

    def _log_weights(self, epoch):
        # Similar to TF implementation, but multiple models
        writer = self.summary_writers['train']
        with writer.as_default(), summary_ops_v2.always_record_summaries():
            for model_name, model in self.network.model.items():
                for layer in model.layers:
                    for weight in layer.weights:
                        weight_name = weight.name.replace(':', '_')
                        weight_name = "{}_{}".format(model_name, weight_name)
                        with tfops.init_scope():
                            weight = backend.get_value(weight)
                        summary_ops_v2.histogram(weight_name, weight, step=epoch)
                        if True in self.write_images:
                            self._log_weight_as_image(weight, weight_name, epoch)
        writer.flush()

    @staticmethod
    def _log_weight_as_image(weight, weight_name, epoch):
        """ Logs a weight as a TensorBoard image.
            Implementation from tensorflow codebase, would have invoked theirs directly but they didn't make it a static
            method
        """
        w_img = array_ops.squeeze(weight)
        shape = backend.int_shape(w_img)
        if len(shape) == 1:  # Bias case
            w_img = array_ops.reshape(w_img, [1, shape[0], 1, 1])
        elif len(shape) == 2:  # Dense layer kernel case
            if shape[0] > shape[1]:
                w_img = array_ops.transpose(w_img)
                shape = backend.int_shape(w_img)
            w_img = array_ops.reshape(w_img, [1, shape[0], shape[1], 1])
        elif len(shape) == 3:  # ConvNet case
            if backend.image_data_format() == 'channels_last':
                # Switch to channels_first to display every kernel as a separate
                # image.
                w_img = array_ops.transpose(w_img, perm=[2, 0, 1])
                shape = backend.int_shape(w_img)
            w_img = array_ops.reshape(w_img, [shape[0], shape[1], shape[2], 1])
        shape = backend.int_shape(w_img)
        # Not possible to handle 3D convnets etc.
        if len(shape) == 4 and shape[-1] in [1, 3, 4]:
            summary_ops_v2.image(weight_name, w_img, step=epoch)

    def _configure_embeddings(self):
        """Configure the Projector for embeddings.
        Implementation from tensorflow codebase, but supports multiple models
        """
        try:
            # noinspection PyPackageRequirements
            from tensorboard.plugins import projector
        except ImportError:
            raise ImportError('Failed to import TensorBoard. Please make sure that '
                              'TensorBoard integration is complete."')
        config = projector.ProjectorConfig()
        for model_name, model in self.network.model.items():
            for layer in model.layers:
                if isinstance(layer, embeddings.Embedding):
                    embedding = config.embeddings.add()
                    embedding.tensor_name = layer.embeddings.name

                    if self.embeddings_metadata is not None:
                        if isinstance(self.embeddings_metadata, str):
                            embedding.metadata_path = self.embeddings_metadata
                        else:
                            if layer.name in embedding.metadata_path:
                                embedding.metadata_path = self.embeddings_metadata.pop(layer.name)

        if self.embeddings_metadata:
            raise ValueError('Unrecognized `Embedding` layer names passed to '
                             '`keras.callbacks.TensorBoard` `embeddings_metadata` '
                             'argument: ' + str(self.embeddings_metadata))

        class DummyWriter(object):
            """Dummy writer to conform to `Projector` API."""
            def __init__(self, logdir):
                self.logdir = logdir

            def get_logdir(self):
                return self.logdir

        writer = DummyWriter(self.train_log_dir)
        projector.visualize_embeddings(writer, config)


class ModelSaver(Trace):
    """Save trained model in hdf5 format.

    Args:
        model_name (str): The name of FE model.
        save_dir (str): The directory to save the trained models.
        save_best (bool, str): best model saving monitor name. If True, the model loss is used.
        save_best_mode: Can be `'min'`, `'max'`, or `'auto'`.
        save_freq: Number of epochs to save models. Cannot be used with `save_best_only=True`.
    """
    def __init__(self,
                 model_name,
                 save_dir,
                 save_best=False,
                 save_best_mode='min',
                 save_freq=1):
        if isinstance(save_best, str):
            super().__init__(inputs=save_best)
        else:
            super().__init__()
        self.model_name = model_name
        self.save_dir = save_dir
        self.save_best = save_best
        self.save_best_mode = save_best_mode
        self.save_freq = save_freq
        assert isinstance(self.save_freq, int), "save_freq must be integer"
        if self.save_best_mode == "min":
            self.best = np.Inf
            self.monitor_op = np.less
        elif self.save_best_mode == "max":
            self.best = -np.Inf
            self.monitor_op = np.greater
        else:
            raise ValueError("save_best_mode must be either 'min' or 'max'")
        self.model = None

    def on_begin(self, state):
        if self.save_dir:
            self.save_dir = os.path.normpath(self.save_dir)
            os.makedirs(self.save_dir, exist_ok=True)
        self.model = self.network.model[self.model_name]
        if self.save_best is True:
            self.save_best = self.model.loss_name

    def on_epoch_end(self, state):
        if self.save_best:
            if state["mode"] == "eval" and self.monitor_op(state[self.save_best], self.best):
                self.best = state[self.save_best]
                self._save_model("{}_best_{}.h5".format(self.model_name, self.save_best))
        elif state["mode"] == "train" and state["epoch"] % self.save_freq == 0:
            self._save_model("{}_epoch_{}_step_{}.h5".format(self.model_name, state['epoch'], state['train_step']))

    def _save_model(self, name):
        if self.save_dir:
            save_path = os.path.join(self.save_dir, name)
            self.model.save(save_path, include_optimizer=False)
            print("FastEstimator-ModelSaver: Saving model to {}".format(save_path))

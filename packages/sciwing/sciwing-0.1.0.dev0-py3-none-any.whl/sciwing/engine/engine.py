from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
from wasabi import Printer
from typing import Iterator, Callable, Any, List, Optional, Dict
from sciwing.meters.loss_meter import LossMeter
from tensorboardX import SummaryWriter
from sciwing.metrics.BaseMetric import BaseMetric
import numpy as np
import time
import logging
from torch.utils.data._utils.collate import default_collate
import torch
from sciwing.utils.tensor_utils import move_to_device
from copy import deepcopy
from sciwing.utils.class_nursery import ClassNursery
import logzero
import hashlib
import pathlib

try:
    import wandb
except ImportError:
    wandb = None


class Engine(ClassNursery):
    def __init__(
        self,
        model: nn.Module,
        train_dataset: Dataset,
        validation_dataset: Dataset,
        test_dataset: Dataset,
        optimizer: optim,
        batch_size: int,
        save_dir: str,
        num_epochs: int,
        save_every: int,
        log_train_metrics_every: int,
        metric: BaseMetric,
        experiment_name: Optional[str] = None,
        experiment_hyperparams: Optional[Dict[str, Any]] = None,
        tensorboard_logdir: str = None,
        track_for_best: str = "loss",
        collate_fn: Callable[[List[Any]], List[Any]] = default_collate,
        device=torch.device("cpu"),
        gradient_norm_clip_value: Optional[float] = 5.0,
        lr_scheduler: Optional[torch.optim.lr_scheduler._LRScheduler] = None,
        use_wandb: bool = False,
    ):
        """ Engine runs the models end to end. It iterates through the train dataset and passes
        it through the model. During training it helps in tracking a lot of parameters for the run
        and saving the parameters. It also reports validation and test parameters from time to time.
        Many utilities required for end-end running of the model is here.

        Parameters
        ----------
        model : nn.Module
            A pytorch module defining a model to be run
        train_dataset : Dataset
            This represents the training dataset.
            Anything that confirms to the Dataset protocol. This can be any class that implements
            the ``__get_item__`` and ``__len__`` as required by pytorch dataset
        validation_dataset : Dataset
            This represents the validation dataset.
            Anything that confirms to the Dataset protocol. This can be any class that implements
            the ``__get_item__`` and ``__len__`` as required by pytorch dataset
        test_dataset : Dataset
            This represents the test dataset
            Anything that confirms to the Dataset protocol. This can be any class that implements
            the ``__get_item__`` and ``__len__`` as required by pytorch dataset
        optimizer : torch.optim
            Any Optimizer object instantiated using  ``torch.optim``
        batch_size : int
            Batch size for the dataset. The same batch size is used for ``train``, ``valid``
            and ``test`` dataset
        save_dir : int
            The experiments are saved in ``save_dir``. We save checkpoints, the best model,
            logs and other information into the save dir
        num_epochs : int
            The number of epochs to run the training
        save_every : int
            The model will be checkpointed every ``save_every`` number of iterations
        log_train_metrics_every : int
            The train metrics will be reported every ``log_train_metrics_every`` iterations
            during training
        metric : BaseMetric
            Anything that is an instance of ``BaseMetric``
        experiment_name : str
            The experiment should be given a name for ease of tracking. Instead experiment
            name is not given, we generate a unique 10 digit sha for the experiment.
        experiment_hyperparams : Dict[str, Any]
            This is mostly used for tracking the different hyper-params of the experiment
            being run. This may be used by ``wandb`` to save the hyper-params
        tensorboard_logdir : str
            The directory where all the tensorboard runs are stored. If ``None`` is passed
            then it defaults to the tensorboard default of storing the log in the current directory.
        track_for_best : str
            Which metric should be tracked for deciding the best model?. Anything that
            the metric emits and is a single value can be used for tracking. The defauly value
            is ``loss``. If its loss, then the best value will be the lowest one. For some
            other metrics like ``macro_fscore``, the best metric might be the one that has the highest
            value
        collate_fn : Callable[[List[Any]], List[Any]]
            Collates the different examples into a single batch of examples.
            This is the same terminology adopted from ``pytorch``. There is no different
        device : torch.device
            The device on which the model will be placed. If this is "cpu", then the model
            and the tensors will all be on cpu. If this is "cuda:0", then the model and
            the tensors will be placed on cuda device 0. You can mention any other cuda
            device that is suitable for your environment
        gradient_norm_clip_value : float
            To avoid gradient explosion, the gradients of the norm will be clipped
            if the gradient norm exceeds this value
        lr_scheduler : torch.optim.lr_scheduler
            Any pytorch ``lr_scheduler`` can be used for reducing the learning rate
            if the performance on the validation set reduces.
        use_wandb : bool
            wandb or weights and biases is a tool that is used to track experiments
            online. Sciwing comes with inbuilt functionality to track experiments
            on weights and biases
        """

        if isinstance(device, str):
            device = torch.device(device)

        self.model = model
        self.train_dataset = train_dataset
        self.validation_dataset = validation_dataset
        self.test_dataset = test_dataset
        self.optimizer = optimizer
        self.batch_size = batch_size
        self.save_dir = pathlib.Path(save_dir)
        self.num_epochs = num_epochs
        self.msg_printer = Printer()
        self.save_every = save_every
        self.log_train_metrics_every = log_train_metrics_every
        self.tensorboard_logdir = tensorboard_logdir
        self.metric = metric
        self.summaryWriter = SummaryWriter(log_dir=tensorboard_logdir)
        self.track_for_best = track_for_best
        self.collate_fn = collate_fn
        self.device = device
        self.best_track_value = None
        self.set_best_track_value(self.best_track_value)
        self.gradient_norm_clip_value = gradient_norm_clip_value
        self.lr_scheduler = lr_scheduler
        self.lr_scheduler_is_plateau = isinstance(
            self.lr_scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau
        )
        self.use_wandb = wandb and use_wandb

        if experiment_name is None:
            hash_ = hashlib.sha1()
            hash_.update(str(time.time()).encode("utf-8"))
            digest = hash_.hexdigest()
            experiment_name = digest[:10]

        self.experiment_name = experiment_name
        self.experiment_hyperparams = experiment_hyperparams or {}

        if self.use_wandb:
            wandb.init(
                project="project-scwing",
                name=self.experiment_name,
                config=self.experiment_hyperparams,
            )

        if not self.save_dir.is_dir():
            self.save_dir.mkdir(parents=True)

        self.num_workers = 0
        self.model.to(self.device)

        self.train_loader = self.get_loader(self.train_dataset)
        self.validation_loader = self.get_loader(self.validation_dataset)
        self.test_loader = self.get_loader(self.test_dataset)

        # refresh the iters at the beginning of every epoch
        self.train_iter = None
        self.validation_iter = None
        self.test_iter = None

        # initializing loss meters
        self.train_loss_meter = LossMeter()
        self.validation_loss_meter = LossMeter()

        # get metric calculators
        self.train_metric_calc = deepcopy(metric)
        self.validation_metric_calc = deepcopy(metric)
        self.test_metric_calc = deepcopy(metric)

        self.msg_printer.divider("ENGINE STARTING")
        self.msg_printer.info(f"Number of training examples {len(self.train_dataset)}")
        self.msg_printer.info(
            f"Number of validation examples {len(self.validation_dataset)}"
        )
        self.msg_printer.info(
            f"Number of test examples {0}".format(len(self.test_dataset))
        )
        time.sleep(3)

        # get the loggers ready
        self.train_log_filename = self.save_dir.joinpath("train.log")
        self.validation_log_filename = self.save_dir.joinpath("validation.log")
        self.test_log_filename = self.save_dir.joinpath("test.log")

        self.train_logger = logzero.setup_logger(
            name="train-logger", logfile=self.train_log_filename, level=logging.INFO
        )
        self.validation_logger = logzero.setup_logger(
            name="valid-logger",
            logfile=self.validation_log_filename,
            level=logging.INFO,
        )
        self.test_logger = logzero.setup_logger(
            name="test-logger", logfile=self.test_log_filename, level=logging.INFO
        )

        if self.lr_scheduler_is_plateau:
            if self.best_track_value == "loss" and self.lr_scheduler.mode == "max":
                self.msg_printer.warn(
                    "You are optimizing loss and lr schedule mode is max instead of min"
                )
            if (
                self.best_track_value == "macro_fscore"
                and self.lr_scheduler.mode == "min"
            ):
                self.msg_printer.warn(
                    f"You are optimizing for macro_fscore and lr scheduler mode is min instead of max"
                )
            if (
                self.best_track_value == "micro_fscore"
                and self.lr_scheduler.mode == "min"
            ):
                self.msg_printer.warn(
                    f"You are optimizing for micro_fscore and lr scheduler mode is min instead of max"
                )

    def get_loader(self, dataset: Dataset) -> DataLoader:
        """ Returns the DataLoader for the Dataset

        Parameters
        ----------
        dataset : Dataset

        Returns
        -------
        DataLoader
            A pytorch DataLoader

        """
        loader = DataLoader(
            dataset=dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            collate_fn=self.collate_fn,
            pin_memory=True,
        )
        return loader

    def is_best_lower(self, current_best=None):
        """ Returns True if the current value of the metric is lower than the best metric.
        This is useful for tracking metrics like loss where, lower the value, the better it is

        Parameters
        ----------
        current_best : float
            The current value for the metric that is being tracked

        Returns
        -------
        bool


        """
        return True if current_best < self.best_track_value else False

    def is_best_higher(self, current_best=None):
        """ Returns ``True`` if the current value of the metric is HIGHER than the best metric.
        This is useful for tracking metrics like FSCORE where, higher the value, the better it is

        Parameters
        ----------
        current_best : float
            The current value for the metric that is being tracked

        Returns
        -------
        bool
        """
        return True if current_best >= self.best_track_value else False

    def set_best_track_value(self, current_best=None):
        """ Set the best value of the value being tracked

        Parameters
        ----------
        current_best : float
            The current value that is best

        Returns
        -------

        """
        if self.track_for_best == "loss":
            self.best_track_value = np.inf if current_best is None else current_best
        elif self.track_for_best == "macro_fscore":
            self.best_track_value = 0 if current_best is None else current_best
        elif self.track_for_best == "micro_fscore":
            self.best_track_value = 0 if current_best is None else current_best

    def run(self):
        """
        Run the engine
        :return:
        """
        for epoch_num in range(self.num_epochs):
            self.train_epoch(epoch_num)
            self.validation_epoch(epoch_num)

        self.test_epoch(epoch_num)

    def train_epoch(self, epoch_num: int):
        """
        Run the training for one epoch
        :param epoch_num: type: int
        The current epoch number
        """

        # refresh everything necessary before training begins
        num_iterations = 0
        train_iter = self.get_iter(self.train_loader)
        self.train_loss_meter.reset()
        self.train_metric_calc.reset()
        self.model.train()

        self.msg_printer.info("starting training epoch")
        while True:
            try:
                # N*T, N * 1, N * 1
                iter_dict = next(train_iter)
                iter_dict = move_to_device(obj=iter_dict, cuda_device=self.device)
                labels = iter_dict["label"]
                batch_size = labels.size()[0]

                model_forward_out = self.model(
                    iter_dict, is_training=True, is_validation=False, is_test=False
                )
                self.train_metric_calc.calc_metric(
                    iter_dict=iter_dict, model_forward_dict=model_forward_out
                )

                try:
                    self.optimizer.zero_grad()
                    loss = model_forward_out["loss"]
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(
                        self.model.parameters(), max_norm=self.gradient_norm_clip_value
                    )
                    self.optimizer.step()
                    self.train_loss_meter.add_loss(loss.item(), batch_size)

                except KeyError:
                    self.msg_printer.fail(
                        "The model output dictionary does not have "
                        "a key called loss. Please check to have "
                        "loss in the model output"
                    )
                num_iterations += 1
                if (num_iterations + 1) % self.log_train_metrics_every == 0:
                    metrics = self.train_metric_calc.report_metrics()
                    print(metrics)
            except StopIteration:
                self.train_epoch_end(epoch_num)
                break

    def train_epoch_end(self, epoch_num: int):
        """ Performs house-keeping at the end of a training epoch

        At the end of the training epoch, it does some house-keeping. It reports the average loss, the
        average metric and other information.

        Parameters
        ----------
        epoch_num : int
            The current epoch number (0 based)

        """
        self.msg_printer.divider("Training end @ Epoch {0}".format(epoch_num + 1))
        average_loss = self.train_loss_meter.get_average()
        self.msg_printer.text("Average Loss: {0}".format(average_loss))
        self.train_logger.info(
            "Average loss @ Epoch {0} - {1}".format(epoch_num + 1, average_loss)
        )
        metric = self.train_metric_calc.get_metric()

        if self.use_wandb:
            wandb.log({"train_loss": average_loss}, step=epoch_num + 1)
            if self.track_for_best != "loss":
                wandb.log(
                    {f"train_{self.track_for_best}": metric[self.track_for_best]},
                    step=epoch_num + 1,
                )

        # save the model after every `self.save_every` epochs
        if (epoch_num + 1) % self.save_every == 0:
            torch.save(
                {
                    "epoch_num": epoch_num,
                    "optimizer_state": self.optimizer.state_dict(),
                    "model_state": self.model.state_dict(),
                    "loss": average_loss,
                },
                self.save_dir.joinpath(f"model_epoch_{epoch_num+1}.pt"),
            )

        # log loss to tensor board
        self.summaryWriter.add_scalars(
            "train_validation_loss",
            {"train_loss": average_loss or np.inf},
            epoch_num + 1,
        )

    def validation_epoch(self, epoch_num: int):
        """ Runs one validation epoch on the validation dataset

        Parameters
        ----------
        epoch_num : int
        0-based epoch number

        """
        self.model.eval()
        valid_iter = iter(self.validation_loader)
        self.validation_loss_meter.reset()
        self.validation_metric_calc.reset()

        while True:
            try:
                iter_dict = next(valid_iter)
                iter_dict = move_to_device(obj=iter_dict, cuda_device=self.device)
                labels = iter_dict["label"]
                batch_size = labels.size(0)

                with torch.no_grad():
                    model_forward_out = self.model(
                        iter_dict, is_training=False, is_validation=True, is_test=False
                    )
                loss = model_forward_out["loss"]
                self.validation_loss_meter.add_loss(loss, batch_size)
                self.validation_metric_calc.calc_metric(
                    iter_dict=iter_dict, model_forward_dict=model_forward_out
                )
            except StopIteration:
                self.validation_epoch_end(epoch_num)
                break

    def validation_epoch_end(self, epoch_num: int):
        """Performs house-keeping at the end of validation epoch

        Parameters
        ----------
        epoch_num : int
            The current epoch number
        """

        self.msg_printer.divider(f"Validation @ Epoch {epoch_num+1}")

        metric_report = self.validation_metric_calc.report_metrics()

        average_loss = self.validation_loss_meter.get_average()
        print(metric_report)

        self.msg_printer.text(f"Average Loss: {average_loss}")

        self.validation_logger.info(
            f"Validation Loss @ Epoch {epoch_num+1} - {average_loss}"
        )

        if self.use_wandb:
            wandb.log({"validation_loss": average_loss}, step=epoch_num + 1)
            metric = self.validation_metric_calc.get_metric()
            if self.track_for_best != "loss":
                wandb.log(
                    {f"validation_{self.track_for_best}": metric[self.track_for_best]},
                    step=epoch_num + 1,
                )

        self.summaryWriter.add_scalars(
            "train_validation_loss",
            {"validation_loss": average_loss or np.inf},
            epoch_num + 1,
        )

        is_best: bool = None
        value_tracked: str = None
        if self.track_for_best == "loss":
            value_tracked = average_loss
            is_best = self.is_best_lower(average_loss)
        elif (
            self.track_for_best == "micro_fscore"
            or self.track_for_best == "macro_fscore"
        ):
            value_tracked = self.validation_metric_calc.get_metric()[
                self.track_for_best
            ]
            is_best = self.is_best_higher(current_best=value_tracked)

        if is_best:
            self.set_best_track_value(current_best=value_tracked)
            self.msg_printer.good(f"Found best model @ epoch {epoch_num + 1}")
            torch.save(
                {
                    "epoch_num": epoch_num,
                    "optimizer_state": self.optimizer.state_dict(),
                    "model_state": self.model.state_dict(),
                    "loss": average_loss,
                },
                self.save_dir.joinpath("best_model.pt"),
            )

    def test_epoch(self, epoch_num: int):
        """Runs the test epoch for ``epoch_num``

        Loads the best model that is saved during the training
        and runs the test dataset.

        Parameters
        ----------
        epoch_num : int
            zero based epoch number for which the test dataset is run
            This is after the last training epoch.

        """
        self.msg_printer.divider("Running on test batch")
        self.load_model_from_file(self.save_dir.joinpath("best_model.pt"))
        self.model.eval()
        test_iter = iter(self.test_loader)
        while True:
            try:
                iter_dict = next(test_iter)
                iter_dict = move_to_device(obj=iter_dict, cuda_device=self.device)

                with torch.no_grad():
                    model_forward_out = self.model(
                        iter_dict, is_training=False, is_validation=False, is_test=True
                    )
                self.test_metric_calc.calc_metric(
                    iter_dict=iter_dict, model_forward_dict=model_forward_out
                )
            except StopIteration:
                self.test_epoch_end(epoch_num)
                break

    def test_epoch_end(self, epoch_num: int):
        """ Performs house-keeping at the end of the test epoch

        It reports the metric that is being traced at the end
        of the test epoch

        Parameters
        ----------
        epoch_num : int
            Epoch num after which the test dataset is run

        """
        metric_report = self.test_metric_calc.report_metrics()
        precision_recall_fmeasure = self.test_metric_calc.get_metric()
        self.msg_printer.divider("Test @ Epoch {0}".format(epoch_num + 1))
        print(metric_report)
        self.test_logger.info(
            f"Test Metrics @ Epoch {epoch_num+1} - {precision_recall_fmeasure}"
        )
        if self.use_wandb:
            wandb.log({"test_metrics": str(precision_recall_fmeasure)})

    def get_train_dataset(self):
        """ Returns the train dataset of the experiment

        Returns
        -------
        Dataset
            Anything that conforms to the pytorch style dataset.

        """
        return self.train_dataset

    def get_validation_dataset(self):
        """ Returns the validation dataset of the experiment

        Returns
        -------
        Dataset
            Anything that conforms to the pytorch style dataset.

        """
        return self.validation_dataset

    def get_test_dataset(self):
        """ Returns the test dataset of the experiment

        Returns
        -------
        Dataset
            Anything that conforms to the pytorch style dataset.

        """
        return self.test_dataset

    @staticmethod
    def get_iter(loader: DataLoader) -> Iterator:
        """ Returns the iterator for a pytorch data loader.

        The ``loader`` is a pytorch DataLoader that iterates
        over the dataset in batches and employs many strategies to do
        so. We want an iterator that returns the dataset in batches.
        The end of the iterator would signify the end of an epoch
        and then we can use that information to perform house-keeping.


        Parameters
        ----------
        loader : DataLoader
            a pytorch data loader

        Returns
        -------
        Iterator
            An iterator over the data loader
        """
        iterator = iter(loader)
        return iterator

    def load_model_from_file(self, filename: str):
        self.msg_printer.divider("LOADING MODEL FROM FILE")
        with self.msg_printer.loading(f"Loading Pytorch Model from file {filename}"):
            model_chkpoint = torch.load(filename)

        self.msg_printer.good("Finished Loading the Model")

        model_state = model_chkpoint["model_state"]
        self.model.load_state_dict(model_state)

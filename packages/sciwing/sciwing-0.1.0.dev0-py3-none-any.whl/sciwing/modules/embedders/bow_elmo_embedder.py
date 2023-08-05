import torch
from allennlp.commands.elmo import ElmoEmbedder
import wasabi
from typing import List, Iterable, Dict, Any
import torch.nn as nn
from sciwing.utils.class_nursery import ClassNursery


class BowElmoEmbedder(nn.Module, ClassNursery):
    def __init__(
        self,
        emb_dim: int = 1024,
        dropout_value: float = 0.0,
        layer_aggregation: str = "sum",
        cuda_device_id: int = -1,
    ):
        """ Bag of words Elmo Embedder which aggregates elmo embedding for every token

        Parameters
        ----------
        emb_dim : int
            Embedding dimension
        dropout_value : float
            Any input dropout to be applied to the embeddings
        layer_aggregation : str
            You can chose one of ``[sum, average, last, first]``
            which decides how to aggregate different layers of ELMO. ELMO produces three
            layers of representations

            sum
                Representations from different layers are summed
            average
                Representations from different layers are average
            last
                Representations from last layer is considered
            first
                Representations from first layer is considered

        cuda_device_id : int
            Cuda device id on which representations will be transferred
            -1 indicates cpu
        """
        super(BowElmoEmbedder, self).__init__()
        self.emb_dim = emb_dim
        self.dropout_value = dropout_value
        self.layer_aggregation_type = layer_aggregation
        self.allowed_layer_aggregation_types = ["sum", "average", "last", "first"]
        self.cuda_device_id = cuda_device_id
        self.device = (
            torch.device("cpu")
            if cuda_device_id < 0
            else torch.device(f"cuda:{cuda_device_id}")
        )
        self.msg_printer = wasabi.Printer()

        assert (
            self.layer_aggregation_type in self.allowed_layer_aggregation_types
        ), self.msg_printer.fail(
            f"For bag of words elmo encoder, the allowable aggregation "
            f"types are {self.allowed_layer_aggregation_types}. You passed {self.layer_aggregation_type}"
        )

        # load the elmo embedders
        with self.msg_printer.loading("Creating Elmo object"):
            self.elmo = ElmoEmbedder(cuda_device=self.cuda_device_id)
        self.msg_printer.good("Finished Loading Elmo object")

    def forward(self, iter_dict: Dict[str, Any]) -> torch.Tensor:
        """

        Parameters
        ----------
        iter_dict : Dict[str, Any]
            ``iter_dict`` from any dataset. Expects ``instance`` to be present in the
            ``iter_dict`` where instance is a list of sentences and the tokens are separated by
            space

        Returns
        -------
        torch.Tensor
            Returns the representation for every token in the instance
            ``[batch_size, max_len, emb_dim]``. In case of Elmo the ``emb_dim`` is 1024


        """
        # [np.array] - A generator of embeddings
        # each array in the list is of the shape (3, #words_in_sentence, 1024)
        x = iter_dict["instance"]
        x = x if isinstance(x, list) else [x]
        x = [instance.split() for instance in x]

        embedded = list(self.elmo.embed_sentences(x))

        # bs, 3, #words_in_sentence, 1024
        embedded = torch.FloatTensor(embedded)

        embedding_ = None
        # aggregate of word embeddings
        if self.layer_aggregation_type == "sum":
            # bs, #words_in_sentence, 1024
            embedding_ = torch.sum(embedded, dim=1)

        elif self.layer_aggregation_type == "average":
            # mean across all layers
            embedding_ = torch.mean(embedded, dim=1)

        elif self.layer_aggregation_type == "last":
            # bs, max_len, 1024
            embedding_ = embedded[:, -1, :, :]

        elif self.layer_aggregation_type == "first":
            # bs, max_len, 1024
            embedding_ = embedded[:, 0, :, :]

        embedding_ = embedding_.to(self.device)

        return embedding_

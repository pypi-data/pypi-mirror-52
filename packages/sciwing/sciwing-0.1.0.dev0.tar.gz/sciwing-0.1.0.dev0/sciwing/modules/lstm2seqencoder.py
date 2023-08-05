import torch
import torch.nn as nn
import wasabi
from typing import Dict, Any
from sciwing.utils.class_nursery import ClassNursery


class Lstm2SeqEncoder(nn.Module, ClassNursery):
    def __init__(
        self,
        emb_dim: int,
        embedder: nn.Module,
        dropout_value: float = 0.0,
        hidden_dim: int = 1024,
        bidirectional: bool = False,
        num_layers: int = 1,
        combine_strategy: str = "concat",
        rnn_bias: bool = False,
        device: torch.device = torch.device("cpu"),
    ):
        """Encodes a set of tokens to a set of hidden states.

        Parameters
        ----------
        emb_dim : int
            Embedding dimension of the tokens
        embedder : nn.Module
            Any embedder can be used for this purpose
        dropout_value : float
            The dropout value for the embedding
        hidden_dim : int
            The hidden dimensions for the LSTM
        bidirectional : bool
            Whether the LSTM is bidirectional
        num_layers : int
            The number of layers of the LSTM
        combine_strategy : str
            The strategy to combine the different layers of the LSTM
            This can be one of
                sum
                    Sum the different layers of the embedding
                concat
                    Concat the layers of the embedding
        rnn_bias : bool
            Set this to false only for debugging purposes
        device : torch.device
        """
        super(Lstm2SeqEncoder, self).__init__()
        self.emb_dim = emb_dim
        self.embedder = embedder
        self.dropout_value = dropout_value
        self.hidden_dim = hidden_dim
        self.bidirectional = bidirectional
        self.combine_strategy = combine_strategy
        self.rnn_bias = rnn_bias
        self.device = device
        self.num_directions = 2 if self.bidirectional else 1
        self.num_layers = num_layers
        self.allowed_combine_strategies = ["sum", "concat"]
        self.msg_printer = wasabi.Printer()

        assert (
            self.combine_strategy in self.allowed_combine_strategies
        ), self.msg_printer.fail(
            f"The combine strategies can be one of "
            f"{self.allowed_combine_strategies}. You passed "
            f"{self.combine_strategy}"
        )
        self.emb_dropout = nn.Dropout(p=self.dropout_value)
        self.output_dropout = nn.Dropout(p=self.dropout_value)
        self.rnn = nn.LSTM(
            input_size=self.emb_dim,
            hidden_size=self.hidden_dim,
            bias=self.rnn_bias,
            batch_first=True,
            bidirectional=self.bidirectional,
            num_layers=self.num_layers,
            dropout=self.dropout_value,
        )

    def forward(
        self,
        iter_dict: Dict[str, Any],
        c0: torch.FloatTensor = None,
        h0: torch.FloatTensor = None,
    ) -> torch.Tensor:
        """

            Parameters
            ----------
            iter_dict : Dict[str, Any]
                Any ``iter_dict`` that is passed from the dataset
            c0 : torch.FloatTensor
                The initial state vector for the LSTM
            h0 : torch.FloatTensor
                The initial hidden state for the LSTM

            Returns
            -------
            torch.Tensor
                Returns the vector encoding of the set of instances
                [batch_size, hidden_dim] if single direction
                [batch_size, 2*hidden_dim] if bidirectional
        """

        # TODO: the batch size should be present in the iter_dict
        batch_size, seq_length = iter_dict["tokens"].size()

        embeddings = self.embedder(iter_dict=iter_dict)

        embeddings = self.emb_dropout(embeddings)

        if h0 is None or c0 is None:
            h0, c0 = self.get_initial_hidden(batch_size=batch_size)

        # output = batch_size, sequence_length, hidden_dim * num_directions
        # h_n = num_layers * num_directions, batch_size, hidden_dimension
        # c_n = num_layers * num_directions, batch_size, hidden_dimension
        output, (_, _) = self.rnn(embeddings, (h0, c0))

        if self.bidirectional:
            output = output.view(batch_size, seq_length, self.num_directions, -1)
            forward_output = output[:, :, 0, :]  # batch_size, seq_length, hidden_dim
            backward_output = output[:, :, 1, :]  # batch_size, seq_length, hidden_dim
            if self.combine_strategy == "concat":
                encoding = torch.cat([forward_output, backward_output], dim=2)
            elif self.combine_strategy == "sum":
                encoding = torch.add(forward_output, backward_output)
        else:
            encoding = output

        return encoding

    def get_initial_hidden(self, batch_size: int):
        h0 = torch.zeros(
            self.num_layers * self.num_directions, batch_size, self.hidden_dim
        )
        c0 = torch.zeros(
            self.num_layers * self.num_directions, batch_size, self.hidden_dim
        )
        h0 = h0.to(self.device)
        c0 = c0.to(self.device)
        return h0, c0

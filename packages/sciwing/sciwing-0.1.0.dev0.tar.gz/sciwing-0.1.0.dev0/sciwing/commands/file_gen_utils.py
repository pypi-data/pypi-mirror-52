import pathlib
from typing import Optional, Dict, Any, List
import sciwing.constants as constants
from questionary.prompts.common import Choice
import jinja2
import questionary
import wasabi
import autopep8
from sciwing.commands.validators import is_file_exist

PATHS = constants.PATHS
TEMPLATES_DIR = PATHS["TEMPLATES_DIR"]
DATASETS_DIR = PATHS["DATASETS_DIR"]


class ClassificationDatasetGenerator(object):
    """ This method interactive generates a classification dataset file with all the different batteries
    required to implement a dataset. We generate the dataset for the developer, developing the dataset
    This provides more flexibility to the developer to change different parts if necessary.

    However, we also provide out-of-the-box functionality if the files are in standard format.
    If the classification dataset is of the format ``text\\tlabel`` with one text instance per
    line then we provide out-of-the-box functionality for the developer of the dataset. There
    is no need to touch the file.
    """

    def __init__(self, dataset_name: str):
        """

        Parameters
        ----------
        dataset_name : str
            The class name of the dataset that will be generated

        """
        self.dataset_name = dataset_name
        self.template_file = pathlib.Path(
            TEMPLATES_DIR, "classification_dataset_template.txt"
        )
        self.msg_printer = wasabi.Printer()
        self.template = self._get_template()
        self.template_variables = self.interact()

    def _get_template(self):
        with open(self.template_file, "r") as fp:
            template_string = "".join(fp.readlines())
        jinja_template = jinja2.Template(template_string)
        return jinja_template

    def generate(self):
        """ Write the generate classification dataset into the ``dataset.classification`` folder

        Returns
        -------
        None
        """
        with open(
            pathlib.Path(DATASETS_DIR, "classification", f"{self.dataset_name}.py"), "w"
        ) as fp:
            rendered_class = self.template.render(self.template_variables)
            rendered_class = autopep8.fix_code(rendered_class)
            fp.write(rendered_class)

    def interact(self) -> Dict[str, Any]:

        debug = self._get_debug_default_value()

        debug_dataset_proportion = self._get_debug_dataset_proportion()

        vocab_pipe = self._get_vocab_pipes()

        word_embedding_type = self._get_word_embedding_type()

        embeddingtype2embedding_dimension = {
            "glove_6B_100": 100,
            "glove_6B_200": 200,
            "glove_6B_300": 300,
            "parscit": 500,
        }

        if word_embedding_type == "random":
            random_emb_dim = questionary.text(
                message="Enter embedding dimension: ", default="100"
            ).ask()
            random_emb_dim = int(random_emb_dim)
            embeddingtype2embedding_dimension["random"] = random_emb_dim

        emb_dim = embeddingtype2embedding_dimension[word_embedding_type]

        word_start_token = self._get_word_start_token()

        word_end_token = self._get_word_end_token()

        word_pad_token = self._get_word_pad_token()

        word_unk_token = self._get_word_unk_token()

        char_start_token = None
        char_end_token = None
        char_pad_token = None
        char_unk_token = None
        char_embedding_type = None
        char_embedding_dimension = None
        char_tokenizer = None
        max_num_chars = None
        if "char_vocab" in vocab_pipe:
            char_start_token = self._get_char_start_token()
            char_end_token = self._get_char_end_token()
            char_pad_token = self._get_char_pad_token()
            char_unk_token = self._get_char_unk_token()
            char_embedding_type = "random"
            char_embedding_dimension = self._get_char_embedding_dimension()
            char_tokenizer = f"CharacterTokenizer()"

        train_size = self._get_default_train_size()

        test_size = self._get_default_test_size()

        validation_size = self._get_default_validation_size()

        tokenizer_type = self._get_tokenizer_type()

        word_tokenizer = f'WordTokenizer(tokenizer="{tokenizer_type}")'

        is_dataset_standard_fmt = self._get_is_dataset_standard_fmt()

        is_valid_default_file = False
        categories = None

        # generate the appropriate code
        if is_dataset_standard_fmt:
            # ask the user for the filename where the dataset is stored
            filename = questionary.text(
                message="Enter the full path of the file where the file is stored",
                validate=is_file_exist,
            ).ask()
            is_valid_file, lines, labels = self.parse_file(filename=filename)
            if not is_valid_file:
                self.msg_printer.fail(
                    f"The file {filename} should be of the format text\tlabel."
                )
                is_valid_default_file = False
            else:
                is_valid_default_file = True

                # what are the different labels in the dataset?
                unique_labels = set(labels)
                unique_labels = list(unique_labels)
                categories = unique_labels

        template_options_dict = {
            "className": self.dataset_name,
            "word_embedding_type": word_embedding_type,
            "word_embedding_dimension": emb_dim,
            "word_start_token": word_start_token,
            "word_end_token": word_end_token,
            "word_pad_token": word_pad_token,
            "word_unk_token": word_unk_token,
            "train_size": train_size,
            "validation_size": validation_size,
            "test_size": test_size,
            "word_tokenization_type": tokenizer_type,
            "word_tokenizer": word_tokenizer,
            "debug": debug,
            "debug_dataset_proportion": debug_dataset_proportion,
            "valid_default_file": is_valid_default_file,
            "categories": categories,
            "vocab_pipe": vocab_pipe,
            "is_char_vocab": "char_vocab" in vocab_pipe,
            "char_start_token": char_start_token,
            "char_end_token": char_end_token,
            "char_pad_token": char_pad_token,
            "char_unk_token": char_unk_token,
            "char_embedding_type": char_embedding_type,
            "char_embedding_dimension": char_embedding_dimension,
            "char_tokenizer": char_tokenizer,
        }
        return template_options_dict

    @staticmethod
    def parse_file(filename: str) -> (bool, List[str], List[str]):
        """ Takes a filename that is in standard classification format and return lines and labels if
        the filename conforms to the standard format

        Parameters
        ----------
        filename : str
            Full path of the filename where the classification dataset is stored

        Returns
        -------
        bool, List[str], List[str]
            - Indicates whether classification dataset conforms to the standard format.
            - Lines from the file
            - Labels from the file

        """
        lines = []
        labels = []
        with open(filename, "r") as fp:
            for line in fp:
                line = line.strip()
                try:
                    columns = line.split("\t")
                    text, label = columns[0], columns[-1]
                    lines.append(text)
                    labels.append(label)
                except ValueError:
                    return False, [], []
        return True, lines, labels

    @staticmethod
    def _get_debug_default_value():
        debug_default_value = questionary.confirm(
            "Do you want default value for debug to be True?: ", default=False
        ).ask()
        return debug_default_value

    @staticmethod
    def _get_debug_dataset_proportion():
        debug_dataset_proportion = questionary.text(
            message="Enter Proportion of dataset for debug: ", default="0.1"
        ).ask()
        debug_dataset_proportion = float(debug_dataset_proportion)
        return debug_dataset_proportion

    @staticmethod
    def _get_word_embedding_type():
        embedding_type = questionary.select(
            message="Chose one of the embeddings available: ",
            choices=[
                Choice(title="random", value="random"),
                Choice(title="parscit", value="parscit"),
                Choice(title="glove_6B_100", value="glove_6B_100"),
                Choice(title="glove_6B_200", value="glove_6B_200"),
                Choice(title="glove_6B_300", value="glove_6B_300"),
            ],
        ).ask()
        return embedding_type

    @staticmethod
    def _get_word_start_token():
        word_start_token = questionary.text(
            message="Enter default token to be used for beginning of sentence: ",
            default="<SOS>",
        ).ask()
        return word_start_token

    @staticmethod
    def _get_word_end_token():
        word_end_token = questionary.text(
            message="Enter default token to be used for end of sentence: ",
            default="<EOS>",
        ).ask()
        return word_end_token

    @staticmethod
    def _get_word_pad_token():
        word_pad_token = questionary.text(
            message="Enter default token to be used for padding sentences: ",
            default="<PAD>",
        ).ask()
        return word_pad_token

    @staticmethod
    def _get_word_unk_token():
        word_unk_token = questionary.text(
            message="Enter default token to be used in case the word is not found in the vocab: ",
            default="<UNK>",
        ).ask()
        return word_unk_token

    @staticmethod
    def _get_default_train_size():
        train_size = questionary.text(
            message="Enter default size of the dataset that will be used for training: ",
            default="0.8",
        ).ask()
        train_size = float(train_size)
        return train_size

    @staticmethod
    def _get_default_test_size():
        test_size = questionary.text(
            message="Enter default size of the dataset that will be used for testing: ",
            default="0.2",
        ).ask()
        test_size = float(test_size)
        return test_size

    @staticmethod
    def _get_default_validation_size():
        validation_size = questionary.text(
            message="Enter default size fo the dataset that will be used for validation.: "
            "This will be the proportion of the test size that will be used",
            default="0.5",
        ).ask()
        return validation_size

    @staticmethod
    def _get_tokenizer_type():
        tokenizer_type = questionary.select(
            message="What is the default tokenization that you would want to use?: ",
            choices=[
                Choice(
                    title="Vanilla (sentences are separated by space to form words)",
                    value="vanilla",
                ),
                Choice(title="Spacy tokenizer", value="spacy"),
            ],
            default="vanilla",
        ).ask()
        return tokenizer_type

    @staticmethod
    def _get_is_dataset_standard_fmt():
        is_dataset_standard_fmt = questionary.confirm(
            message="Is dataset in standard format?", default=False
        ).ask()
        return is_dataset_standard_fmt

    @staticmethod
    def _get_vocab_pipes():
        vocab_pipe = questionary.checkbox(
            message="What batteries do you want with the dataset?",
            choices=[
                Choice(
                    title="word_vocab [Default] will always be included",
                    checked=True,
                    disabled=True,
                    value="word_vocab",
                ),
                Choice(
                    title="char_vocab - Usually included if character embeddings are needed",
                    value="char_vocab",
                ),
            ],
        ).ask()
        vocab_pipe.append("word_vocab")
        return vocab_pipe

    @staticmethod
    def _get_char_start_token():
        char_start_token = questionary.text(
            message="Enter the start token to be used for characters", default=" "
        ).ask()
        return char_start_token

    @staticmethod
    def _get_char_end_token():
        char_end_token = questionary.text(
            message="Enter the end token to be used for characters", default=" "
        ).ask()
        return char_end_token

    @staticmethod
    def _get_char_pad_token():
        char_pad_token = questionary.text(
            message="Enter the pad token to be used for characters", default=" "
        ).ask()
        return char_pad_token

    @staticmethod
    def _get_char_unk_token():
        char_unk_token = questionary.text(
            message="Enter the unk token to be used for characters", default=" "
        ).ask()
        return char_unk_token

    @staticmethod
    def _get_char_embedding_dimension():
        char_embedding_dimension = questionary.text(
            message="Enter char embedding dimension", default="25"
        ).ask()
        char_embedding_dimension = int(char_embedding_dimension)
        return char_embedding_dimension

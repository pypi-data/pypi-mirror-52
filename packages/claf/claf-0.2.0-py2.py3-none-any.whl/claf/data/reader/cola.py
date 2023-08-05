
import logging

from overrides import overrides

from claf.data.reader import SeqClsReader
from claf.decorator import register

logger = logging.getLogger(__name__)


@register("reader:cola")
class CoLAReader(SeqClsReader):
    """
    CoLA DataReader

    * Args:
        file_paths: .json file paths (train and dev)
        tokenizers: define tokenizers config (word)
    """

    CLASS_DATA = [0, 1]

    def __init__(
            self,
            file_paths,
            tokenizers,
            sequence_max_length=None,
    ):

        super(CoLAReader, self).__init__(
            file_paths,
            tokenizers,
            sequence_max_length=sequence_max_length,
        )

    @overrides
    def _get_data(self, file_path, **kwargs):
        data_type = kwargs["data_type"]

        _file = self.data_handler.read(file_path)
        lines = _file.split("\n")

        if data_type == "train":
            lines.pop(0)

        data = []
        for i, line in enumerate(lines):
            line_tokens = line.split("\t")
            if len(line_tokens) > 1:
                data.append({
                    "uid": f"{data_type}-{i}",
                    "sequence": line_tokens[1] if data_type == "test" else line_tokens[3],
                    self.class_key: str(0) if data_type == "test" else str(line_tokens[1])
                })

        return data

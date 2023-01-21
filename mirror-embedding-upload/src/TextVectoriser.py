from transformers import AutoTokenizer, AutoModel
from torch import FloatTensor, cuda


class TextVectoriser(object):

    def __init__(self, model_dir: str, *args, **kwargs):
        """
        Text Embedding model wrapper.

        For now, the TextVectoriser only supports HuggingFace-based models.
        
        This class can be easily extended to support other models by pointing self.tokenizer and self.model 
        to other model implementations, and overriding its methods.
        E.g. CustomRetriever requires a TextVectoriser that implements `inference_from_dicts(dicts)`.

        :param model_dir: path to directory containing the HuggingFace models.
        See https://huggingface.co/princeton-nlp/sup-simcse-roberta-large/tree/main
        for an example.

        """
        self.device = "cuda:0" if cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModel.from_pretrained(model_dir).to(self.device)
        return super().__init__(*args, **kwargs)


    def compute_vector(self, str_list):
        """
        :param str_list: a batch of strings.
        :returns: torch.FloatTensor of shape (batch_size, hidden_size).
        """

        inputs = self.tokenizer(str_list, return_tensors="pt", padding=True, truncation=True).to(self.device)
        outputs = self.model(**inputs)

        return outputs.pooler_output  # can try other pooling schemes too.

        
    def inference_from_dicts(self, dicts: list) -> list:
        """
        Encodes texts into vectors.
        
        :param dicts: A list of dicts. Each dict should have "text" field. e.g. {"text": t}, where t is a string.
        :returns: A list of dicts. Each dict should have a "vec" field. e.g. {"vec": v}, where v is a FloatTensor of len == embedding dims.
        """
        str_list = [d["text"] for d in dicts]
        
        inputs = self.tokenizer(str_list, return_tensors="pt", padding=True, truncation=True).to(self.device)
        outputs = self.model(**inputs)

        return [{"vec": emb} for emb in outputs.pooler_output]  # can try other pooling schemes too.



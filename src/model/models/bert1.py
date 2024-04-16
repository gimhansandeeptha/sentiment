# concreate Implementation of bert model
import torch
from transformers import BertModel

class BertClass(torch.nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        self.model = BertModel.from_pretrained("bert-base")
        pass
    
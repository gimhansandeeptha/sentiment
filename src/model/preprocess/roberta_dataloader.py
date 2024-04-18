import torch
from abc import ABC, abstractmethod

class RobertaSentimentData(ABC):
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self,index):
        pass

    def convert_text(self, text,index, tokenizer, max_len)->dict:
        text = str(self.text[index])
        text = " ".join(text.split())

        inputs = tokenizer.encode_plus(
            text,
            None,
            add_special_tokens=True,
            max_length=max_len,
            pad_to_max_length=True,
            return_token_type_ids=True,
            truncation=True
        )
        ids = inputs['input_ids']
        mask = inputs['attention_mask']
        token_type_ids = inputs["token_type_ids"]

        return {
            'ids': torch.tensor(ids, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
            'token_type_ids': torch.tensor(token_type_ids, dtype=torch.long),
        }

class RobertaTrainSentimentData(RobertaSentimentData):
    '''
    Custom class for handling sentiment data. To be able to pass to the DataLoader.
    __getitem__ function do the tokenization for each text sample.
    '''
    def __init__(self, x, y, tokenizer, max_len):
        self.tokenizer = tokenizer
        self.text = x
        self.targets = y
        self.max_len = max_len

    def __len__(self):
        return len(self.text)

    def __getitem__(self, index):
        text = str(self.text[index])
        text = " ".join(text.split())

        data = super().convert_text(text, index, self.tokenizer, self.max_len)
        data['targets'] = torch.tensor(self.targets[index], dtype=torch.float)
        return data


class RobertaInferenceSentimentData(RobertaSentimentData):
    def __init__(self, x, tokenizer, max_len):
        self.tokenizer = tokenizer
        self.text = x
        self.max_len = max_len

    def __len__(self):
        return len(self.text)
    
    def __getitem__(self, index):
        text = str(self.text[index])
        text = " ".join(text.split())

        data = super().convert_text(text, index, self.tokenizer, self.max_len)
        return data
    
import torch
from transformers import RobertaModel

class RobertaClass(torch.nn.Module):
    '''
    Custom PyTorch module for sentiment analysis using a fine-tuned RoBERTa model.
    - l1: Pre-trained RoBERTa model loaded from "roberta-base" using Hugging Face Transformers.
    - pre_classifier: Linear layer for additional transformation before classification.
    - dropout: Dropout layer for regularization.
    - classifier: Linear layer for final sentiment classification.
    '''
    def __init__(self, hidden_size = 768, dropout_prob=0.3, num_classes=3):
        super(RobertaClass, self).__init__()
        self.l1 = RobertaModel.from_pretrained("roberta-base")
        self.pre_classifier = torch.nn.Linear(hidden_size, 100)
        self.dropout = torch.nn.Dropout(dropout_prob)
        self.classifier = torch.nn.Linear(100, num_classes)

    def forward(self, input_ids, attention_mask, token_type_ids):
        output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        hidden_state = output_1[0]
        pooler = hidden_state[:, 0]
        pooler = self.pre_classifier(pooler)
        pooler = torch.nn.ReLU()(pooler)
        pooler = self.dropout(pooler)
        output = self.classifier(pooler)
        return output
    
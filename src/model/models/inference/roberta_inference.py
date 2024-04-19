from tqdm import tqdm
import torch
import numpy as np

class RobertaInference():
    def __init__(self,model: torch.nn.Module,tokenizer,max_len, device) -> None:
        self.model = model
        self.tokenizer = tokenizer
        self.max_len = max_len
        self.device = device

        self.model.to(self.device)

    def infer(self, inference_loader)-> np.array:
        self.model.eval()
        result =[]
        for _, data in tqdm(enumerate(inference_loader, 0)):
            predicted_class = None
            ids = data['ids'].to(self.device, dtype=torch.long)
            mask = data['mask'].to(self.device, dtype=torch.long)
            token_type_ids = data['token_type_ids'].to(self.device, dtype=torch.long)

            with torch.no_grad():
                output = self.model(ids, mask, token_type_ids)
            _, predicted_class = torch.max(output, dim=1)

            result.append(predicted_class)
        result = np.array(result)
        return result
    
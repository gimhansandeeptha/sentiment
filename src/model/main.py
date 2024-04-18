import os
import json
from datetime import datetime
from src.model.models.model import Model
from src.model.models.roberta_model import RobertaModel
from src.utils.metadata import Metadata
from src.data.data_model import ServicenowData
from src.model.preprocess.roberta_dataloader import RobertaTrainSentimentData

class ModelProcess:
    def __init__(self) -> None:
        self.model_creator: Model = None
        self.finetune_metadata_filepath = "models\\finetune_checkpoint\\metadata\\roberta_metadata.json"
        self.stable_metadata_filepath = "models\\stable_checkpoint\\metadata\\initial_metadata.json"
        self.max_finetuned_count = 5
    
    def save(self, folder):
        pass

    def train(self):
        pass

    def inference_process(self, data: ServicenowData):
        metadata = Metadata(self.stable_metadata_filepath)
        model_path = metadata.get_value(["path"])
        texts = data.get_column("text")
        model_creator = RobertaModel()
        model_creator.create()
        model_creator.load(model_path)
        sentiments = model_creator.infer(texts)

        data.insert_field("roberta_sentiment")
        for i in range(len(sentiments)):
            data.insert_data(i, "roberta_sentiment",sentiments[i])

    def _preprocess(self, data:ServicenowData):
        df = data.get_data()
        texts = df['text'].to_numpy()
        sentiments = df['sentiment'].to_numpy()
        return texts, sentiments

    def finetune_process(self, data:ServicenowData):
        text = data.get_column("text")
        sentiment = data.get_column("sentiment")

        metadata = Metadata(self.finetune_metadata_filepath)
        checkpoint_path = metadata.get_value(['latest','path'])
        finetuned_count = metadata.get_value(['latest','finetune_count'])

        model_creator = RobertaModel()
        model_creator.create()
        model_creator.load(checkpoint_path)

        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        directory, old_filename = os.path.split(checkpoint_path)
        new_checkpoint_path = os.path.join(directory, f"{current_datetime}.pth")

        if finetuned_count < self.max_finetuned_count:
            model_creator.finetune(text, sentiment)
            model_creator.save(new_checkpoint_path)
            os.remove(checkpoint_path)
            metadata.set_value(['latest','finetune_count'], finetuned_count+1)
            
        else:
            checkpoint_validation_loss = model_creator.validate(text, sentiment)

            stable_metadata = Metadata(self.stable_metadata_filepath)
            stable_model_path = stable_metadata.get_value(['path'])
            stable_directory, stable_old_filename = os.path.split(stable_model_path)
            new_model_path = os.path.join(stable_directory, f"{current_datetime}.pth")
            stable_validation_loss = stable_metadata.get_value(['validation_loss'])

            if checkpoint_validation_loss < stable_validation_loss:
                model_creator.save(new_model_path)
                os.remove(stable_model_path)
                stable_metadata.set_value(['validation_loss'], checkpoint_validation_loss)

            metadata.set_value(['latest','finetune_count'], 0)
          
from src.data.data_model import ServicenowData
from src.model.main import ModelProcess
from src.test import get_df

df = get_df()
data = ServicenowData()
data.load_test_data(df)

main = ModelProcess()
main.finetune_process(data)
# print(data.get_data())

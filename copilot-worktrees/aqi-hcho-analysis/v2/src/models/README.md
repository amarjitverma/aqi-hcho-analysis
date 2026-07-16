\# Models Module



This module contains all deep learning model architectures.



\## Available Models



| Model | Folder | Description |

|-------|--------|-------------|

| LSTM | `lstm/` | Standard LSTM for time-series prediction |

| CNN-LSTM | `cnn\_lstm/` | Hybrid CNN-LSTM for spatiotemporal data |

| ConvLSTM | `convlstm/` | ConvLSTM for spatiotemporal prediction |

| Transformer | `transformer/` | Transformer for time-series prediction |

| Ensemble | `ensemble/` | Ensemble of all models |



\## Usage



```python

from src.models.lstm.lstm import LSTMModel



model = LSTMModel()

model.build(input\_shape)

model.compile()

model.train(X\_train, y\_train, X\_val, y\_val)

predictions = model.predict(X\_test)


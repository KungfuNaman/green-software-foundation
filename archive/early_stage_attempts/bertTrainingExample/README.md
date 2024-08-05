
# Bert Training Demo

This is a Google Colab script that trains the LLM Bert (specifically BertForSequenceClassification) on the classification task of predicting whether a description adheres to 1 or more green practices.

In this case there are 2 possible green practices 'decoupled_messaging' and 'serverless_solution' that a text description can adhere to.

Each text in the text list (top to bottom) is represented from left to right within the  'decoupled_messaging' and 'serverless_solution' lists, with a label of 1 if the text adheres to the practice and a label of 0 if it doesn't.

This dataset is initially created and converted to csv.

Then the dataset is read from the csv format and split into training and validation datasets.

The training/validation split is 0.8 - 0.2, so 4 data points in the training and 1 in the validation.

The training and validation text descriptions are encoded using a tokeniser (bert-base-uncased). The training and validation labels (0s and 1s) are converted into tensors.

A loss function is defined within a custom Trainer class. In this case it is Binary Cross Entropy loss (deemed suitable for multilabel classification where each label is a separate binary decision) The aim of training is to minimize this loss function.

A custom dataset class (overrides torch.utils.data.Dataset) is used to combine the train encodings and labels, and validation encodings and labels. This dataset can be fed in to create a Trainer instance.

The training arguments are also defined, which define the hyperparameters such as number of epochs to train for and where to store the trained model.

The model is then trained with the training arguments and datasets. The final model is saved in the results directory.

The following box contains code to infer on the trained model (loaded from the results directory) by tokenising and passing in new input.

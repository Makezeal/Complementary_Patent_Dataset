**Status:** Archive (code is provided as-is, no updates expected)

# Complementary_Patents_Dataset

Code and data from the paper “Construction of Complementary Patent Dataset Based on Transaction Relationships”

This article proposes a method for obtaining a complementary patent dataset by extracting transaction relationships between patents. There are multiple transfer categories in patent transfer records, and this article delves into direct transactions and joint research records to limit transaction frequency, transaction size, and patent text similarity, thereby constructing a complementary patent dataset. In addition, this article validates the effectiveness of the dataset through link prediction tasks in heterogeneous networks.

## Requirements

To run this code you need the following:

| Libraries     | version |
| ------------- | ------- |
| numpy         | 1.26.4  |
| pandas        | 2.2.3   |
| requests      | 2.32.3  |
| scikit-learn  | 1.5.2   |
| gensim        | 4.3.3   |
| tensorflow    | 2.18.0  |
| torch         | 2.4.1+cu118   |

The environment configuration of the code is not the same. Please modify it according to the specific situation. The following is for reference only.

## Usage

The comments in the code have been changed from Chinese to English. Part of the data is published by USPTO, and the data in Data/Heterogeneous_graph_data is the final complementary patent dataset and patent heterogeneous graph data

### Process

- Perform data preprocessing on patent transfer data and patent authorization data separately using the files in 'Data_preprocessing'.
- Merge patent transfer data and patent authorization data together using the files in 'Dataset_comstruction', extract corresponding transaction relationships, and ultimately construct a complementary patent dataset. The file code also includes some visual analysis of the dataset.

## Evaluation Metric

In our study, we used **Link Prediction Task** to evaluate the dataset. Specifically, we extracted patent heterogeneity maps from the constructed complementary patent dataset and inputted them into RGCN, HAN, HGT models. The results were evaluated using evaluation metrics such as AUC, Precision, Recall, and F1.

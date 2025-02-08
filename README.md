**Status:** Archive (code is provided as-is, no updates expected)

# Complementary_Patents_Dataset

Code and data from the paper “Construction of Complementary Patent Dataset Based on Patent Market Transactions”

This article proposes a method for obtaining a complementary patent dataset by extracting transaction relationships between patents. There are multiple transfer categories in patent assignment records, and this article delves into direct transactions and joint research records to limit transaction frequency, transaction scale, and patent text similarity, thereby constructing a complementary patent dataset.

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

The environment configuration of the code may vary, please modify it according to the specific situation. The above content is for reference only.

## Usage

The comments in the code have been changed from Chinese to English. Part of the data is published by USPTO, and the data in Data/Heterogeneous_graph_data is the final complementary patent dataset.

### Process

- Perform data preprocessing on patent transfer data and patent authorization data separately using the files in 'Data_preprocessing'.
- Merge patent transfer data and patent grant data together using the files in 'Dataset_comstruction', extract corresponding transaction relationships, and ultimately construct a complementary patent dataset. The file code also includes some visual analysis of the dataset.

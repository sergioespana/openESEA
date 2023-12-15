# Automated Method Comparison Algorithm

## Project description

<DESCRIPTION> This project is being carried out within the Software for Organisational Responsibility Lab at Utrecht University. The project is part of ongoing research and development endeavours surrounding the openESEA framework. More information about the OpenESEA framework can be found on https://github.com/sergioespana/openESEA. For this project an automated method comparison algorithm is developed. The automated  method comparison algorithm performs matching and merging of data from two models (Method_Model_A and Method_Model_B) based on similarity scores calculated using BERT embeddings and cosine similarity. The goal is to identify similar models and merge them, writing the results to output files.

## Directory structure
```
`-- openESEA model management/
      |-- Preprocessing/
      |     |-- input/
      |     |     |-- DSL_Model_A.txt
      |     |     `-- DSL_Model_B.txt
      |-- Match_and_Merge/
      |     |-- input/
      |     |     |-- Method_Model_A.txt
      |     |     `-- Method_Model_B.txt
            `-- output/
      |           |-- Similarity_scores.txt
      |           |-- Matched.txt
      |           `-- Unmatched.txt 
      |-- Postprocessing/
      |     |-- input/
      |     |     |-- Merged_models.txt
            `-- output/
      |           |-- Final_Merged_Model.txt
      |-- src/
      |     |-- preprocessing.ipynb
      |     |-- match_and_merge.ipynb
      |     |-- postprocessing.ipynb
      `-- requirements.txt
```

- `Preprocessing/` Combining Topic, Indicator, and Question Fragments

- `Match_and_Merge/` Matching and Merging ESEA Method Models

- `Postprocessing/` Data Cleaning and Transformation

- `src/` Contains all function and module code in notebooks corresponding to the 3 main steps of the project: (1) preprocessing, (2) matching and merging, (3) postprocessing

- `requirements.txt` Contains all packages and libraries that are needed to run the script. 

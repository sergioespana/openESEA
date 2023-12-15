# Matching and Merging ESEA Method Models
## Importing Libraries
The script starts by importing necessary libraries such as transformers (for BERT models), torch, sklearn.metrics.pairwise, and itertools.

```bash
pip install transformers torch scikit-learn pint
```

## Input Match and Merge
- The input data is sourced from two files: `Method_Model_A.txt` and `Method_Model_B.txt`. These .txt files were generated in the preprocessing phase and now function as inputs for the match and merge algorithm.

```python
# Example paths
data1_path = "/path/to/Method_Model_A.txt"
data2_path = "/path/to/Method_Model_B.txt"

# Example output file paths
all_scores_file_path = "/path/to/Similarity_scores.txt"
merged_file_path = "/path/to/Merged_models.txt"
matched_file_path = "/path/to/matched.txt"
unmatched_file_path = "/path/to/unmatched.txt"
```

## Main Script
The Python script performs matching and merging of method models based on the similarity of attributes such as "topic_Description," "indicator_Name," and "indicator_Description." The script uses BERT embeddings and cosine similarity to calculate similarity scores.

### Functions
1. **get_answer_options(model1, model2)**
   - Retrieves answer options from two models.

2. **calculate_answer_similarity(options1, options2)**
   - Calculates the similarity of answer options using BERT embeddings and cosine similarity.

3. **generate_back_conversion_description(original_unit, converted_unit)**
   - Attempts to find a back conversion formula between two units

4. **process_transformation_formula(model1, model2, output_file)**
   - Processes and writes transformation formulas to the output file.

5. **calculate_similarity_attributes(model1, model2)**
   - Calculates similarity scores for attributes (e.g., topic_Description, indicator_Name) between two models.

6. **calculate_similarity_question(model1, model2)**
   - Calculates similarity scores for indicator_Description between two models

7. **parse_fragment_models(file_path, name_prefix)**
   - Parses "fragment_model" sections from a data file and assigns names.

8. **is_data_type_valid(model1, model2)**
   - Checks if the combination of data types between two models is valid.

9. **choose_model(model1, model2)**
   - Chooses the appropriate model based on data type rules.

10. **get_formatted_write_string(model)**
    - Formats a model dictionary as a string for writing to files

11. **match_and_merge_output(data1_path, data2_path, threshold_indicator, threshold_question, all_scores_file_path, merged_file_path, matched_file_path, unmatched_file_path)**
    - Main function to perform matching and write output to files.	


## Main Execution
- Call the main function to perform matching and write output to files
- The script specifies paths for input data files (`data1_path` and `data2_path`) and output files (`all_scores_file_path`, `merged_file_path`, `matched_file_path`, `unmatched_file_path`).
- Thresholds (`threshold_indicator` and `threshold_question`) are set to determine matches based on similarity scores.
- The `match_and_merge_output` function is called to perform the matching and merging process.

## Output Match and Merge
- The output includes similarity scores written to a `Similarity_scores.txt` file, merged models written to `Merged_models.txt`, matched models to `matched.txt`, and unmatched models to `unmatched.txt`. 

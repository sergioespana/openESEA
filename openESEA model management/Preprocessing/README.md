# Preprocessing: Combining Topic, Indicator, and Question Fragments

## Input Preprocessing
- Copy and paste all topic, indicator, and question fragments from an ESEA method model to a new text file.
- Two example input files are stored in the preprocessing folder: `DSL_Model_A.txt` and `DSL_Model_B.txt`.

## Excel Transformation Sheet Related Functions
The following functions need to be executed only if you have created text file models based on the excel transformation sheet. They remove unnecessary quotation marks.

1. **remove_quotation_marks(input_path)**
   - Usage:
     ```python
     data1_path = "/Users/Documents/Main/Preprocessing/DSL_Model_A.txt"
     remove_quotation_marks(data1_path)
     ```

2. **remove_duplicate_quotation_marks(input_path)**
   - Usage:
     ```python
     data1_path = "/Users/Documents/Main/Preprocessing/DSL_Model_A.txt"
     remove_duplicate_quotation_marks(data1_path)
     ```

3. **remove_pre_and_postunit_quotes(input_file)**
   - Usage:
     ```python
     file_path = "/Users/Documents/Main/Preprocessing/DSL_Model_A.txt"
     remove_pre_and_postunit_quotes(file_path)
     ```

## Main Script
- The Python script utilizes the `re` module for regular expressions to search for and replace specific patterns in an input file (`DSL_Model_A.txt`).
- Modified data is processed to extract relevant information and generate a new output file (`DSL_Model_A_with_Suffix.txt`).

## Functions
1. **suffix_text: 
   - Adding suffix to Text and Order for unique keys**
2. **parse_modified_data(output_file_path)**
   - Parses the modified data from the output file, extracting topics, indicators, and questions into separate lists.
   
3. **combine_data(topics, indicators, questions)**
   - Combines data based on specified conditions, creating a list of dictionaries representing combined subsections.
   
4. **write_combined_data(combined_data, combined_output_file_path)**
   - Writes the combined data to the specified output file (`Method_Model_A.txt`).

## Output Preprocessing
- Adding prefixes "topic", "indicator", and "question" to all attributes to prevent duplicate attribute names.
- Transforming attributes like "Name" of Topic and "Name" of Indicator into "topic_name" and "indicator_name".
- Combining Topic_id searching for indicator_topic and indicator_id searching for question_indicator and combining them when needed.
- Combines even when attributes have the same "topic_id".
- Output is saved in "Method_Model_A.txt," which can be found in the Match and Merge folder
- This output will be used as input for the Match and Merge algorithm
- Repeat this code untill all input files that you want to match and merge are created and stored in the Match and Merge folder

```python
# Example usage:
input_file_path = "/Users/Documents/Main/Preprocessing/DSL_Model_A.txt"
output_file_path = "/Users/Documents/Main/Preprocessing/DSL_Model_A_with_Suffix.txt"
combined_output_file_path = "/Users/noahritfeld/Main/Match_and_Merge/Method_Model_A.txt"



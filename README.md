# Vector-Space-Model

This program uses vector space model to compare similarity among large datasets.

The following measures are used as vector elements:
1. Unique words frequency
2. Term frequency
2. Tf-idf measure (tf-idf_t,d = tf_t,d × idf_t)
4. The sublinear tf scaling: wf_t,d = 1 + log10(tf_t,d) if tf_t,d > 0 ; Otherwise 0
   The sublinear tf scaling is defined as: wf-idf_t,d = wf_t,d × idf_t

**Notes**:
Provide the value for K to display top K closest documents

# Probabilistic-Retrieval-Model

This program implements the binary independence model and displays the top 10 documents with high Retrieval Status Value (RSV).

**Notes**:
1. All related resources such as documents, file_label.txt, query.txt should be in the programs current working directory.

# Statistical Computation:

**Steps**:
1. This program will read contents from Sonnets.txt file and count words for each sonnet. 
2. The sonnet number and word counts will be stored in a dictionary. 
3. Then the mean, median and standard deviations are calculated using the python statistics module.

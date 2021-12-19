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

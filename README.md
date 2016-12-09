# Intra-Lexical Comparison Project

In this project, we aim to determine the linguistic relatedness of a number of languages in the same manner as described in [Kirby and Ellison (2006)](http://dl.acm.org/citation.cfm?id=1220210), using an improved dataset.  This paper describes a process whereby a language is quantified as a matrix comparing the probability of confusing one word for another for every word pair in the language, and these matrices are compared and clustered based on their relatedness.  This new dataset contains more data than that used by the authors in the paper, and uses each word's IPA transcription rather than its orthography to calculate confusion probabilities.

To complete this project, we must replicate all data processing techniques utilized in the paper using this new data, and compare the results we obtain.  After doing so, we must write a paper on our results and prepare a presentation on the topic.

[TOC]

## The Coding

The bulk of the work of this project will likely consist of writing the code necessary to process the data.  This process will consist of 3 independent components passing their results onto one another:

 - **Inter-language processing**:  This will involve the reading of the CSV data file, organizing the data, and performing calculations necessary for computing the matrix for each language that indicates the confusion probabilities for all word pairs.
 - **Intra-language processing**:  This will involve using the matrix output from the previous step to calculate the Kullback-Liebler and Rao distance for each pair of languages, and output the matrix result.
 - **Tree construction**:  This will involve using the matrix output of the previous step to construct a tree showing the relatedness and inferred ancestry of all languages in the collection.

### Inter-language Processing

As the first step in the process, this will first of all involve reading the provided CSV data file ([here](https://ovidius.uni-tuebingen.de/ilias3/goto.php?target=file_1368853_download&client_id=pr02)).  The language, meaning, and phonological forms of all words must be stored, and then sorted into groups based on language.

At this point, all word pairs must be iterated through, and their *confusion probabilities* must be calculated as described in **Section 2** of the paper.  The *confusion probability* represents the likelihood that one word would be confused for the other word, based mostly on their Levenshtein edit distances.  This will essentially create a network of what words are similar to other words in the language.  The assumption behind this is that although languages will vary in their phonological representation of concepts, even when closely related, that this network of word-pair relations will remain closer to constant due to uniform language shifting. 

The paper describes using the frequency of each word as a variable in calculating this confusion probability.  As our dataset contains no information about the frequency of each word, we will have to assume a uniform likelihood for each word.

The output of this component will be a square matrix, where each row and column represents a particular word meaning, and the value at each row and column represents the confusion probability for the words at that row and column.  These matrices must all be the same dimensions, consisting of all word meanings in the dataset, whether or not a particular language has data in for a word.  The values should be normalized by some means; the paper suggests normalizing so that all values in the matrix add up to equal 1.

This leads to the potential problem of how to deal with 0 values when comparing languages;  should they be treated as 0 for the calculation, or should they be entirely ignored?

### Intra-language Processing

For this part, the matrices for all languages from the last component will be used as the input.  Based on these values, two separate distance calculations must be made:  The *Kullback-Liebler distance*, and the *Rao distance*.

Both of these are based on the *geometric path* of each language pairing and various mutations thereof.  As described in the paper:

>The geometric path between two distributions P and Q is a conditional distribution R with a continuous parameter 'a' such that at a=0, the distribution is P, and at a=1 it is Q.

The equations involved in these calculations are described in further detail in **Section 3** of the paper.

The output of this component will consist of 2 matrices, where the rows and columns represent all languages in the collection.  The value at each row and column will represent the distance measurement for the languages at that row and column; the KL-distance for one matrix, and the Rao distance for the other.  

### Tree Construction

This component will take the distance-measurement matrices from the previous component and construct a tree demonstrating a proposed lineage for each language in the collection.  The paper describes using a 3rd party program to accomplish this, namely the NEIGHBOR program from the [PHYLIP](http://evolution.genetics.washington.edu/phylip.html) package.  The feasibility of utilizing this needs to be determined.  It may be necessary to find another suitable program or library, or we may have to write our own custom clustering algorithm.

## The Paper

*To be determined*

## The Presentation

*To be determined*


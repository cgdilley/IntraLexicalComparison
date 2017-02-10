import os
import math


# calculates the normaliser for the conditional distribution, being the sum of the
# weighted geometric means of values from P and Q
# This value is known as the Chernoff coefficient or Helliger path (Basseville,1989)
def k_norm(a, p, q):

    # the final sum product
    k_sum = 0
    # for every row in the matrix
    for i in range(len(p)):
        # for every column in the matrix
        for j in range(len(p)):
            # apply the formula to the entries
            if p[i][j] != 0.0 and q[i][j] != 0.0:
                k_sum += math.pow(p[i][j], 1 - a) * math.pow(q[i][j], a)
    # return the calculated sum
    return k_sum


# calculates the differential of the normaliser with regard to α
def k1_norm(a, p, q):

    # the final sum product
    k1_sum = 0
    # for every row in the matrix
    for i in range(len(p)):
        # for every column in the matrix
        for j in range(len(p)):
            # apply the formula to the entries
            if p[i][j] != 0.0 and q[i][j] != 0.0:
                k1_sum += math.log((q[i][j] / p[i][j]), 2) * math.pow(p[i][j], 1 - a) * math.pow(q[i][j], a)
    # return the calculated sum
    return k1_sum


# calculate the second-order differential of the normaliser with regard to α.
def k2_norm(a, p, q):

    # the final sum product
    k2_sum = 0
    # for every row in the matrix
    for i in range(len(p)):
        # for every column in the matrix
        for j in range(len(p)):
            # apply the formula to the entries
            if p[i][j] != 0.0 and q[i][j] != 0.0:
                log = math.pow(math.log((q[i][j] / p[i][j]), 2), 2)
                k2_sum += log * math.pow(p[i][j], 1 - a) * math.pow(q[i][j], a)
    # return the calculated sum
    return k2_sum


# calculates the Kullback-Liebler distance
def kl_distance(p, q):

    # get the normalizer given α = 1
    k1 = k1_norm(1, p, q)
    # get the normalizer given α = 0
    k2 = k1_norm(0, p, q)

    # average the commutations
    kl_dist = (k1 - k2) / 2

    # return the calculated distance
    return kl_dist


# Fisher information along the path R from P to Q at point α using k and its first two derivatives.
def fisher_info(a, p, q):

    # get the normalizers k, k1 and k2
    k = k_norm(a, p, q)
    k1 = k1_norm(a, p, q)
    k2 = k2_norm(a, p, q)

    # apply the Fischer Information formula
    fi = ((k * k2) - math.pow(k1, 2)) / math.pow(k, 2)

    # return the calculated product
    return fi


# The Rao distance r(P, Q) along R can be approximated by the square root of the Fisher information
# at the path’s midpoint α = 0.5.
def rao_dist(p, q):

    # get the fisher information, using α = 0.5
    fi = fisher_info(0.5, p, q)
    # calculate the rao distance
    rao = math.sqrt(fi)

    # return the calculated product
    return rao


#######################################################################################################################
# ADJUST THE MATRICES


def process_file(file, size, meanings):

    # open and read the file
    l_file = open(file)
    l_lines = l_file.readlines()

    # iterate the lines in the file to find which meanings are present.
    # add them to the dictionary, alongside with the indexes in this file.
    j = 0  # counter
    l_meanings = {}  # meaning to small index
    l_indexes = {}  # small index to big index
    l_values = {}  # small index to values

    for l in l_lines:
        # get the current meaning
        row = l.split("\t")
        mean = row[0]

        if mean not in l_meanings and mean != "\n":
            l_meanings[mean] = j

            if j not in l_indexes:
                l_indexes[j] = meanings[mean]

            # get the values of each row and assign to the corresponding meaning index
            values = row[1].split(" ")

            # remove the last space
            values.pop()

            l_values[j] = values

            # increment the counter
            j += 1

    # close the file
    l_file.close()
    # return the constructed matrix
    return construct_matrix(size, l_indexes, l_meanings, l_values)


def construct_matrix(size, l_indexes, l_meanings, l_values):

    # create a matrix filled with zeroes
    # the size of the matrix corresponds to the meanings dictionary size (all of the meanings in corpus)
    # each entry is a list of the same size with zero values
    lm = [[0.0 for i in range(size)] for j in range(size)]

    for lmean in l_meanings:
        # its index in the language matrix (small)
        small_ind = l_meanings[lmean]

        # its index in the main matrix (big)
        b_ind = l_indexes[small_ind]

        # values of this meaning in the language matrix
        values = l_values[small_ind]

        for v_small_ind in range(len(values)):
            # find the values index in the big matrix
            if v_small_ind in l_indexes:
                v_big_ind = l_indexes[v_small_ind]

                # in the big matrix, in the list of index b_ind
                # find the value of index v_big_ind
                # and change it's value for the current one in the values list
                lm[b_ind][v_big_ind] = float(values[v_small_ind])

    return lm


#######################################################################################################################

# open the file object
file = open('lm_normalized_dedup', 'r')

# read the file
lines = file.readlines()

# a dictionary with all the meanings from the file and their indexes
meanings = {}

# a counter to use for the meanings indexes
m_index = 0

# list of all the languages
langs = []

# iterate through the file
for line in lines:
    # add the languages to the language dictionary, alongside their indexes
    if line.startswith("#"):
        langs.append(line)
    # add the meaning and the corresponding index to the meanings dictionary
    else:
        # extract the meaning
        ln = line.split("\t")
        meaning = ln[0]
        # make sure it's not yet in the dictionary
        if meaning not in meanings:
            if meaning != "\n":
                meanings[meaning] = m_index
                # increment the counter
                m_index += 1

for mng in meanings:
    print(mng, meanings.get(mng))


# find the size of the to-be-built matrix
size = len(meanings)

print("Size of the matrix and of its rows: ", size)
print("number of languages: ", len(langs))


#######################################################################################################################

# iterate the files in the directory and construct a matrix for each file/language
directory = "lm/"
files = os.listdir(directory)

# make a dictionary from language to its matrix
lang_matrices = {}

# make a dictionary from a language to its index
lang_ind = 0  # index counter
languages = {}

for file in files:
    # add the language to the map
    languages[file] = lang_ind
    lang_ind += 1

    # construct the file name
    filename = "lm/" + file

    # make the matrix for this language
    matrix = process_file(filename, size, meanings)

    # add the language and its matrix to the dictionary
    lang_matrices[file] = matrix


with open('langs.txt', 'w') as file:
    for lang in languages:
        output = (str(lang[3:]).replace('_', '') + "          ")[:10]
        file.write(output + "=" + str(languages[lang]) + "\n")

#######################################################################################################################
# CONSTRUCT THE LANGUAGE DISTANCES MATRICES

# matrices of size languages filled with zeroes
lang_KL_dist = [[0 for i in range(len(languages))] for j in range(len(languages))]
lang_rao_dist = [[0 for i in range(len(languages))] for j in range(len(languages))]

# for each language
for lang1 in languages:
    # find its index
    l1_index = languages[lang1]
    # find its matrix
    l1_matrix = lang_matrices[lang1]

    # go through the languages again to compare to the first language
    for lang2 in languages:
        # get the index
        l2_index = languages[lang2]
        # get the matrix
        l2_matrix = lang_matrices[lang2]

        # calculate distances
        kl = kl_distance(l1_matrix, l2_matrix)
        rao = rao_dist(l1_matrix, l2_matrix)

        # add to matrices
        lang_KL_dist[l1_index][l2_index] = kl
        lang_rao_dist[l1_index][l2_index] = rao


# write to file
new_file = open("kl.txt", "w")

for i in range(len(lang_KL_dist)):
    for j in range(len(lang_KL_dist[i])):
        new_file.write(str(lang_KL_dist[i][j]))
        new_file.write(" ")
    new_file.write("\n")

new_file.close()

#
# write to file
new_file = open("rao.txt", "w")

for i in range(len(lang_rao_dist)):
    for j in lang_rao_dist[i]:
        new_file.write(str(j))
        new_file.write(" ")
    new_file.write("\n")

new_file.close()

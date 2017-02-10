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
            p_val = p[i][j]
            q_val = q[i][j]
            frac = (q_val / p_val)
            log = math.log(frac, 2)
            pow_p = math.pow(p_val, 1 - a)
            pow_q = math.pow(q_val, a)
            k1_sum += log * pow_p * pow_q
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
            log = math.pow(math.log((p[i][j] / q[i][j]), 2), 2)
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
    fi = (k * k2) - math.pow(k1, 2) / math.pow(k, 2)

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


###################################################################################################


matrices = {'x': [[0.102, 0.027, 0.023, 0.024, 0.024],
                 [0.028, 0.107, 0.024, 0.026, 0.015],
                 [0.024, 0.024, 0.107, 0.023, 0.023],
                 [0.025, 0.025, 0.022, 0.104, 0.023],
                 [0.026, 0.015, 0.023, 0.025, 0.111]],
            'y': [[0.102, 0.024, 0.023, 0.027, 0.024],
                 [0.015, 0.107, 0.026, 0.024, 0.028],
                 [0.024, 0.024, 0.107, 0.023, 0.023],
                 [0.025, 0.022, 0.025, 0.104, 0.023],
                 [0.015, 0.026, 0.023, 0.025, 0.111]],
            'w': [[0.102, 0.024, 0.023, 0.027, 0.024],
                 [0.015, 0.107, 0.026, 0.024, 0.028],
                 [0.024, 0.024, 0.107, 0.023, 0.023],
                 [0.025, 0.022, 0.025, 0.104, 0.023],
                 [0.015, 0.026, 0.023, 0.025, 0.111]],
            'z': [[0.102, 0.027, 0.023, 0.024, 0.024],
                 [0.028, 0.107, 0.024, 0.026, 0.015],
                 [0.024, 0.024, 0.107, 0.023, 0.023],
                 [0.025, 0.025, 0.022, 0.104, 0.023],
                 [0.026, 0.015, 0.023, 0.025, 0.111]]}

# create a list of all languages
languages = []
for lang in matrices.keys():
    languages.append(lang)

# go through the list of the languages
while languages:
    # get the first language name and delete if from the list
    p_lang = languages.pop(0)

    # find the matrix that is associated with this language in the map
    p_mtx = matrices.get(p_lang)

    # delete this matrix from the map
    del matrices[p_lang]

    # go through the remaining languages and compare their matrices to the p language matrix
    for q_lang in languages:
        q_mtx = matrices.get(q_lang)

        print(p_lang, " vs. ", q_lang,)
        print("KL Distance: ", kl_distance(p_mtx, q_mtx))
        print("Rao distance: ", rao_dist(p_mtx, q_mtx), "\n")

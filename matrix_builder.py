import math

class MatrixBuilder:

    def build(this,vocabulary_dict):
        matrix = {}
        different_docs = []
        df_square_sums = {}
        for word,doc_ids in vocabulary_dict.items():
            if word == '':
                continue
            if word not in matrix:
                matrix[word] = {}
                matrix[word]['df'] = 0
            for doc_id in doc_ids:
                if doc_id in matrix[word]:
                    matrix[word][doc_id] += 1
                else:
                    matrix[word][doc_id] = 1
                    matrix[word]['df'] += 1
                    if doc_id not in different_docs:
                        different_docs.append(doc_id)
            for doc_id in list(set(doc_ids)):
                if doc_id not in df_square_sums:
                    df_square_sums[doc_id] = 0
                df_square_sums[doc_id] += math.pow(matrix[word][doc_id],2)
        for word,other in matrix.items():
            matrix[word]['idf'] = math.log(len(different_docs)/matrix[word]['df'])
        return matrix,df_square_sums

    def normalize(self,matrix,df_square_sums):
        new_matrix = {}
        for word,items in matrix.items():
            new_matrix[word] = {}
            for doc_id,square_sum in df_square_sums.items():
                if doc_id in items:
                    new_matrix[word][doc_id] = matrix[word][doc_id]/math.sqrt(square_sum)
        return new_matrix
class DictEncoder:

    def endoce_dict(this,vocabulary_dict,title_vocabulary_dict):
        #This will contain the whole dictionary-as-a-string variable.
        final_string = ""

        for word,doc_ids in vocabulary_dict.items():
            final_string+=word
            if word in title_vocabulary_dict:
                title_considered_docs = [] #So as not to insert a doc_id more than once
                final_string+="$"#Title separator
                for title_doc in title_vocabulary_dict[word]:
                    if title_doc in title_considered_docs:
                        continue
                    title_considered_docs.append(title_doc)
                    title_repetitions = title_vocabulary_dict[word].count(title_doc)
                    final_string += str(title_doc) + "#" + str(title_repetitions) + ","
                final_string = final_string[:-1] #Remove the trailing comma
            final_string+="&"#DocumentSeparator
            considered_docs = []
            for doc in doc_ids:
                if doc in considered_docs:
                    continue
                considered_docs.append(doc)
                repetitions = doc_ids.count(doc)
                final_string += str(doc) + "#" + str(repetitions) + ","
            final_string = final_string[:-1] #Remove the trailing comma
            final_string += "%"
        final_string = final_string[:-1] #Remove the trailing sign %
        return final_string

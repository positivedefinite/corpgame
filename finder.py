# Case-sensitive search through notices
# Returns a list of files in which the phrase was found.
# USAGE:
# python notice_finder.py -p "./data/notices" -s "C 37548"

import os, plac, re

def process_doc(doc_path, search_phrase):
    with open(doc_path, 'r', encoding='utf-8') as f:
        text = f.read()
        return re.findall(search_phrase, text)

@plac.annotations(
    path_to_notice_folder = ("Path to the directory with notice HTMLs", "option", "p", str),
    search_phrase = ("Phrase (company name?) to look for in notices", "option", "s", str)
)
def search(path_to_notice_folder = "./", search_phrase = "get_directed_payoffs"):
    for doc_count, doc in enumerate(os.listdir(path_to_notice_folder)):
        #print(doc, doc[len(doc)-2::])
        if doc[len(doc)-2::]=='py' or doc[len(doc)-2::]=='nb':
            doc_path = '/'.join([path_to_notice_folder, doc])
            match = process_doc(doc_path, search_phrase)
            if match!=[]:
                print(doc_count, doc_path, match)
if __name__ == "__main__":
    plac.call(search)



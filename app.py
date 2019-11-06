from flask import Flask, jsonify, request
import json
import sys
import os
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import docx2txt
import json
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

from io import StringIO

app = Flask(__name__)











@app.route('/resume_jd_match/', methods=['POST'])
def resume_jd_match():
    data = request.get_json()
    resume = data['resume_directory']
    jd = data['jd_directory']
    #return resume
    print(resume)
    print(jd)

    '''print("Enter resume Directory ")
    resume = str(input())
    print("Enter Job Description file path")
    jd = str(input())'''
    final_list = []
    # print(resume)
    # print(jd)
    count = 0
    file_cv = os.listdir(resume)
    file_jd = os.listdir(jd)

    # for jd_file in fil_jd:
    # jd_file_name = jd_file

    # jd_text = word2vec(jd+'\\'+str(jd_file_name))
    # print(jd_text)
    # print("Files in "+ resume)

    for a_jd in file_jd:

        #print(jd_file_name)
        jd_extension = a_jd.split(".")[-1]
        if jd_extension == "pdf":
            jd_file_name = a_jd
            jd_text = convert_pdf_to_txt(jd + '\\' + str(jd_file_name))
        if (jd_extension == "docx" or jd_extension == "doc"):
            jd_file_name = a_jd
            jd_text = word2vec_doc(jd + '\\' + str(jd_file_name))

        for i, a in enumerate(file_cv):
            try:
                extension = a.split(".")[-1]
                if extension == "pdf":
                    resume_text = convert_pdf_to_txt(resume + '\\' + str(a))
                    result = cosine_sim(resume_text, jd_text)
                    if result == "0.0":
                        final_list.append({"Resume Ratch Score": "Pdf file encoded cant be read ", "Resume": str(a),
                                           "Job Description": str(a_jd)})
                    else:
                        final_list.append(
                            {"Resume Ratch Score": str(result) + "%", "Resume": str(a), "Job Description": str(a_jd)})

                if (extension == "docx" or extension == "doc"):
                    resume_text = word2vec_doc(resume + '\\' + str(a))
                    result = cosine_sim(resume_text, jd_text)

                    if result == "0.0":
                        final_list.append({"Resume Ratch Score": "Pdf file encoded cant be read ", "Resume": str(a),
                                           "Job Description": str(a_jd)})
                    else:
                        final_list.append(
                            {"Resume Ratch Score": str(result) + "%", "Resume": str(a), "Job Description": str(a_jd)})
            except:
                pass

    return jsonify(final_list)

@app.route('/metadata/',methods=['POST'])
def get_metadata():
    data = request.get_json()
    file_path = data['path']
    files_in_dir = os.listdir(file_path)
    final_list = []
    for file in files_in_dir:
        extension = file.split(".")[-1]
        if extension == "pdf":
            ext_text_list = extract_metadata(file_path + '\\' + str(file))
            #print(type(ext_text_list))
            final_list.append({str(file): str(ext_text_list)})
    #print(final_list)
    return jsonify(final_list)

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr,  laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def word2vec_doc(text_file):
    text_file_extracted = docx2txt.process(text_file)
    return text_file_extracted


def cosine_sim(resume_file, jd_file):
    documents = [resume_file, jd_file]

    count_vectorizer = CountVectorizer()
    sparse_matrix = count_vectorizer.fit_transform(documents)

    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, columns=count_vectorizer.get_feature_names(), index=['resume_file', 'jd_file'])

    answer = cosine_similarity(df, df)
    answer = pd.DataFrame(answer)
    answer = answer.iloc[[1], [0]].values[0]
    answer = round(float(answer), 4) * 100
    match_score = str(answer)
    return match_score


def extract_metadata(path):
    final_list =[]
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    for i in doc.info:
        for keys, values in i.items():
            val = ''
            key = ''
            val = values
            key = keys
            if key == 'CreationDate' or key == 'ModDate':
                final_list.append({str(keys): val})
            else:
                val = val.decode("utf-16")
                final_list.append({str(keys): val})

    return final_list


if __name__ == '__main__':
    app.run()


#[{'Google ml_jd.pdf': [{'Creator': 'Writer'}, {'Producer': 'LibreOffice 6.3'}, {'CreationDate': b"D:20191101123102+05'30'"}]}, {'Machine-Learning-Engineer.pdf': [{'Author': '牋獩整\u206e慊潣獢湥'}, {'Creator': 'Microsoft® Word 2016'}, {'CreationDate': b"D:20160902164621-05'00'"}, {'ModDate': b"D:20160902164621-05'00'"}, {'Producer': 'Microsoft® Word 2016'}]}]
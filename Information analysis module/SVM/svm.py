import logging
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC, SVC
from sklearn.metrics import precision_score, recall_score, f1_score

logging.basicConfig(level=logging.INFO)


class Paragraph:
    def __init__(self, url='', text='', words='', sort=''):
        self.url = url
        self.content = text
        self.sort = sort
        self.words = words

    #
    def sepSentences(self):
        self.sentences = self.content
    #
    def sepWords(self):
        self.words = self.content
    #
    def processData(self):
        self.sepSentences()
        self.sepWords()

def read_all_data(path):
    data_list = []
    data_all = pd.read_excel(path)
    for i in range(len(data_all['text'])):
        d = Paragraph()
        d.content = data_all['text'][i].replace(',', ' ')
        d.sort = data_all['sort'][i]
        data_list.append(d)
    return data_list


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))


def split_test():
    global corpus
    global test_corpus
    data_dir_path = '/SVM/train.xlsx'
    test_dir_path = '/SVM/testdata.xlsx'
    # stopwords_path = '.\\StopWord\\cn_stopwords.txt'
    # punctuation_path = '.\\StopWord\\cn_punctuation.txt'

    data_list = read_all_data(data_dir_path)
    test_list = read_all_data(test_dir_path)
    # print(data_list)

    # data process
    corpus = []
    for i in range(len(data_list)):
        data_list[i].processData()
        corpus.append(str(data_list[i].words))
    test_corpus = []
    for i in range(len(test_list)):
        test_list[i].processData()
        test_corpus.append(str(test_list[i].words))
    # print(test_corpus)

    # LDA
    # logging.info('Training LDA model...')
    cntVector = CountVectorizer(max_features=2000)
    # train_count = count_vect.fit_transform(x_train)
    # tfidf_trainformer = TfidfTransformer()

    # cntVector = TfidfVectorizer(decode_error='replace', encoding='utf-8')
    cntTf = cntVector.fit_transform(corpus)


    # lda = LatentDirichletAllocation(n_components=7, learning_offset=50., max_iter=2000, random_state=0)
    # docres = lda.fit_transform(cntTf)

    test_cnVector = CountVectorizer(max_features=2000)
    test_cntTf = test_cnVector.fit_transform(test_corpus)

    # SVM
    logging.info('SVM classify...')
    # X = cntTf
    # y = [data_list[i].sort for i in range(len(data_list))]
    # print(y)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
    X_train = cntTf
    tfidf_trainformer = TfidfTransformer()
    train_tfidf = tfidf_trainformer.fit_transform(X_train)
    for k in range(1,200):
        select = SelectKBest(chi2, k)
        y_train = [data_list[i].sort for i in range(len(data_list))]
        train_tfidf_chi = select.fit_transform(train_tfidf, y_train)
        svm_model = LinearSVC()  # model = SVC()
        svm_model.fit(train_tfidf, y_train)
        X_test = test_cntTf
        # y_test = [test_list[i].sort for i in range(len(test_list))]
        test_train_tfidf = tfidf_trainformer.fit_transform(X_test)
        select = SelectKBest(chi2, k)
        y_test = [test_list[i].sort for i in range(len(test_list))]
        train_tfidf_chi = select.fit_transform(test_train_tfidf, y_test)
        y_pred = svm_model.predict(X_test)

    # analysis
        p = precision_score(y_test, y_pred, average='macro')
        r = recall_score(y_test, y_pred, average='macro')
        f1 = f1_score(y_test, y_pred, average='macro')
        logging.info('Precision:{:.3f},Recall:{:.3f},F1:{:.3f}'.format(p, r, f1))


def SVM():
    global newcorpus
    data_dir_path = '/SVM/data.xlsx'
    data_list = read_all_data(data_dir_path)
    newcorpus = []
    for i in range(len(data_list)):
        data_list[i].processData()
        newcorpus.append(str(data_list[i].words))
    cntVector = CountVectorizer(max_features=2000)
    cntTf = cntVector.fit_transform(newcorpus)
    logging.info('SVM classify...')
    X = cntTf
    y = [data_list[i].sort for i in range(len(data_list))]
    xlist = [0.1, 1, 10, 100, 1000, 5000, 10000]
    pl = []
    rl = []
    f1l = []
    pr = []
    rr = []
    f1r = []
    for lines in xlist:
        # x = lines/20
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1)
        svm_model = SVC(C=lines,kernel='linear')  # model = SVC()
        svm_model.fit(X_train, y_train)
        y_pred = svm_model.predict(X_test)
        # xlist.append(x)
        # pl.append(precision_score(y_test, y_pred, average='macro'))
        # rl.append(recall_score(y_test, y_pred, average='macro'))
        # f1l.append(f1_score(y_test, y_pred, average='macro'))
        # logging.info('Precision:{:.3f},Recall:{:.3f},F1:{:.3f}'.format(p, r, f1))

        svm_model1 = SVC(C=lines,kernel='rbf')  # model = SVC()
        svm_model1.fit(X_train, y_train)
        y_pred = svm_model1.predict(X_test)
        # xlist.append(x)
        pr.append(precision_score(y_test, y_pred, average='macro'))
        rr.append(recall_score(y_test, y_pred, average='macro'))
        f1r.append(f1_score(y_test, y_pred, average='macro'))
        # plt.title('扩散速度')  # 折线图标题
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示汉字
    plt.xlabel('惩罚因子C')  # x轴标题
    plt.ylabel('准确率')  # y轴标题
    # plt.plot(xlist, pl, marker='o', markersize=3)  # 绘制折线图，添加数据点，设置点的大小
    # plt.plot(xlist, rl, marker='o', markersize=3)
    # plt.plot(xlist, f1l, marker='o', markersize=3)
    plt.plot(xlist, pr, marker='o', markersize=3)  # 绘制折线图，添加数据点，设置点的大小
    plt.plot(xlist, rr, marker='o', markersize=3)
    plt.plot(xlist, f1r, marker='o', markersize=3)

    # for a, b in zip(xlist, p):
    #     plt.text(a, b, b, ha='center', va='bottom', fontsize=10)  # 设置数据标签位置及大小
    # for a, b in zip(xlist, r):
    #     plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
    # for a, b in zip(xlist, f1):
    #     plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
    plt.legend(['precision', 'recall', 'f1' ])
    # plt.legend(['precision', 'recall', 'f1' ,'precison1','recall1','f11'])
    plt.show()


if __name__ == "__main__":
    SVM()
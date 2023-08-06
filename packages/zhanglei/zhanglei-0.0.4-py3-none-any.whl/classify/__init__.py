from classify import run_cnn as rc, process_data as pd


def classify(paragraph):
    sen_list = pd.phrasing(paragraph)
    pd.save_sens(sen_list)
    rc.test()


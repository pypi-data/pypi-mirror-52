import process_data as pd
import run_cnn as rc


def classify(paragraph):
    sen_list = pd.phrasing(paragraph)
    pd.save_sens(sen_list)
    rc.test()


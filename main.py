import os
from config import Config


def get_docs(ace2005_path):
    docs = list()
    for fname in os.listdir(ace2005_path):
        fpath = os.path.join(ace2005_path, fname)
        if not os.path.isdir(fpath):
            continue

        for fname_sub in os.listdir(fpath):
            print('fname_sub :', fname_sub)
            if '.sgm' not in fname_sub:
                continue
            fpath_sub = os.path.join(fpath, fname_sub)
            print('fpath_sub :', fpath_sub)

            raw = fname.split('.sgm')[0]
            # docs.append({
            #     'sgm': self.dir_path.format(dir) + raw + '.sgm',
            #     'apf.xml': self.dir_path.format(dir) + raw + '.apf.xml'
            # })
    return docs


if __name__ == '__main__':
    get_docs(Config.ace2005_path)
    pass

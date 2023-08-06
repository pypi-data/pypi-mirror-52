import requests
import pandas as pd


class YapTool:
    # The URL of the yap REST API.
    yap_url = 'http://localhost:8000/yap/heb/joint'
    # The headers of the morphological analysis result.
    analysis_headers = ['Start', 'End', 'Form', 'Lemma', 'Part of Speech', 'x', 'Features', 'Token']
    dependency_headers = ['Form', 'Lemma', 'Part of Speech', 'x', 'Head', 'Dependent', 'Relation', 'y', 'z']

    def __init__(self):
        self.ma_lattice: pd.DataFrame = None
        self.md_lattice: pd.DataFrame = None
        self.dep_tree: pd.DataFrame = None

    def run_text_analysis(self, text: str):
        res = YapTool._make_get_request({'text': f'  {text}  '})
        self.ma_lattice = YapTool._parse_tsv_to_df(res['ma_lattice'], YapTool.analysis_headers)
        self.md_lattice = YapTool._parse_tsv_to_df(res['md_lattice'], YapTool.analysis_headers)
        self.dep_tree = YapTool._parse_tsv_to_df(res['dep_tree'], YapTool.dependency_headers)

    def get_ma_lattice(self):
        return self.ma_lattice

    def get_md_lattice(self):
        return self.md_lattice

    def get_dep_tree(self):
        return self.dep_tree

    @staticmethod
    def _make_get_request(data):
        r = requests.post(url=YapTool.yap_url, json=data)
        return r.json()

    @staticmethod
    def _parse_tsv_to_df(res: str, headers):
        return pd.read_csv(pd.compat.StringIO(res), sep='\t', names=headers)

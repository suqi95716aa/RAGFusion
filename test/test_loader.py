from unittest import TestCase


class TestLoader(TestCase):

    def test_csv_loader(self):
        from ss_loaders import CSVLoader
        # 详细参数可观察csv build in
        loader = CSVLoader(file_path='../doc/qa-template.csv', csv_args={
            'delimiter': ',',
            'quotechar': '"',
            # 'fieldnames': ['MLB Team', 'Payroll in millions', 'Wins']
        })
        data = loader.load()
        for item in data:
            print(item)

    def test_excel_loader(self):
        from ss_loaders import ExcelLoader
        # 详细参数可观察csv build in
        # loader = ExcelLoader(
        #     file_path='../doc/qa-template.xlsx',
        #     source_column="query",        # 当前行数据的数据来源，以具体的数据代表
        #     metadata_columns=("query",)   # 在excel cols中的元数据，不充当数据源
        # )
        loader = ExcelLoader(
            file_path='../doc/副本副本流程助手终版校验final666.xlsx',
        )
        data = loader.load()
        for item in data:
            print(item)





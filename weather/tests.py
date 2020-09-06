from django.test import TestCase
from .models import WeatherDataRow
from .models import UploadedDocument
from .components import graph_data


class ModelsTestCase(TestCase):
    def setUp(self):
        self.test_document = UploadedDocument.objects.create(document='media/documents/test.csv')
        WeatherDataRow.objects.create(parent_file=self.test_document, date='2020-12-14', min_temp='-5',
                                      max_temp='0', mean_temp='0', heat_degree_days='0', total_rain='22',
                                      total_snow='11', speed_max_gusts='11')

    def test_document_name(self):
        self.assertEqual(self.test_document.document.name, 'media/documents/test.csv')

    def test_weather_row_date(self):
        test_weather_row = WeatherDataRow.objects.get(parent_file_id=self.test_document.id)
        self.assertEqual(str(test_weather_row.date), '2020-12-14')


class ComponentTestCase(TestCase):
    def setUp(self):
        self.test_document = UploadedDocument.objects.create(document='media/documents/test.csv')
        WeatherDataRow.objects.create(parent_file=self.test_document, date='2020-12-14', min_temp='-5',
                                      max_temp='0', mean_temp='0', heat_degree_days='0', total_rain='22',
                                      total_snow='11', speed_max_gusts='11')

    def test_graph_data(self):
        plot_div = graph_data.return_plot_div(self.test_document.id, date__range=['2020-12-14', '2020-12-14'])
        self.assertEqual(type(plot_div), str)
        self.assertGreater(len(plot_div), 10000)

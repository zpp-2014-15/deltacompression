"""Views for charts."""

import pygal
import tempfile
import webbrowser


class BarChartView(object):

    def __init__(self, experiment_result):
        self._result = experiment_result

    def show(self):
        bar_chart = pygal.Bar(y_title="Data to send in MiB")
        bar_chart.title = "Result of experiment"
        bar_chart.x_labels = [n for n, _ in self._result.files_with_results]
        bar_chart.add("Experiment 1", [float(d) / 1024 / 1024 for _, d in
                                       self._result.files_with_results])
        rendered = bar_chart.render()
        file_name = tempfile.mktemp(suffix=".svg")
        svg_file = open(file_name, "w")
        svg_file.write(rendered)
        svg_file.close()
        webbrowser.open(file_name)

"""Views for charts."""

# pylint: disable=E1101
import pygal
import tempfile
import webbrowser


class BarChartView(object):

    def __init__(self, experiment_results):
        self._results = experiment_results
        self._versions = [n for n, _ in self._results[0].versions_with_results]

    def show(self):
        """Method for showing a chart in a browser."""
        bar_chart = pygal.Bar(y_title="Data to send in B")
        bar_chart.title = "Result of experiment"
        bar_chart.x_labels = self._versions
        for result in self._results:
            bar_chart.add(result.getDescription(),
                          [float(d) for _, d in result.versions_with_results])
        bar_chart.config.legend_at_bottom = True
        bar_chart.config.legend_at_bottom_columns = True
        bar_chart.config.human_readable = True
        rendered = bar_chart.render()
        file_name = tempfile.mktemp(suffix=".svg")
        svg_file = open(file_name, "w")
        svg_file.write(rendered)
        svg_file.close()
        webbrowser.open(file_name)

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

from ignition.models import IgnitionRow


def index(request):
	return render(request, 'home.html')
    # return HttpResponse("Hello, world. You're at the ignition index.")


class LineChartJSONView(BaseLineChartView):

    def __init__(self):
        self.num_ticks = 120
        self.keys = ['5','25','50','200','500']

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        # return ["January", "February", "March", "April", "May", "June", "July"]
        return [i for i in range(self.num_ticks)]

    def get_providers(self):
        """Return names of datasets."""
        return self.keys

    def get_data(self):
        """Return 3 datasets to plot."""

        data = list(IgnitionRow.objects.all().order_by('pub_date').values())
        two_hours = data[-self.num_ticks:] # The most recent two hours of data
        keys = ['num_players_{}'.format(key) for key in self.keys]
        num_players_data = [[min(elem[key],50) for elem in two_hours] for key in keys]
        return num_players_data

class LineChartAvgPot(BaseLineChartView):

    def __init__(self):
        self.num_ticks = 120
        self.keys = ['5','25','50','200','500']

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        # return ["January", "February", "March", "April", "May", "June", "July"]
        return [i for i in range(self.num_ticks)]

    def get_providers(self):
        """Return names of datasets."""
        return self.keys

    def get_data(self):
        """Return 3 datasets to plot."""

        data = list(IgnitionRow.objects.all().order_by('pub_date').values())
        two_hours = data[-self.num_ticks:] # The most recent two hours of data
        avg_pot_data = [[float(elem['avg_pot_{}'.format(key)]) / (int(key) / 100) for elem in two_hours] 
        	for key in self.keys]
        avg_pot_data = [[min(elem, 50) for elem in arr] for arr in avg_pot_data] # Assume a max pot size of 2000 BBs
        return avg_pot_data

class LineChartPctFlop(BaseLineChartView):

    def __init__(self):
        self.num_ticks = 120
        self.keys = ['5','25','50','200','500']

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        # return ["January", "February", "March", "April", "May", "June", "July"]
        return [i for i in range(self.num_ticks)]

    def get_providers(self):
        """Return names of datasets."""
        return self.keys

    def get_data(self):
        """Return 3 datasets to plot."""

        data = list(IgnitionRow.objects.all().order_by('pub_date').values())
        two_hours = data[-self.num_ticks:] # The most recent two hours of data
        avg_pot_data = [[float(elem['pct_flop_{}'.format(key)]) / (int(key) / 100) for elem in two_hours] 
        	for key in self.keys]
        avg_pot_data = [[min(elem, 100) for elem in arr] for arr in avg_pot_data] # Assume a max pot size of 2000 BBs
        return avg_pot_data


line_chart = TemplateView.as_view(template_name='line_chart.html')
avg_pot_line_chart = TemplateView.as_view(template_name='line_chart_avg_pot.html')
pct_flop_line_chart = TemplateView.as_view(template_name='line_chart_pct_flop.html')
line_chart_json = LineChartJSONView.as_view()
line_chart_avg_pot_json = LineChartAvgPot.as_view()
line_chart_pct_flop_json = LineChartPctFlop.as_view()

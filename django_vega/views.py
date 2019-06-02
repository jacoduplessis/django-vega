from django.views.generic import TemplateView
import altair as alt


class AltairTemplateView(TemplateView):
    queryset = None
    template_name = 'django_vega/default.html'
    embed_options = {}
    chart_title = None

    def get_queryset(self):
        return self.queryset

    def get_embed_options(self):
        return self.embed_options

    def configure_chart(self):
        chart = self.get_chart()
        if self.chart_title:
            chart = chart.properties(
                title=self.chart_title
            )
        return chart

    def get_spec(self):
        chart = self.configure_chart()
        return chart.to_dict()

    def get_data(self):

        qs = self.get_queryset()
        if qs is None:
            return None
        return alt.Data(values=list(qs))

    def get_chart(self):
        raise NotImplemented

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options'] = self.get_embed_options()
        context['spec'] = self.get_spec()

        return context

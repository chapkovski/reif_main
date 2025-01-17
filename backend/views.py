from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from otree.models import Participant
from .models import Event
from otree.models import Session
from django.shortcuts import redirect, reverse
import pandas as pd




from django.utils import timezone

class PandasExport(View):
    display_name = 'Event export'
    url_name = 'export_events'
    url_pattern = fr'events/export'
    content_type = 'text/csv'

    def get(self, request, *args, **kwargs):
        events = Event.objects.all().values('owner__participant__code', 'owner__session__code', 'owner__round_number', 'name', 'timestamp', 'body', )
        df = pd.DataFrame(data=events)
        if df is not None and not df.empty:
            timestamp = timezone.now()
            curtime= timestamp.strftime('%m_%d_%Y_%H_%M_%S')
            csv_data = df.to_csv(  index=False)
            response = HttpResponse(csv_data, content_type=self.content_type)
            filename = f'events_{curtime}.csv'
            response['Content-Disposition'] = f'attachment; filename={filename}'
            return response
        else:
            return redirect(reverse('ExportIndex'))

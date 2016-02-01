import json
from django_select2.views import AutoResponseView
from core.models import Goal
from django.http import HttpResponse
from core.utils import WikiDataSearch


class IdeaChainedView(AutoResponseView):
    def get_queryset(self):
        goal_id = self.request.GET.get('goal_id', False)
        queryset = self.queryset

        if goal_id:
            queryset = Goal.objects.get(pk=goal_id)
            queryset = queryset.goal_ideas.all()

        return self.widget.filter_queryset(self.term, queryset)


def heavy_data_2(request):
    if request.GET.get('term'):
        wiki_results = WikiDataSearch(request.GET.get('term'), request.LANGUAGE_CODE)
        wiki_data = []

        for wiki_result in wiki_results:
            name = wiki_result[0],
            definition = wiki_result[1],
            defined_meaning_id = wiki_result[2]

            wiki_data.append({
                'id': json.dumps({
                    'name': name[0],
                    'definition': definition[0],
                    'defined_meaning_id': defined_meaning_id
                }),
                'text': definition
            })

        response = json.dumps({
            'err': 'nil',
            'results': wiki_data
        })

        return HttpResponse(response, content_type='application/json')
    return HttpResponse(json.dumps({'err': 'nil', 'results': []}), content_type='application/json')

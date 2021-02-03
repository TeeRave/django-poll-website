from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        response_kwargs.setdefault('content_type', self.content_type)
        question = context['question']
        existing_questions = self.request.session.get('user_choices', {}).get(self.request.session.session_key, {}).get('questions_choices', {}).keys()
        if question.question_text in existing_questions:
            question = get_object_or_404(Question, pk=question.id)
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if not request.session or not request.session.session_key:
        # request.session.create()
        request.session.save()

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        session_key = request.session.session_key

        user_choices = request.session.get('user_choices', {})

        if not user_choices.get(session_key):
            user_choices[session_key] = {'questions_choices': {question.question_text: selected_choice.choice_text}}
        else:
            user_choices[session_key]['questions_choices'].update({question.question_text: selected_choice.choice_text})

        request.session['user_choices'] = user_choices
        request.session['selected_choice_text'] = selected_choice.choice_text
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

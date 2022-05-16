"""views"""
from django.db import models
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice


class IndexView(
    generic.ListView[Question]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object # pylint-django/issues/361
    """Display the 5 latests poll questions."""

    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self) -> models.QuerySet[Question]:
        """Return the last five published questions."""
        # pylint: disable=no-self-use
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(
    generic.DetailView[Question]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object # pylint-django/issues/361
    """Display the question text for a given poll."""

    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self) -> models.QuerySet[Question]:
        """Return questions are published."""
        return self.model.objects.filter(pub_date__lte=timezone.now())


class ResultsView(
    generic.DetailView[Question]
):  # pylint: disable=too-few-public-methods,unsubscriptable-object # pylint-django/issues/361
    """Display the results for the question."""

    model = Question
    template_name = "polls/results.html"


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    """Display the question voting form."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

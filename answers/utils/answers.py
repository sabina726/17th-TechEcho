from answers.models import Vote as AnswerVotes
from django.db.models import OuterRef, Subquery, CharField, Value
from django.db.models.functions import Coalesce

def parse_answers(request, question, answer_order_type):
    answer_subquery = AnswerVotes.objects.filter(user=request.user, answer=OuterRef('pk')).values("vote_type")[:1]
    answers = question.answer_set.annotate(
        voted=Coalesce(Subquery(answer_subquery, output_field=CharField()), Value("neither"))
    ).select_related("user")
    if answer_order_type == "id":
        return answers.order_by("-id")
    else:
        return answers.order_by("-votes_count", "-id")
        

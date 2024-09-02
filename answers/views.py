from django.shortcuts import render, redirect, get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from questions.models import Question
from answers.models import Answer

def index(request, id):
    if request.method == "POST":
        question = get_object_or_404(Question, pk=id)
        answer = question.answer_set.create(content=request.POST["content"])
        return redirect("questions:show", id=id)

@csrf_exempt
def delete_answer(request, id):
    if request.method == "POST":
        answer = get_object_or_404(Answer, pk=id)
        answer.delete()
        return redirect("questions:show", id=answer.question.id)

@csrf_exempt
def upvote_answer(request, id):
    if request.method == "POST":
        answer = get_object_or_404(Answer, pk=id)
        answer.votes_count += 1
        answer.save()
        return redirect("questions:show", id=answer.question.id)

@csrf_exempt
def downvote_answer(request, id):
    if request.method == "POST":
        answer = get_object_or_404(Answer, pk=id)
        answer.votes_count -= 1
        answer.save()
        return redirect("questions:show", id=answer.question.id)


# def upvote_answer(request, id):
#     if request.method == "POST":
#         answer = get_object_or_404(Answer, id=id)
#         user_vote = Vote.objects.filter(user=request.user, answer=answer).first()

#         if user_vote:
#             if user_vote.vote_type == "downvote":
#                 answer.votes += 2  
#                 user_vote.vote_type = "upvote"
#                 user_vote.save()
#             else:
#                 return redirect("questions:show", id=answer.question.id)  
#         else:
#             answer.votes += 1
#             Vote.objects.create(user=request.user, answer=answer, vote_type="upvote")

#         answer.total_votes = answer.votes
#         answer.save()
#         return redirect("questions:show", id=id)

# def downvote_answer(request, answer_id):
#     if request.method == "POST":
#         answer = get_object_or_404(Answer, id=answer_id)
#         user_vote = Vote.objects.filter(user=request.user, answer=answer).first()

#         if user_vote:
#             if user_vote.vote_type == "upvote":
#                 answer.votes -= 2  
#                 user_vote.vote_type = "downvote"
#                 user_vote.save()
#             else:
#                 return redirect("questions:show", id=answer.question.id)
#         else:
#             answer.votes -= 1
#             Vote.objects.create(user=request.user, answer=answer, vote_type="downvote")

#         answer.total_votes = answer.votes
#         answer.save()
#         return redirect("questions:show", id=id)
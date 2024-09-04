def upvoted_or_downvoted_or_neither(request, question) -> str:
    # to avoid DoesNotExist exception if not found
    if not request.user.is_authenticated:
        return "neither"

    if not question.has_voted(request.user):
        return "neither"

    return question.questionuservotes_set.get(user=request.user).vote_status




# only three states of (upvote, downvote) allowed
# 1. (False,False) 
# 2. (True,False)
# 3. (False,True) 
# current_status, vote_change -> new_status, count_change
# upvoted         downvoted      downvoted   -2
# upvoted         upvoted        neither     -1
# neither         downvoted      downvoted   -1
# neither         upvoted        upvoted     1
# downvoted       downvoted      neither     1
# downvoted       upvoted        upvoted     2
def validate_votes_input(current_vote_status,vote_change) -> tuple:
    if vote_change not in ("upvoted", "downvoted"):
        return (current_vote_status, 0)

    if current_vote_status == vote_change:
        return ("neither", -1 if vote_change == "upvoted" else 1)
    
    if current_vote_status == 'neither':
        return (vote_change, 1 if vote_change == "upvoted" else -1)

    return (vote_change, -2 if vote_change == "downvoted" else 2)


    


    

    



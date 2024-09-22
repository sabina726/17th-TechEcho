from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from editors.utils.run_code import run_javascript_code, run_python_code
from lib.utils.student_required import student_required


@login_required
@student_required
def index(request):
    if request.POST:
        code = request.POST.get("code")
        language = request.POST.get("language")
        if language == "javascript":
            result = run_javascript_code(code)
        elif language == "python":
            result = run_python_code(code)
        else:
            return JsonResponse({"error": "Unsupported language"}, status=400)
        return JsonResponse({"result": result})
    return render(request, "editors/index.html")

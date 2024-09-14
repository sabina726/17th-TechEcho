from django.http import JsonResponse
from django.shortcuts import render

from editors.utils.run_code import run_javascript_code


def index(request):
    if request.POST:
        code = request.POST.get("code")
        language = request.POST.get("language")

        if language == "javascript":
            result = run_javascript_code(code)
        else:
            return JsonResponse({"error": "Unsupported language"}, status=400)

        return JsonResponse({"result": result})

    return render(request, "editors/index.html")

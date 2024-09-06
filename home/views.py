from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        # 用戶已登入，傳遞用戶信息到模板
        context = {"user": request.user, "is_authenticated": True}
    else:
        # 用戶未登入，傳遞相應的上下文
        context = {"is_authenticated": False}
    return render(request, "home/index.html", context)

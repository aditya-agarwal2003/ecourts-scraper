from django.shortcuts import render
from .selenium_scraper import run_selenium_scraper

# def case_form(request):
#     if request.method == "POST":
#         case_type = request.POST.get("case_type")
#         case_year = request.POST.get("case_year")
#         case_status = request.POST.get("case_status")

#         data = run_selenium_scraper(case_type, case_year, case_status)

#         return render(request, "fetcher/case_form.html", {
#             "data": data,
#         })

#     return render(request, "fetcher/case_form.html")

def case_form(request):
    if request.method == "POST":
        case_type = request.POST.get("case_type")
        case_no = request.POST.get("search_case_no")
        case_year = request.POST.get("case_year")
        case_status = request.POST.get("case_status")

        data = run_selenium_scraper(case_type, case_no, case_year, case_status)

        return render(request, "fetcher/case_form.html", {
            "data": data,
        })

    return render(request, "fetcher/case_form.html")
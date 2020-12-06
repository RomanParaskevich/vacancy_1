import os
import django


os.environ["DJANGO_SETTINGS_MODULE"] = 'vacancy.settings'
django.setup()


from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from vacancies.models import Company, Specialty, Vacancy


def index_view(request):

    specializations = Specialty.objects.all()
    companies = Company.objects.all()

    context = {
        'specializations': specializations,
        'companies': companies,
    }
    return render(request, 'index.html', context=context)


class VacanciesView(TemplateView):
    template_name = 'all_vacancies.html'

    def get_context_data(self, **kwargs):
        vacansies = Vacancy.objects.all()
        return {
            'vacansies': vacansies,
        }


class VacancyView(TemplateView):
    template_name = 'vacancy.html'

    def get_context_data(self, vacansy_id, **kwargs):
        vacansy = get_object_or_404(Vacancy, id=vacansy_id)
        return {
            'vacansy': vacansy,
        }


class CompanyView(TemplateView):
    template_name = 'company.html'

    def get_context_data(self, company_id, **kwargs):
        company = get_object_or_404(Company, id=company_id)
        vacansies = Vacancy.objects.filter(company=company).select_related('company', 'specialty')
        return {
            'company': company,
            'vacansies': vacansies,
        }


class CatView(TemplateView):
    template_name = 'cat_vacancies.html'

    def get_context_data(self, specialization, **kwargs):
        speciality = get_object_or_404(Specialty, code=specialization)
        vacansies = Vacancy.objects.filter(specialty=speciality).select_related('company', 'specialty')
        return {
            'title': speciality.title,
            'vacansies': vacansies,
        }

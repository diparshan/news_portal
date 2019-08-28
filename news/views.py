from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView, DeleteView
from news import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.text import slugify
from news.models import News, Comment

from django.views import View

# Create your views here.

class CreateNewsView(LoginRequiredMixin, CreateView):
    login_url = "/accounts/login/"
    form_class = forms.CreateNewsForm
    template_name = "news/create_news.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        title = form.cleaned_data['title']
        news = form.save(commit=False)
        news.reporter = self.request.user
        news.slug = slugify(title)
        news.save()
        return super(CreateNewsView, self).form_valid(form)

    def form_invalid(self, form):
        return super(CreateNewsView, self).form_invalid(form)

# class NewsList(ListView):
#     model = News
#     context_object_name = 'news_list'
#     template_name='index.html'
#     ordering = ['-created_at']

class NewsTemplateView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = News.objects.all()
        context["latest_news"] = news.order_by("-created_at")[:10]
        context["political_news"] = news.filter(category="0").order_by("-created_at")
        context["sport_news"] = news.filter(category="1").order_by("-created_at")
        context["fashion_news"] = news.filter(category="2").order_by("-created_at")
        context["technology_news"] = news.filter(category="3").order_by("-created_at")
        context["popular_mews"] = news.order_by("-count")
        return context

class NewsCategoryView(ListView):
    model = News
    ordering = ['-created_at']
    context_object_name = "category_list"
    template_name = "news/category_news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs.get('category')
        return context
    

    def get_queryset(self):
        print(self.kwargs)
        category = self.kwargs.get('category')
        category_key = [ item[0] for item in  News.CATEGORY if item[1]==category][0]
        return News.objects.filter(category=category_key)
    
class NewsDetailView(DetailView):
    model = News
    template_name = "news/detail_news.html"
    context_object_name = "news"
    # success_url = reverse_lazy("news_detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(news=self.object)
        self.object.count = self.object.count +1
        self.object.save()
        return context
    

class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    template_name = "news/update_news.html"
    fields = ("title", "story")
    success_url = reverse_lazy("home")

class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy("home")

# class NewsDeleteView(LoginRequiredMixin, DeleteView):
#     model = News
#     template_name = "news/delete_news.html"
#     success_url = reverse_lazy("home")

@login_required
def create_comment(request, **kwargs):
    data = request.POST
    news = get_object_or_404(News, pk=kwargs.get('pk'))
    feedback = data.get('feedback')
    comment_by = request.user
    payload = {"news": news, "comment_by": comment_by, "feedback":feedback}
    comment = Comment(**payload)
    comment.save()
    return render(request, "news/comment.html", {"comment": comment})
    

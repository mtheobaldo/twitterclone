from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.views.generic.detail import SingleObjectMixin
from .models import Profile, Post
from django.core.urlresolvers import reverse, reverse_lazy
from django import forms
from django.http import HttpResponseRedirect


# Create your views here.
class PublicListView(ListView):
	model = Post
	paginate_by = 10

class ProfileDetailView(DetailView):
	model = Profile

class MyFeedView(ListView):
	model = Post
	paginate_by = 10
	template_name = "microblog/myfeed.html"

	def get_queryset(self):
		my_profile, created = Profile.objects.get_or_create(user = self.request.user)
		following_profile_list = list(my_profile.following.all())
		following_profile_list.append(my_profile)
		return Post.objects.filter(profile__in = following_profile_list)

class PostCreateView(CreateView):
    model = Post
    fields = ['body']

    def get_success_url(self):
        return reverse('microblog:allposts')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.profile = self.request.user.profile_set.all()[0]
        post.save()
        return super(PostCreateView, self).form_valid(form)


class ProfileCreateView(CreateView):
	model = Profile
	fields = ("bio", "profile_picture", "following")

	def get_success_url(self):
		return reverse('microblog:profiledetail', args=(self.object.pk,))

	def form_valid(self, form):
		profile = form.save(commit=False)
		profile.user = self.request.user
		profile.save()
		return super(ProfileCreateView, self).form_valid(form)

class ProfileUpdateView(UpdateView):
	model = Profile
	fields = ['bio', 'profile_picture']

	def get_success_url(self):
		return reverse('microblog:profiledetail', args=(self.object.pk,))

class FollowFormView(SingleObjectMixin, View):
	model = Profile
	def post(self, *args, **kwargs):
		my_profile = self.request.user.profile_set.all()[0]
		my_profile.following.add(self.get_object())
		my_profile.save()
		return HttpResponseRedirect(reverse('microblog:followsuccess', args=(self.get_object().pk,)))

class FollowSuccessView(DetailView):
	template_name = 'microblog/follow_success.html'
	model = Profile
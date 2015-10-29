from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views

urlpatterns = [
#   url(r'^$', login_required(views.IdeaListView.as_view()), name="idealist"),
	url(r'^$', (views.PublicListView.as_view()), name="allposts"),
	url(r'^profile/(?P<pk>\d+)/$', (views.ProfileDetailView.as_view()), name="profiledetail"),
	url(r'^myfeed/$', login_required(views.MyFeedView.as_view()), name="myfeed"),
	url(r'^user/(?P<pk>\d+)/follow/$', login_required(views.FollowFormView.as_view()), name = "follow"),
	url(r'^user/(?P<pk>\d+)/follow/success/$', login_required(views.FollowSuccessView.as_view(template_name='microblog/follow_success.html')), name = "followsuccess"),
	url(r'^profile/create/$', login_required(views.ProfileCreateView.as_view()), name="profilecreate"),
	url(r'^profile/edit/(?P<pk>\d+)/$', login_required(views.ProfileUpdateView.as_view()), name="editprofile"),
	url(r'^newtwitt/$', login_required(views.PostCreateView.as_view()), name="newtwitt"),
]

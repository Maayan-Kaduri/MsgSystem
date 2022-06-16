from django.urls import path as url
from MessageHandling import views


urlpatterns = [
    url('allunreadmsg/', views.unreadMessageApi),
    url('allmsg/', views.allMessageApi),
    url('writemsg/', views.writeMessageApi),
    url('deletemsg/<int:id>', views.deleteMsgApi),
    url('readmsg/<int:id>', views.readMsgApi)
]
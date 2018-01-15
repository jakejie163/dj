from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)

from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, 
    CsrfExemptMixin, JsonRequestResponseMixin,
)

from .models import Course


class OwnerMixin(object):   # 提供过滤功能
    def get_queryset(self):
        qs = super(ManageCourseListView,self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):     # 提供延后自动保存user的功能
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):     # 基于Course模型
    model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):   # 定制表单
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    

# 有一个问题，登录用户是否可以编辑其他人的内容?
# user有对某个model的权限
class CourseCreateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin,
                       OwnerCourseMixin,
                       DeleteView):
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


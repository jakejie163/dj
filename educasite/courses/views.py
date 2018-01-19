from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import (
    TemplateResponseMixin, View
)
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView

)
from django.forms.models import modelform_factory
from django.apps import apps
from django.db.models import Count

from braces.views import (
    LoginRequiredMixin, PermissionRequiredMixin, 
    CsrfExemptMixin, JsonRequestResponseMixin,
)

from .models import (
    Subject, Course, Module, Content
)
from .forms import ModuleFormSet


class OwnerMixin(object):   # 提供过滤功能
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):     # 提供延后自动保存user的功能
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):     # 基于Course模型
    model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):   # 定制表单
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('courses:manage_course_list')
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    

class CourseCreateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin, #bug?
                       OwnerCourseEditMixin,
                       UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin,
                       OwnerCourseMixin,
                       DeleteView):
    success_url = reverse_lazy('courses:manage_course_list')
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response(
            {
                'course': self.course,
                'formset': formset
            } 
        )

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:manage_course_list')

        return self.render_to_response(
            {
                'course': self.course,
                'formset': formset
            } 
        )


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model('courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        form = modelform_factory(
            model, 
            exclude=['owner', 'created', 'updated'],
        )
        return form(*args, **kwargs)
    
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(
            Module,
            id = module_id,
            course__owner = request.user
        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(       # 决定了是新建还是更新已存在content
                self.model,
                id = id,
                owner = request.user
            )
        return super(ContentCreateUpdateView, self).dispatch( 
            request, module_id, model_name, id
        )

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            self.model,
            instance = self.obj,
            data = request.POST,
            files = request.FILES,
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(
                    module = self.module,
                    item = obj
                )
            return redirect('courses:module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})

        
class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(
            Content,
            id = id,
            module__course__owner = request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('courses:module_content_list', module.id)

    
class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'
    
    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})


# 处理ajax行为服务器端视图, 功能是更新每个对象的order
class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id, course__owner=request.user)\
                    .update(order=order)
        return self.render_json_response({'saved':'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id, module__course__owner=request.user)\
                    .update(order=order)
        return self.render_json_response({'saved':'OK'})


# 公共展示部分
class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        subjects = Subject.objects.annotate(
            total_courses = Count('courses')
        )
        courses = Course.objects.annotate(
            total_modules = Count('modules')
        )
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response(
            {
                'subjects': subjects,
                'subject': subject,
                'courses': courses
            }
        )


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

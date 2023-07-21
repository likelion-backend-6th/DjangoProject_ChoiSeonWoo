from datetime import datetime

from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        # 폼에서 입력한 날짜 정보
        new_publish_date = form.data.get('publish_0')
        new_publish_time = form.data.get('publish_1')
        new_publish_microsecond = datetime.now().microsecond
        datetime_str = f"{new_publish_date} {new_publish_time}.{new_publish_microsecond:06d}"
        new_publish = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")

        # 데이터 수정
        if change:
            # DB에 저장된 기존 데이터의 날짜 정보
            existing_publish_data = Post.objects.get(id=obj.id).publish
            # 폼에서 날짜/시각을 변경하지 않은 경우
            if existing_publish_data.strftime('%Y-%m-%d %H:%M:%S') == obj.publish.strftime('%Y-%m-%d %H:%M:%S'):
                obj.publish = existing_publish_data
            # 폼에서 날짜/시각 정보를 변경한 경우
            else:
                obj.publish = new_publish
        # 데이터 생성
        else:
            obj.publish = new_publish

        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Post
from .forms import EmailPostForm


# FBV
def post_list(request):
    post_list = Post.published.all()
    # 페이지당 3개의 게시물로 페이지네이션
    per_page = request.GET.get('per_page', 3)
    paginator = Paginator(post_list, per_page, orphans=1)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # page_number가 정수가 아닌 경우 첫 번째 페이지 제공
        posts = paginator.page(1)
    except EmptyPage:
        # page_number가 범위를 벗어난 경우 결과의 마지막 페이지 제공
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


# CBV
class PostListView(ListView):
    """
    대체 글 목록 뷰
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                    'blog/post/detail.html',
                    {'post': post})


def post_share(request, post_id):
    # id로 글 검색
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # 폼이 제출되었습니다.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 폼 필드가 유효성 검사를 통과
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']}님이 {post.title}을(를) 추천합니다."
            message = f"{post.title}을(를) 다음에서 읽어보세요.\n\n" \
                      f"{cd['name']}의 의견: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
                      [cd['to']])
            sent = True

    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form})
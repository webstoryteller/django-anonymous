"""
URL configuration for anonymous project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin # 사용하지 않으므로 비활성화 또는 삭제
from django.urls import path
from board.views import board, post_write, post_detail
from user.views import signin, signup, signout
from django.conf.urls.static import static # 게시글 불러올 때 img url 연결을 위해 필요
from django.conf import settings # 게시글 불러올 때  img url 연결을 위해 필요
# from user.views import signup


urlpatterns = [
    # path('admin/', admin.site.urls), # 사용하지 않으므로 비활성화 또는 삭제
    path("", board, name="board"), # 아래 또 있으면 "," comma를 찍어야 함  #  주소창 입력 url - http://127.0.0.1:8000
    path("user/signin", signin, name="signin"),  #  주소창 입력 url - http://127.0.0.1:8000/user/signin
    path("user/signup", signup, name="signup"),  #  주소창 입력 url - http://127.0.0.1:8000/user/signup
    path("user/signout", signout, name="signout"),  #  주소창 입력 url - http://127.0.0.1:8000/user/signout 여기서는 로그아웃시키고board로 redirect하도록 구성함.

    path("post/write", post_write, name="post_write"), #  주소창 입력 url - http://127.0.0.1:8000/post/write
    path("post/<int:post_id>", post_detail, name="post_detail"),
]

""" AWS 설정시 주석 처리
# 게시글에서 url img 불러오기 위해 아래 작성
if settings.DEBUG: # settings의 DEBUG가 True이면 <현재는 개발 중인 페이지라서 DEBUG를 True로 해놓음. web server에 옮기면 변경함
    urlpatterns += static('upload', document_root=settings.MEDIA_ROOT) # 정적인 파일을 매칭해서 img 올린 폴더에서 url 추가함
"""
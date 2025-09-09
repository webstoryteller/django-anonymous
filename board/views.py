from django.shortcuts import render, redirect
from board.models import Post, Comment
from django.core.paginator import Paginator # 게시글을 페이지에 몇 개씩 보이게 하는지 설정하는 방법. 페이징.
from django.contrib.auth.decorators import login_required # 로그인 안 했을 경우 로그인 하도록 안내하는 것
                                                          # decorators는 @login_required처럼 '@'로 어느 함수 실행에 앞서 필요한 작동 표기
from django.core.files.storage import default_storage     # image 등 파일 저장할 때 사용하는 함수 가져옴
import uuid                                               # 중복 파일 이름 등록을 막기 위해 UUID 사용


# Create your views here.
def board(request):              # urls.py에서 path에 board 지정
    # 게시글 리스트
    if request.method == "GET":
        page = request.GET.get('page', 1) # default는 1로 잡는다는 뜻
        search_text = request.GET.get('search_text', "") # search_text라는 변수를 search_text라는 parameter로 받음.기본값은 blank
        post_set = Post.objects.filter(
            title__icontains=search_text
            ).order_by('-id') # 제목에 search_text를 포함하고 있으면 검색.icontains의 i는 대소문자를 가리지 않는다는 표시

        # post_set = Post.objects.all().order_by('-id') # db의 post테이블의 레코드 id 오름차순으로 정렬. 최신 게시글이 가장 먼저 보이도록
        paginator = Paginator(post_set, 4) # 페이지마다 4개까지 게시글을 보여준다는 뜻
        # django의 Paginator의 기능을 활용하여 현재 페이지, 전체 페이지 등을 구성할 수 있음
        # 참조 링크 django Pagination : https://docs.djangoproject.com/en/5.2/topics/pagination/
        post_set = paginator.get_page(page) # 위쪽 page에서 가져옴

        # print(post_set)

        context= {
            # "title":"안녕 베어유?"
            "post_set":post_set,
            "search_text":search_text, # 검색했을 때 검색 결과가 여러 페이지에 걸쳐 나올 때 이전글, 다음글 parameter 적용.
        }
        # return render(request, 'index.html', context = context) # index.html 속성 내에서 context를 함께 rendering함
                                                                # indext.html 태그에서 장고 변수 속성으로 추가하여 불러올 수 있음
        return render(request, 'page/index.html', context = context)

    # 게시판에 글쓰기 적용
@login_required(login_url="signin")    # 로그인하지 않은 유저가 접근하면 로그인 페이지로 넘겨주는 것
def post_write(request):
    if request.method=="GET":
        return render(request, "page/post_write.html")
       
    if request.method=="POST":
        title=request.POST["title"]
        content=request.POST["content"]
        img = request.FILES.get('img', None) # image가 있으면 img를 올리고, 없으면 없는 것으로 함. 이렇게 쓰면 request.FILES.get['img'] => 무조건 img를 올려야 함.
        img_url = "" # 이미지가 없을 때 이미지 url 값을 공란으로 함.

        if img:
            # 이미지 저장! anonymous - settings.py - STATIC_URL = 'static/' MEDIA_ROOT = 'upload' # upload라는 폴더에 이미지 저장
            img_name = uuid.uuid4() # randomly generating file names
            # 어쩌.구.저쩌구.png
            # split('.') 함수를 쓰면 ["어쩌", "구", "저쩌구", "png"] 로 파일 이름이 나뉨. [-1] 쓰면 가장 뒤쪽을 기준으로 나눔.
            ext = img.name.split('.')[-1] # 파일 확장자 구하기
            img_url = f"upload/{img_name}.{ext}" #AWS S3에 폴더 upload를 만들어 올림.

            
            """
            # 장고 django 5.2.5 버전에서 default_storage의 3 저장 경로 URL을 터미널창에서 확인하려면 아래 주석을 제거하고 실행한다.
            saved_filename = default_storage.save(img_url, img)

            # 저장된 파일의 URL 가져오기
            uploaded_file_url = default_storage.url(saved_filename)
            print(f"파일이 '{saved_filename}'으로 저장되었습니다. URL: {uploaded_file_url}")
            """

            default_storage.save(img_url, img) #AWS에 저장하는 것. 경로와 파일 이름. 위쪽 주석을 제거하면 이 줄은 주석 처리해서 위 라인 명령어에 따라 터미널창에 나온다.
            # from django.core.files.storage import default_storage의 default_storage를 쓰면 루트 폴더를 지정한다.

            # default_storage.save(f"{img_name}.{ext}", img) # AWS로 대체
            # img_url = f"{img_name}.{ext}" # AWS로 대체
            # 이미지 저장! default_storage는 ANONYMOUS - upload 폴더.
            # pass


        Post(                         # board-models.py의 class Post(models.Model) 로 넘겨 db에 저장
            img_url=img_url,
            user=request.user,
            title=title,
            content=content,
        ).save()

        return redirect('board') # 위쪽에 from django.shortcuts import render 이렇게만 쓰면 redirect에 물결 밑줄이 생기며 에러가 남.
    


def post_detail(request, post_id):  # 게시글 상세 사항. 게시글은 post_id (post 테이블의 레코드 id). django에서 내부적으로 post_id 넘김

    if request.method=="GET":
        # print(post_id) # 터미널 창에 post_id 나오는지 확인하기 위한 것임
        post = Post.objects.get(id=post_id) # post_id는 ANONYMOUS - urls.py에서 설정
        context = {
            "post":post
        }
        return render(request, 'page/post_detail.html', context=context)
    
    """    GET parameter를 이용해 post_id를 가져오는 방법도 있음.   
    def post_detail(request):  # 게시글 상세 사항
        if request.method=="GET":
            post_id = request.GET['post_id']
    """      

    if request.method=="POST":
        content=request.POST['content']
        Comment(
            post_id=post_id,
            content=content,
        ).save()

        return redirect('post_detail', post_id)

        
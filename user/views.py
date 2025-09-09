from django.contrib import messages #각종 메시지 팝업창을 띄우도록 함
from django.shortcuts import render, redirect # redirect : 로그인 실패 때 다른 페이지로 가도록 하는 것
from django.contrib.auth import authenticate, login, logout # 로그인 회원가입 POST method 사용 시
from django.contrib.auth.hashers import check_password, make_password
from user.models import User # import User의 User는 사용자가 만든 것

# Create your views here.

def signin(request):

    # request의 4 가지 method
    # 값 읽기 : GET - URL Parameter 사용 (http://example.com?title=안녕하세요)
    # 값 지우기 : DELETE

    # 값 고치기 (수정) : PUT - body 쪽에 값을 넣어서 전달
    # 값 만들기 (생성) : POST - body 쪽에 값을 넣어서 전달

    if request.method == "GET":
        # print(request.GET['title']) => 브라우저 주소창에 http://127.0.0.1:8000/user/signin?title=안녕하세요 치면 VS에 돌아와 보면 아래 Terminal 창에 "안녕하세요" 나옴
        return render(request, 'page/signin.html')
    
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']      

        user = authenticate(username=username, password=password)  # django의 authenticate는 user와 password를 간편하게 확인할 수 있게 하는 함수
        if user:                   # user가 있고 password가 맞으면
            login(request, user)   # user로 로그인해라
            return redirect('board') # 로그인하면 board (여기서는 main 페이지)로 들어가라
        else:                         # user나 password가 맞지 않으면
            messages.error(request, "입력값을 확인해 주세요.")  # signin 페이지에서 message 출력 태그 작성할 것
            return redirect('signin') # signin 페이지로 돌아가라

def signup(request):
    if request.method == "GET":
        return render(request, 'page/signup.html')
    
    if request.method ==  "POST":
        username=request.POST['username']
        password=request.POST['password']  
        nickname=request.POST['nickname']

        #user=User.objects.filter(username=username) #django ORM을 이용해 이미 가입한 user인지 확인하는 것
        # # exists- 존재하면 True, 존재하지 않으면 False
        #if user.exists():
        if User.objects.filter(username=username).exists():
            messages.error(request, "이미 가입한 아이디입니다.") # signup 페이지에서 message 출력 태그 작성할 것
            return redirect('signup') # signup 페이지로 돌아가라
        else:
            new_user= User(
                username=username,
                password=make_password(password), # django가 비밀번호를 암호화하여 저장하도록 함
                nickname=nickname, # db 필드에서 대소문자를 구분하므로 user/models.py에서 틀린 부분  고친 다음 migration할 것
            )
            new_user.save()
            login(request, new_user)
            return redirect('board')
        
def signout(request):
    if request.method == "GET":
        logout(request)
        return redirect('board')


    


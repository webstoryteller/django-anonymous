처음부터 다시!

※ 매우 중요

(1) VS Code, Python 3.9.23 재설치 (AWS ec2 ssh 서버에서 확인한 파이썬 버전과 맞추기 이해 만듦)

(2) 프로젝트 폴더 (나중에 AWS에서 application이라고 해서 웹서버에 올릴 최상위 폴더 만들기

(3) 프로젝트 폴더에서 가상 파이썬 환경 실행하여 가상 파이썬 (예: venv)에서 작업할 것
   -> 이게 중요한데, 가상 파이썬 환경을 만들고 그 안에서 작업해야 나중에 dependencies (의존성) 에러에 걸리지 않음.
      dependencies (의존성)이란 프로젝트 폴더 내에서만 명령어가 상호작용, 곧 상호 의존해야 나중에 통째로 서버로 이 폴더를 올려도 문제가 없는데 가상 환경을 만들지 않으면 내 pc의 다른 폴더와 프로젝트 폴더 안의 파일들이 상호 연결, 의존하게 되어 웹서버에 옮기면 웹서버의 프로젝트 파일들이 내 pc의 다른 파일과 연결이 안 되어 에러가 나게 되는 것임.

(4) 가상 파이썬 (예: venv) 켜고 requirements.txt 파일을 아래처럼 작성하여 설치 (psycopg2 는 뭔가 문제가 있기 때문에 대안으로 psycopg2-binary 설치)
django==4.2.24
psycopg2-binary
boto3
django-storages
awsebcli

(5) 프로젝트 틀 작성 : django-admin startproject anonymous . (장고를 이용해 anonymous라는 프로젝트를 현재 폴더에 만든다는 뜻)

(6) 가상 파이썬 (예: venv) 켜고 코딩하여 로컬에서 잘 작동하는 것 확인하고 AWS에 upload 진행할 것


<<------------------------------------------------------------------------->>

장고 django AWS EB EC2 배포 안 되는 원인 추측

아. 이건 아니지. AWS 통해서 배포하는 것은 접는 것이 낫다는 결론. AWS가 정책을 바꾸면 어떻게 할 도리가 없음. 어쩐지 배포했다는 글들 보니까 대부분 2024년 이전 글들임. 몇 번 더 시도해보고 안 되면 구글이나 MS 알아보고 안 되면 PC IIS 알아봐야겠음.

2024년 10월 관련 글:
AWS계정을 새롭게 생성 후 간단한 테스트를 위해 Beanstalk 환경을 구성하는 과정에서 아래와 같은 에러가 발생했다. 에러로그는 아래와 같다. 
위 안내 문구는 Auto Scaling 그룹에서 더 이상 Launch Configuration 생성을 지원하지 않으므로 Launch Template을 사용하라는 메시지가 포함되어 있었다.
ERROR Creating Auto Scaling launch configuration failed Reason: Resource handler returned message: "The Launch Configuration creation operation is not available in your account. Use launch templates to create configuration templates for your Auto Scaling groups. 

https://billtech.tistory.com/23

1년 전 글
Creating an Elastic Beanstalk without success

Question:
Hello, I am new to using Elastic Beanstalk. I am trying to create an environment but i get these errors

Creating Auto Scaling launch configuration failed Reason: Resource handler returned message: "The Launch Configuration creation operation is not available in your account. Use launch templates to create configuration templates for your Auto Scaling groups.
Stack named 'awseb-e-dcjhm3nklm-stack' aborted operation. Current state: 'CREATE_FAILED' Reason: The following resource(s) failed to create: [AWSEBAutoScalingLaunchConfiguration].
Service:AmazonCloudFormation, Message:Resource AWSEBAutoScalingGroup does not exist for stack awseb-e-dcjhm3nklm-stack

Answers
I had the same issue and worked for me after trying for days was to:

 - DisableIMDSv1
 - Setting RootVolumeType to: gp3 I hope that helps

https://repost.aws/questions/QUyYai-CJ4SiuDJpdV15SO2w/creating-an-elastic-beanstalk-without-success
https://repost.aws/questions/QUcX9TipxqSGeM5G7RORmqoQ/new-account-recently-created-unable-to-create-environments-on-elastic-beanstalk-launch-configuration-error#ANY34Fe2VjTd6r8Ir2-gqJRw

<<------------------------------------------------------------------------->>

2025년에 배포했다는 유튜브 영상 찾았음.
초보자를 위한 Python, Amazon Elastic Beanstalk, AWS 및 Django 앱 배포

https://www.youtube.com/watch?v=2N-L7-MAeuc

<<------------------------------------------------------------------------->>

경로 path 관련 사항
: 윈도우 빼고 리눅스 유닉스 운영체제와 zip 파일, 파이썬, 장고는 경로 표시할 때 슬래시 (정방향 / forward slash)를 써야 함.
: django 장고에서는 url 끝에 슬래시를 자동으로 붙이기 때문에 url을 변수로 지정하고 폴더 경로를 붙일 때 폴더 경로 '/upload/'는 에러가 나고 'upload/'로 붙여야 함. 최근 버전의 정규화 기능이라고 하는데 왜 그렇게 했는지 모르겠음. 불과 2~3년 전에 만든 코딩에 에러가 나게 만드는 심보는 뭘까?

<<------------------------------------------------------------------------->>

1) VS code 터미널에서 eb ssh 명령어 입력하여 AWS EC2 ssh 접속해서 직접 설치하는데 크게 다음 세가지 버전, 패키지 문제가 발생한 듯함
   - AWS ec2 리눅스 2023 운영체제 허용 버전
     python : Python 3.9.23 버전. sudo yum install python3.11 -y 또는 sudo dnf install python3.11 -y 등을 활용해 3.11과 3.13 버전을 설치해도 안 바뀜
     django : django 5.2.5로 프로젝트 작업했는데 "ERROR: No matching distribution found for django==5.2.5" 이런 메시지가 뜸. 봤더니 AWS EC2에서 허용하는 django 최대 버전은 django 4.2.24

     로컬 pc에는 python 3.13.6 과 django 5.2.5 깔고 프로젝트 완수했는데, 아주 잘 돌아갔는데 AWS에서는 안 됨. google 등 다른 배포 클라우드를 알아보든가 파이썬, 장고 낮은 버전으로 다시 프로젝트 작업해야 함.

2) psycopg2 : 뭐냐 이건.
   Collecting psycopg2
  Downloading psycopg2-2.9.10.tar.gz (385 kB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... error
  error: subprocess-exited-with-error
  라이센스가 어쩌고 저쩌고 하는데 설치 안 됨. 대신 psycopg2-binary 설치하라고 함.
  아무래도 VScode 터미널창에서 eb init 했을 때 cp949 에러 발생한 게 얘랑 관련 있을까? cp949는 한글 UTF-8 또는 공백 4개 대신 탭을 쳐 넣어서 발생한 것이라고 하는데, binary 문제면 얘도 cp949 에러와 관련 있는 듯.

1)과 2) 고려해서 requirements.txt 파일 내용을 아래처럼 다시 작성하고 설치해야 할 듯.
django==4.2.24
psycopg2-binary
boto3
django-storages
awsebcli

3) AWS ec2 ssh에 직접 연결해서 작업할 때 또 무슨 문제가 있었느냐 하면 env.json 파일을 어떻게 올리느냐는 것임.
   AWS EC2 인스턴스에 파일 업로드 및 다운로드 (SCP 명령어) 이것 배워서 하든가, 직접 파일 만드는 방법 연구해야 함. 결국 리눅스 linux 파일 폴더 명령어 cat 찾아서 만들어는 보았음.
   (venv) [ec2-user@ip-000-00-00-000 django-anonymous]$ cat > env.json
   "env.json 내용 복사한 것 붙여넣고 Ctrol + D 키를 두 번 누르면 됨"

   물론 AWS EC2에서도 가상 환경 만들어서 진행해야 함. 코딩의 코도 모르고 초보자도 쉽게 웹사이트 만들어서 올릴 수 있다고 해서 수강했는데 버전도 안 맞고 안 되고 혼자 배우느라 겁나 어려웠음.

   리눅스 linux 파일 폴더 명령어 알아야 함. 근데 구글에는 대부분 ubuntu 위주로 설명이 나와서 참 어려웠음. 나중에 배포 잘 되고 에러 안 나면 전부 다 정리해서 초보자도 따라할 수 있도록 할 것임.

   아무튼 미친 척 하고 AWS ec2 ssh 창에서 명령어 실행했더니
   (venv) [ec2-user@ip-000-00-00-000 django-anonymous]$ python manage.py runserver 8000

   도메인으로 연결은 된 것 같은데 또 뭐냐?
   Welcome to nginx!
   If you see this page, the nginx web server is successfully installed and working. Further configuration is required.
   For online documentation and support please refer to nginx.org.
   Commercial support is available at nginx.com.
   Thank you for using nginx.

   와... 초보자한테 한 달도 안 되는 강의 들으면 장고 익명 게시판 웹사이트 만들어서 올릴 수 있다고 하더니 학원이 개념이 없는 듯.
   강의도 몇 년 전 내용인데 업데이트 해 주시고 호환 버전도 알려 주시고 했으면 좋았을 것을.

   저건 또 어떻게 하나... 난감하네요.

<<------------------------------------------------------------------------->>


※ 참고 참조 검색 문제 해결 키워드. 브라우저 닫기 전에 검색 제목만 복사해서 붙임.

<<------------------------------------------------------------------------->>

1. "git" 깃 깉 얘도 보기보다 어려웠음. 지금도 잘 모르겠음. VS code에서 로그아웃 어떻게 하는지도 모름.
Git 저장소의 경로는 현재 프로젝트 디렉토리 안의 .git 폴더에 있습니다. 이 .git 폴더는 Git의 모든 버전 관리 정보가 저장되는 곳입니다. git init으로 Git 저장소를 생성하면 현재 디렉토리에 .git 폴더가 생성되며, git clone으로 원격 저장소를 복제하면 해당 프로젝트 폴더에 .git 폴더가 생성됩니다. 

git remote -v
https://nemomemo.tistory.com/83#google_vignette

Git 핵심 명령어 모음
https://www.heropy.dev/p/PcUkdT

Git 로컬 저장소의 위치를 확인하려면 해당 디렉터리에서 git status 명령어를 실행하거나, .git 폴더가 있는지 확인하면 됩니다. git status를 실행하면 Git 저장소가 초기화되어 있는 경우, Git이 현재 디렉토리를 저장소로 인식하여 관련 정보를 보여줍니다. 또는 해당 디렉터리에서 숨김 폴더인 .git 폴더를 찾아볼 수 있으며, 이 폴더의 존재가 Git 로컬 저장소의 루트임을 나타냅니다. 

Github 입문기 (2) : 로컬 저장소의 새 폴더를 git에 옮기자
https://omil.tistory.com/16#c5

git repository 주소 확인

Git repository 주소는 로컬 터미널에서 git remote -v 명령어를 실행하거나, git remote show origin (여기서 origin은 리모트 저장소의 별칭) 명령어로 확인할 수 있습니다. 또는 웹사이트(예: GitHub)의 저장소 페이지에서 직접 복사할 수도 있습니다. 
Git repository가 있는 웹사이트(예: GitHub)로 이동합니다. 리포지토리의 기본 페이지에서 Clone 또는 유사한 버튼을 찾아 클릭합니다.

<<------------------------------------------------------------------------->>

2. AWS 버킷 정책을 삭제하려면 Amazon S3 콘솔에서 버킷의 '권한(Permissions)' 탭으로 이동한 후, '버킷 정책(Bucket Policy)' 섹션에서 '삭제(Delete)'를 선택하고, 확인 텍스트 필드에 'delete'를 입력하고 '삭제(Delete)' 버튼을 클릭하면 됩니다. 만약 정책 삭제가 안 된다면, 해당 버킷 정책에 명시적으로 s3:DeleteBucket을 거부하는 Deny 문이 있는지 확인하고, 있다면 해당 버킷 정책의 내용을 수정해야 합니다.

<<------------------------------------------------------------------------->>

3. django aws gunicorn 안 됨 : 근데 Gunicorn이 Nginx와 같은 거냐?
Django와 AWS 환경에서 Gunicorn이 작동하지 않는 경우, Gunicorn 설정 및 실행 확인, Nginx 설정 확인, 서버 로그 확인, 방화벽 설정 검토가 필요합니다. 각 단계를 따라 문제를 해결해야 하며, Gunicorn이 WSGI 서버로 올바르게 설정되었는지, Nginx와 통신이 가능한지, 그리고 EC2 인스턴스의 보안 그룹과 방화벽이 트래픽을 허용하는지 확인해야 합니다.

Gunicorn 실행: gunicorn --bind 0:8000 myproject.wsgi:application
Nginx 설정 파일 확인: Nginx 설정 파일(nginx.conf, sites-available 디렉토리의 conf 파일 등)이 Gunicorn 서버의 포트(예: 8000)와 올바르게 연결되어 있는지 확인합니다.
Nginx 설정 재시작: sudo systemctl restart nginx 
Nginx 문법 확인: sudo nginx -t 

Nginx 로그 확인: sudo tail -f /var/log/nginx/error.log
시스템 로그 확인: sudo journalctl -u gunicorn 또는 sudo journalctl -u nginx 
4단계: 방화벽(보안 그룹) 설정 검토
EC2 보안 그룹: AWS EC2 인스턴스의 보안 그룹 설정에서 HTTP(80), HTTPS(443) 포트 및 Gunicorn이 사용하는 포트(예: 8000)에 대한 인바운드 트래픽이 허용되어 있는지 확인합니다. 
이 단계를 통해 Django 앱이 정상적으로 배포되지 않는 근본적인 원인을 파악하고 문제를 해결할 수 있습니다.

<<------------------------------------------------------------------------->>

4. 리눅스 aws ssh python 설치
Amazon Linux: sudo yum -y install
python3, Ubuntu 등 Debian 계열: sudo apt-get install python3

버전 확인
python3 --version
pip3 --version

<<------------------------------------------------------------------------->>

5. aws ssh 로컬 폴더 파일 업로드
AWS에서 SSH를 사용 로컬 터미널

scp -i <키_파일_경로> -r <로컬_폴더_경로> <사용자명>@<EC2_퍼블릭_IP>:<서버_폴더_경로>

참조: AWS EC2 인스턴스에 파일 업로드 및 다운로드 (SCP 명령어)
https://rizdev.tistory.com/entry/AWS-EC2-인스턴스에-파일-업로드-및-다운로드-SCP-명령어

<<------------------------------------------------------------------------->>

6. aws ssh requirements.txt 설치
requirements.txt 파일이 있는 프로젝트 디렉토리로 이동
그 다음, 가상환경을 생성 및 활성화하고 pip install -r requirements.txt 명령어를 실행

설치가 되지않는 패키지는 뛰어넘고 설치 가능한 패키지만 모두 설치 시 (Linux와 CentOS에서만)
cat requirements.txt | xargs -n 1 pip install

참조: [Linux] requirements.txt 생성하기
https://aeong-dev.tistory.com/18

<<------------------------------------------------------------------------->>

7. aws ssh 프로젝트 디렉토리
AWS에서 SSH 프로젝트 디렉토리는 일반적으로 ~/.ssh 디렉토리 또는 사용자가 지정한 프로젝트 디렉토리에 위치합니다. SSH 키 페어 파일은 ~/.ssh에 저장하고, 소스 코드는 git clone 또는 다른 방법을 통해 /home/ubuntu/app 등 원하는 프로젝트 디렉토리에 복제하여 사용합니다.

<<------------------------------------------------------------------------->>

8. aws ssh git clone aws ec2 리눅스 github ssh key 만들기
AWS EC2 리눅스 인스턴스에서 GitHub SSH 키를 생성하려면, 먼저 인스턴스에 SSH로 접속한 뒤 ssh-keygen -t rsa -b 4096 -C "your_email@example.com" 명령을 사용하여 SSH 키 쌍을 생성합니다
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

<<------------------------------------------------------------------------->>

9. AWS EC2 cd 명령어를 사용하여 requirements.txt 파일이 위치한 프로젝트 디렉토리로 이동
sudo find / -name requirements.txt

<<------------------------------------------------------------------------->>

10. AWS EC2 에 Django 기반의 웹 서버 만들기  Gunicorn 설정 NGINX 설정
참조: https://space-cho.tistory.com/21

<<------------------------------------------------------------------------->>

11. 리눅스 파일 폴더 명령어
참조: https://inpa.tistory.com/entry/LINUX-📚-디렉토리-명령어-💯-정리

<<------------------------------------------------------------------------->>

12. aws 리눅스 ec2 ssh pip 설치
pip 설치 (Amazon Linux/RHEL 계열)
sudo yum update
sudo yum install python3-pip -y

또는 ( AWS linux 2023 버전 )
sudo dnf update
sudo dnf install python3-pip -y

<<------------------------------------------------------------------------->>

13. aws ec2 파이썬 최신 버전 설치
아마존 리눅스(Amazon Linux  AL2): sudo yum install
아마존 리눅스(Amazon Linux  AL3): sudo dnf install

sudo yum update 또는 sudo dnf update (AL2023의 경우)
sudo yum install python3.11 -y 또는 sudo dnf install python3.11 -y

-> 확인해보면 3.9 버전임. AWS ec2에서 일부러 그렇게 설정한 듯함

<<------------------------------------------------------------------------->>

14. aws ec2 리눅스 ssh 가상 폴더 venv 설치
Amazon Linux 계열: sudo yum update 후 sudo yum install python3 python3-venv
파이썬 가상환경을 생성할 프로젝트 디렉토리로 이동: python3 -m venv <가상환경이름> ( 예: python3 -m venv venv )
가상환경 활성화 - 프로젝트 폴더로 이동.: source <가상환경이름>/bin/activate ( 예: source venv/bin/activate )

<<------------------------------------------------------------------------->>

15. aws ec2 리눅스 ssh 환경에서 requirements.txt 편집 env.json 만들기
참조: 리눅스 파일 편집 cat, vi
https://yuchae.tistory.com/443

cat > requirements.txt
django==4.2.24
psycopg2-binary
boto3
django-storages
awsebcli
"여기서 Ctrl + D 두 번 누름"

보기( ">" 를 빼고 입력함) : 
cat requirements.txt

cat > env.json
"내용 입력함. 그리고 Ctrl + D 두 번 누름"
보기( ">" 를 빼고 입력함) : 
cat env.json

<<------------------------------------------------------------------------->>





     
     

장고 django AWS EB EC2 배포 안 되는 원인 추측

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
   


     
     

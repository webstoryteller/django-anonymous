from django.db import models
# Create your models here.
from user.models import User

class Post(models.Model): # 게시글 형식 지정
    # post_id = models.AutoField(primary_key=True) # post_id와 같은 맞춤 값으로 만들 수도 있음. 그렇지 않으면 장고가 id란 값으로 primary key를 자동으로 함
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user가 탈퇴하면 user의 글도 삭제. User ID를 자동으로 잡음. user_id=1
    title = models.CharField(max_length=100) # 게시글 제목 글자 수 100자 제한
    content = models.TextField() # content 필드를 추가했습니다.
    reg_date = models.DateTimeField(auto_now_add=True)
    img_url = models.URLField(null=True)

    class Meta:
        db_table = "post" # 만약 post라고 이름을 정의하지 않으면, 자동으로 board_post라고 됨 (즉 app이름_model이름)


# FK -> Parents.children_set
# post.comment_set

class Comment(models.Model): # 댓글, 덧글 달기
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # post ID를 자동으로 잡음. post_id=1
    content= models.TextField()
    reg_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comment"

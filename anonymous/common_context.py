from django.conf import settings

def img_url_context(request):
    # return {"IMG_URL":settings.S3_ROOT_URL}
    return {"IMG_URL":f"{settings.S3_ROOT_URL}/"} # 장고 django 5.2.5에서는 / 를 주의해서 붙여야 함. ----.com/upload/----.png

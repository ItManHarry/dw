import os
def handle_uploaded_file(file=None):
    if file:
        # 文件上传路径
        upload_path = os.path.join(os.path.abspath('.'), 'attachments/files')
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        file_to_upload = os.path.join(upload_path, file.name)
        # 执行上传
        with open(file_to_upload, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    else:
        print('No file to upload ...')
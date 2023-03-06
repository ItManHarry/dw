def handle_uploaded_file(f=None):
    if f is not None:
        print('Upload a file ...')
        with open('upload.txt', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    else:
        print('No file to upload ...')

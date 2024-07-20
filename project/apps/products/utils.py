def validate_img_extension(file):
    try:
        ext = file.name.split('.')[-1]
        valid_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif', 'svg', 'jfif', 'pjpeg', 'pjp', 'apng', 'avif']
        if ext.lower() in valid_extensions:
            return True
        else:
            return False
        
    except Exception:
        pass

    
def validate_video_extension(file):
    try:
        ext = file.name.split('.')[-1]
        valid_extensions = ['mp4', 'mov', 'avi', 'mkv', 'webm', 'flv', 'wmv', 'ogg', 'qt', 'mts', 'm2ts', 'm4v', 'mpeg', 'mpg', 'm4v', '3gp', '3g2']
        if ext.lower() in valid_extensions:
            return True
        else:
            return False
    except Exception:
        pass

import os
import moviepy.editor as mp
from PIL import Image


class FileAnalysis:
    def __init__(self, file_path):
        self.file_path = file_path

    def details(self):
        file_name = os.path.basename(self.file_path)
        return os.path.splitext(file_name)

    def convert_to_mp4(self, new_path=None):
        valid_file = ['.gif', '.avi']
        old_path = self.file_path
        current_dir = os.getcwd()
        source_path = self.file_path if new_path is None else new_path
        self.file_path = source_path
        _, ext = self.details()
        self.file_path = old_path
        if not source_path:
            return False
        if ext not in valid_file:
            return False
        dest_path = current_dir+"/converted"
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)

        try:
            clip = mp.VideoFileClip(source_path)
            clip.write_videofile(dest_path+"/output.mp4")
            clip.close()
            return True
        except:
            return False

    def convert_to_jpg(self):
        try:
            img = Image.open(self.file_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save("converted/image.jpg")
            return True
        except:
            return False

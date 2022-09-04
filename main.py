from fileanalysis import FileAnalysis
from imageanalysis import ImageAnalyze

from tkinter import filedialog


input("Press any key to choose your file for analyze: ")
file_path = filedialog.askopenfilename(filetypes=[(
    "Image files", "*.jpg *.jpeg *.png"), ("GIF files", "*.gif")])

file = FileAnalysis(file_path)


_, ext = file.details()
analyze = ImageAnalyze(file_path)

if ext in [".jpg", ".jpeg", ".png"]:
    pic_object = analyze.findobject()
    analyze.imagetype = pic_object["object"]
    if analyze.imagetype != "person":
        print("Your image file does not contain person to detect emotions.")
        analyze.showbbox(pic_object) if pic_object["object"] != "Not found" else print(
            "there's no information to find the object")
    else:
        img_analyze = ImageAnalyze(file_path)
        result = img_analyze.detectemotions(show=True)
        if (result == None or len(result) == 0):
            print(
                "Your image is vague and it can not be analyzed.")
        else:
            print(
                "Your image has been analyzed.\nThe result is in the output folder which name is emotion.jpg")

elif ext == ".gif":
    # check the gif file contain person for analyzing emotion
    file.file_path = file_path
    is_convert = file.convert_to_jpg()
    new_file_path = "converted/image.jpg" if is_convert else None
    if new_file_path != None:
        analyze.img_path = new_file_path
        pic_object = analyze.findobject()
        analyze.imagetype = pic_object["object"]
        if analyze.imagetype != "person":
            print("Your gif does not contain person to detect emotions.")
            analyze.showbbox(pic_object) if pic_object["object"] != "Not found" else print(
                "there's no information to find the object")
        else:
            is_convert = file.convert_to_mp4(file_path)
            if is_convert:
                new_file_path = "converted/output.mp4"
                analyze.img_path = new_file_path
                analyze.gifemotiondetect()
                print(
                    "Your image has been analyzed.\nThe result is in the output folder which name is emotion.jpg")
            else:
                print(
                    "Your image is vague and it can not be analyzed.")
    else:
        print("There was an error to convert your *.gif file.")

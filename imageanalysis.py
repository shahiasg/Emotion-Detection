import os
import cv2
from fer import FER
from fer import Video
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class ImageAnalyze:
    imagetype = "person"

    def __init__(self, img):
        self.img = cv2.imread(img)
        self.img_path = img

    def findobject(self, new_path=None):
        current_dir = os.getcwd()
        source_path = self.img_path if new_path is None else new_path
        img = cv2.imread(source_path)
        classNames = []
        classFile = current_dir+'/resource/object.names'
        with open(classFile, 'rt') as f:
            classNames = f.read().rstrip('\n').split('\n')

        config_path = current_dir+'/resource/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weights_path = current_dir+'/resource/frozen_inference_graph.pb'

        net = cv2.dnn_DetectionModel(weights_path, config_path)
        net.setInputSize(320, 320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)
        classIds, confs, bbox = net.detect(
            img, confThreshold=0.45)
        return {
            "image": img,
            "object": classNames[classIds[0]-1] if len(classIds) > 0 else "Not found",
            "confidence": confs[0] if len(classIds) > 0 else 0,
            "boundingbox": bbox[0] if len(classIds) > 0 else 0
        }

    def detectemotions(self, show=False):
        if self.imagetype == "person":
            emotion_detector = FER(mtcnn=True)
            # Save output in result variable
            result = emotion_detector.detect_emotions(self.img)
            image_emotions = []
            if len(result) > 0:
                bounding_box = result[0]["box"]
                emotions = result[0]["emotions"]
                cv2.rectangle(self.img,
                              (bounding_box[0], bounding_box[1]),
                              (bounding_box[0] + bounding_box[2],
                               bounding_box[1] + bounding_box[3]),
                              (0, 155, 255), 2,)
                emotion_name, score = emotion_detector.top_emotion(self.img)

                for index, (emotion_name, score) in enumerate(emotions.items()):
                    color = (211, 211, 211) if score < 0.01 else (255, 0, 0)
                    emotion_score = "{}: {}".format(
                        emotion_name, "{:.2f}".format(score))
                    image_emotions.append(
                        {"emotion": emotion_name, "score": score})
                    cv2.putText(self.img, emotion_score,
                                (bounding_box[0], bounding_box[1] +
                                 bounding_box[3] + 30 + index * 15),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA,)
                if show:
                    # Save the result in new image file
                    cv2.imwrite("output/emotion.jpg", self.img)
                    # Read image file using matplotlib's image module
                    result_image = mpimg.imread('output/emotion.jpg')
                    plt.imshow(result_image)
                    dominant = self.dominantemotion(result[0]["emotions"])
                    plt.xlabel("Dominant emotion is {}: %{}".format(dominant["emotion"],
                                                                    "{:.2f}".format(dominant["score"]*100)))
                    plt.show()
                return image_emotions
        else:
            return []

    def dominantemotion(self, emotions):
        emotion_name = list(emotions.keys())
        emotion_score = list(emotions.values())
        # find max of emotion
        intence_emotion = max(emotion_score)
        return {
            "emotion": emotion_name[emotion_score.index(intence_emotion)],
            "score": intence_emotion
        }

    def showbbox(self, detectobj):
        cv2.rectangle(detectobj["image"], detectobj["boundingbox"],
                      color=(0, 255, 0), thickness=2)
        # Save the result in new image file
        cv2.imwrite("output/detect.jpg", detectobj["image"])

        # Read image file using matplotlib's image module
        result_image = mpimg.imread('output/detect.jpg')
        plt.imshow(result_image)
        plt.xlabel(
            "Your object in the image is: {} and the confidece for it is: %{}"
            .format(detectobj["object"],
                    "{:.2f}".format(detectobj["confidence"]*100)))
        plt.show()

    def gifemotiondetect(self):

        # Build the Face detection detector
        face_detector = FER(mtcnn=True)
        # Input the video for processing
        input_video = Video(self.img_path)

        # The Analyze() function will run analysis on every frame of the input video.
        # It will create a rectangular box around every image and show the emotion values next to that.
        # Finally, the method will publish a new video that will have a box around the face of the human with live emotion values.
        processing_data = input_video.analyze(face_detector, display=False)

        # We will now convert the analysed information into a dataframe.
        # This will help us import the data as a .CSV file to perform analysis over it later
        vid_df = input_video.to_pandas(processing_data)
        vid_df = input_video.get_first_face(vid_df)
        vid_df = input_video.get_emotions(vid_df)

        # Plotting the emotions against time in the video
        pltfig = vid_df.plot(figsize=(20, 8), fontsize=16).get_figure()

        # We will now work on the dataframe to extract which emotion was prominent in the video
        angry = sum(vid_df.angry)
        disgust = sum(vid_df.disgust)
        fear = sum(vid_df.fear)
        happy = sum(vid_df.happy)
        sad = sum(vid_df.sad)
        surprise = sum(vid_df.surprise)
        neutral = sum(vid_df.neutral)

        emotions = ['Angry', 'Disgust', 'Fear',
                    'Happy', 'Sad', 'Surprise', 'Neutral']
        emotions_values = [angry, disgust, fear, happy, sad, surprise, neutral]

        score_comparisons = pd.DataFrame(emotions, columns=['Human Emotions'])
        score_comparisons['Emotion Value from the Video'] = emotions_values
        score_comparisons

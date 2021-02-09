import cv2
import math



class GenderDetectV2:

    def highlightFace(self, net, frame, conf_threshold=0.7):
        frameOpencvDnn = frame.copy()
        frameHeight = frameOpencvDnn.shape[0]
        frameWidth = frameOpencvDnn.shape[1]
        blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

        net.setInput(blob)
        detections = net.forward()
        faceBoxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                faceBoxes.append([x1, y1, x2, y2])
                cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
        return frameOpencvDnn, faceBoxes


    def detect_gender(self, image_file):
        padding = 20
        # image_file = cv2.imread(image_file)

        face_proto = "./Assets/GenderModels/opencv_face_detector.pbtxt"
        face_model = "./Assets/GenderModels/opencv_face_detector_uint8.pb"

        gender_proto = "./Assets/GenderModels/gender_deploy.prototxt"
        gender_model = "./Assets/GenderModels/gender_net.caffemodel"

        MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
        gender_list = ['Male', 'Female']

        face_net = cv2.dnn.readNet(face_model, face_proto)
        # ageNet = cv2.dnn.readNet(ageModel, ageProto)
        gender_net = cv2.dnn.readNet(gender_model, gender_proto)

        resultImg, faceBoxes = self.highlightFace(face_net, image_file)
        if not faceBoxes:
            print("No face detected")



        blob = cv2.dnn.blobFromImage(image_file, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        gender_net.setInput(blob)
        genderPreds = gender_net.forward()
        gender = gender_list[genderPreds[0].argmax()]
        print(f'Gender: {gender}')

        return gender, genderPreds[0]

        # ageNet.setInput(blob)
        # agePreds = ageNet.forward()
        # age = ageList[agePreds[0].argmax()]
        # print(f'Age: {age[1:-1]} years')
        #
        # cv2.putText(resultImg, f'{gender}, {age}', (faceBox[0], faceBox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
        #             (0, 255, 255), 2, cv2.LINE_AA)
        # cv2.imshow("Detecting age and gender", resultImg)
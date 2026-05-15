import os
import cv2
import numpy as np
import onnxruntime as ort

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "cat_dog_model.onnx"
)


class CatDogClassifier:

    def __init__(self):

        try:
            self.session = ort.InferenceSession(MODEL_PATH)

            self.input_name = self.session.get_inputs()[0].name

        except Exception as e:
            raise Exception(
                f"Ошибка загрузки модели: {e}"
            )

    def preprocess(self, image_path):

        try:
            image = cv2.imread(image_path)

            if image is None:
                raise Exception("Не удалось загрузить изображение")

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            image = cv2.resize(image, (224, 224))

            image = image.astype(np.float32) / 255.0

            image = np.transpose(image, (2, 0, 1))

            image = np.expand_dims(image, axis=0)

            return image

        except Exception as e:
            raise Exception(
                f"Ошибка обработки изображения: {e}"
            )

    def predict(self, image_path):

        try:
            image = self.preprocess(image_path)

            outputs = self.session.run(
                None,
                {self.input_name: image}
            )

            prediction = float(outputs[0][0][0])

            if prediction >= 0.5:
                result_class = "dog"
                confidence = prediction
            else:
                result_class = "cat"
                confidence = 1 - prediction

            return {
                "class": result_class,
                "confidence": round(confidence * 100, 2)
            }

        except Exception as e:
            raise Exception(
                f"Ошибка модели: {e}"
            )
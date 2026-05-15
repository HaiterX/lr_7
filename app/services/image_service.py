import os

SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png"]


class ImageValidator:

    @staticmethod
    def validate_image(path):

        if not path:
            raise Exception("Файл не выбран")

        if not os.path.exists(path):
            raise Exception("Файл не существует")

        extension = os.path.splitext(path)[1].lower()

        if extension not in SUPPORTED_FORMATS:
            raise Exception(
                "Поддерживаются только JPG и PNG"
            )

        return True
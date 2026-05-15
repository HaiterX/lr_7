import os
import flet as ft

from model.classifier import CatDogClassifier
from services.image_service import ImageValidator
from ui.components import ResultCard


classifier = CatDogClassifier()

class CatDogApp:

    def __init__(self, page: ft.Page):
        self.page = page

        self.selected_image_path = None

        self.setup_page()
        self.create_components()
        self.build_layout()

    def setup_page(self):
        self.page.title = "Cat vs Dog Classifier"
        self.page.window_width = 900
        self.page.window_height = 700
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.scroll = ft.ScrollMode.AUTO

    def create_components(self):

        self.title = ft.Text(
            value="Классификация изображений",
            size=30,
            weight=ft.FontWeight.BOLD
        )

        self.image_view = ft.Image(
            width=350,
            height=350,
            fit=ft.ImageFit.CONTAIN,
            border_radius=15,
            visible=False
        )

        self.result_card = ResultCard()

        self.status_text = ft.Text(
            value="",
            color=ft.Colors.RED,
            size=16
        )

        self.pick_files_dialog = ft.FilePicker(
            on_result=self.on_file_selected
        )

        self.page.overlay.append(self.pick_files_dialog)

        self.upload_button = ft.ElevatedButton(
            text="Выбрать изображение",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=self.pick_image
        )

        self.predict_button = ft.ElevatedButton(
            text="Классифицировать",
            icon=ft.Icons.ANALYTICS,
            on_click=self.predict_image
        )

    def build_layout(self):

        self.page.add(
            ft.Column(
                controls=[
                    self.title,
                    ft.Row(
                        controls=[
                            self.upload_button,
                            self.predict_button
                        ],
                        spacing=20
                    ),
                    self.image_view,
                    self.result_card,
                    self.status_text
                ],
                spacing=25,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def pick_image(self, e):

        self.pick_files_dialog.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"]
        )

    def on_file_selected(self, e: ft.FilePickerResultEvent):

        try:
            self.status_text.value = ""

            if not e.files:
                self.status_text.value = "Файл не выбран"
                self.page.update()
                return

            file_path = e.files[0].path

            ImageValidator.validate_image(file_path)

            self.selected_image_path = file_path

            self.image_view.src = file_path
            self.image_view.visible = True

            self.page.update()

        except Exception as error:
            self.show_error(str(error))

    def predict_image(self, e):

        try:
            self.status_text.value = ""

            if not self.selected_image_path:
                raise Exception(
                    "Сначала выберите изображение"
                )

            result = classifier.predict(
                self.selected_image_path
            )

            self.result_card.update_result(
                result["class"],
                result["confidence"]
            )

            self.page.update()

        except Exception as error:
            self.show_error(str(error))

    def show_error(self, message):

        self.status_text.value = f"Ошибка: {message}"

        snack = ft.SnackBar(
            content=ft.Text(f"Ошибка: {message}"),
            bgcolor=ft.Colors.RED
        )

        self.page.open(snack)
        self.page.update()



def main(page: ft.Page):
    CatDogApp(page)


ft.app(target=main)
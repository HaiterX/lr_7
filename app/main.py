import os
import sys
from pathlib import Path

import flet as ft

# Добавляем корень проекта для корректных импортов
sys.path.append(str(Path(__file__).parent.parent))

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
        self.page.window_width = 920
        self.page.window_height = 720
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 30
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def create_components(self):
        # Заголовок
        self.title = ft.Text(
            value="Классификация Кот / Собака",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_GREY_900
        )

        # Изображение
        self.image_view = ft.Image(
            src="",
            width=380,
            height=380,
            fit=ft.BoxFit.CONTAIN,
            border_radius=20,
            visible=False
        )

        self.result_card = ResultCard()
        
        self.status_text = ft.Text(
            value="",
            color=ft.Colors.RED_700,
            size=16,
            text_align=ft.TextAlign.CENTER
        )

        # === FilePicker (обновлено под Flet 0.85) ===
        self.pick_files_dialog = ft.FilePicker()
        self.page.overlay.append(self.pick_files_dialog)

        # Кнопки
        self.upload_button = ft.Button(
            content=ft.Text("Выбрать изображение"),   # ← content вместо text
            icon=ft.Icons.UPLOAD_FILE,
            on_click=self.pick_image,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12)
            )
        )

        self.predict_button = ft.Button(
            content=ft.Text("Классифицировать"),      # ← content вместо text
            icon=ft.Icons.ANALYTICS,
            on_click=self.predict_image,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12)
            )
        )

    def build_layout(self):
        self.page.add(
            ft.Column(
                controls=[
                    self.title,
                    ft.Row(
                        controls=[self.upload_button, self.predict_button],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Container(
                        content=self.image_view,
                        padding=20,
                        border=ft.Border.all(2, ft.Colors.BLUE_GREY_200),   # ← исправлено
                        border_radius=24,
                        bgcolor=ft.Colors.WHITE
                    ),
                    self.result_card,
                    self.status_text
                ],
                spacing=30,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def pick_image(self, e):
        """Открывает диалог выбора файла"""
        self.pick_files_dialog.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"]
        )

    async def on_file_selected(self, e: ft.FilePickerResultEvent):
        """Обработка выбранного файла (async!)"""
        try:
            self.status_text.value = ""
            self.result_card.clear()

            if not e.files:
                return  # пользователь отменил выбор

            file_path = e.files[0].path

            ImageValidator.validate_image(file_path)

            self.selected_image_path = file_path

            # Обновляем изображение
            self.image_view.src = file_path
            self.image_view.visible = True

            self.page.update()

        except Exception as error:
            self.show_error(str(error))

    def on_file_selected(self, e: ft.FilePickerResultEvent):
        try:
            self.status_text.value = ""
            self.result_card.clear()

            if not e.files:
                raise Exception("Файл не выбран")

            file_path = e.files[0].path

            ImageValidator.validate_image(file_path)

            self.selected_image_path = file_path

            # Обновляем изображение
            self.image_view.src = file_path
            self.image_view.visible = True

            self.page.update()

        except Exception as error:
            self.show_error(str(error))

    def predict_image(self, e):
        # ... (оставляем как было)
        try:
            self.status_text.value = ""

            if not self.selected_image_path:
                raise Exception("Сначала выберите изображение!")

            result = classifier.predict(self.selected_image_path)

            self.result_card.update_result(
                result["class"],
                result["confidence"]
            )
            self.page.update()

        except Exception as error:
            self.show_error(str(error))

    def show_error(self, message: str):
        self.status_text.value = f"Ошибка: {message}"
        
        snack = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED_700,
            action="OK"
        )
        self.page.open(snack)
        self.page.update()


def main(page: ft.Page):
    CatDogApp(page)

async def main(page: ft.Page):
    app = CatDogApp(page)
    # Подключаем обработчик после создания приложения
    app.pick_files_dialog.on_result = app.on_file_selected


ft.app(target=main)
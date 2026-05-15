import flet as ft


class ResultCard(ft.Container):

    def __init__(self):
        super().__init__()

        self.class_text = ft.Text(
            value="Класс: -",
            size=22,
            weight=ft.FontWeight.BOLD
        )

        self.confidence_text = ft.Text(
            value="Вероятность: -",
            size=18
        )

        self.content = ft.Column(
            controls=[
                self.class_text,
                self.confidence_text
            ],
            spacing=10
        )

        self.padding = 20
        self.border_radius = 15
        self.bgcolor = ft.Colors.BLUE_GREY_50

    def update_result(self, result_class, confidence):
        self.class_text.value = f"Класс: {result_class}"
        self.confidence_text.value = (
            f"Вероятность: {confidence}%"
        )
import pyautogui
import cv2
import numpy as np
import time


class ScreenAnalyzerBot:
    def __init__(self):
        self.templates = {}  # Словарь для хранения шаблонов предметов

    def add_template(self, name, template_path):
        """Добавляет шаблон предмета для поиска"""
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is not None:
            self.templates[name] = template
            print(f"Шаблон '{name}' успешно добавлен")
        else:
            print(f"Ошибка загрузки шаблона из {template_path}")

    def capture_screen(self):
        """Захватывает текущее изображение экрана"""
        screenshot = pyautogui.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    def find_template(self, template_name, threshold=0.8):
        """Ищет указанный шаблон на экране"""
        if template_name not in self.templates:
            print(f"Шаблон '{template_name}' не найден")
            return None

        screen = self.capture_screen()
        template = self.templates[template_name]

        # Поиск шаблона на экране
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Если совпадение достаточно хорошее
        if max_val >= threshold:
            # Получаем координаты центра найденного предмета
            h, w = template.shape[:-1]
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y, max_val)

        return None

    def find_all_templates(self, threshold=0.8):
        """Ищет все добавленные шаблоны на экране"""
        results = {}
        screen = self.capture_screen()

        for name, template in self.templates.items():
            result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                h, w = template.shape[:-1]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                results[name] = (center_x, center_y, max_val)

        return results

    def continuous_search(self, template_name, interval=1, threshold=0.8):
        """Непрерывный поиск предмета с заданным интервалом"""
        print(f"Начинаем поиск предмета '{template_name}'...")
        while True:
            result = self.find_template(template_name, threshold)
            if result:
                x, y, confidence = result
                print(f"Найден '{template_name}' в позиции ({x}, {y}) с уверенностью {confidence:.2f}")
            else:
                print(f"Предмет '{template_name}' не найден")
            time.sleep(interval)


# Пример использования
if __name__ == "__main__":
    bot = ScreenAnalyzerBot()

    # Добавляем шаблоны предметов для поиска
    bot.add_template("sword", "sword_template.png")
    bot.add_template("shield", "shield_template.png")
    bot.add_template("potion", "potion_template.png")

    # Поиск одного предмета
    sword_position = bot.find_template("sword")
    if sword_position:
        print(f"Меч найден в позиции: {sword_position[:2]}")

    # Поиск всех предметов
    all_items = bot.find_all_templates()
    print("Найденные предметы:", all_items)

    # Непрерывный поиск (раскомментируйте для использования)
    # bot.continuous_search("potion", interval=2)
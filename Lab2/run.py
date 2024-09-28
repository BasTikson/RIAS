from main import SecurityIncidentAnalyzer


from main import SecurityIncidentAnalyzer

def main():
    print("Оценка относительных частот возникновения угроз ИБ.")

    while True:
        choice = input("\nВведите вариант (от 1 до 35): ")
        try:
            variant = int(choice)
            if not (1 <= variant <= 35):
                raise ValueError("Вариант должен быть от 1 до 35.")
            break
        except ValueError as e:
            print("\n")
            print("Неправильный формат ввода данных. Попробуйте еще раз!")
            print(e)

    while True:
        count_element_group = input("\nВведите количество групп (не более 10): ")
        try:
            count_element_group = int(count_element_group)
            if not (1 <= count_element_group <= 10):
                raise ValueError("Количество элементов в группе должно быть от 1 до 10.")
            break
        except ValueError as e:
            print("\n")
            print("Неправильный формат ввода данных для количества групп. Попробуйте еще раз!")
            print(e)

    sec_anal = SecurityIncidentAnalyzer(variant, count_element_group)
    sec_anal.run()

if __name__ == "__main__":
    main()
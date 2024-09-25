from main import SecurityIncidentAnalyzer
def main():
    print("Оценка относительных частот возникновения угроз ИБ.")
    choice = input("\nВведите вариант: ")
    try:
        variant = int(choice)
        if 1 <= variant <= 35:
            sec_anal = SecurityIncidentAnalyzer(variant)
            sec_anal.run()
        else:
            print("\n")
            print("Выбран несуществующий вариант, выберите от 1 до 35!")
            main()
    except ValueError as e:
        print("\n")
        print("Неправильный формат ввода данных. Попробуйте еще раз!")
        print(e)
        main()
    except Exception as e:
        print("\n")
        print("Произошла непредвиденная ошибка!",)
        print(e)


if __name__ == "__main__":
    main()
import csv


def is_valid_number(value):
    try:
        number = float(value)
        return number >= 1
    except ValueError:
        return False


def kof_to_csv_period(kof_file, csv_file):
    with open(kof_file, mode='r', encoding='utf-8') as kof:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as csvf:
            writer = csv.writer(csvf, delimiter=';')

            for line in kof:

                stripped_line = line.strip()
                if not stripped_line:
                    continue

                numbers = stripped_line.split()

                if len(numbers) > 3 and not is_valid_number(numbers[-1]):
                    numbers.pop()

                name = numbers[1]
                x = numbers[-3]
                y = numbers[-2]
                z = numbers[-1]

                writer.writerow(
                    [name, x, y, z])


def kof_to_csv_comma(kof_file, csv_file):
    with open(kof_file, mode='r', encoding='utf-8') as kof:
        with open(csv_file, mode='w', newline='', encoding='utf-8') as csvf:
            writer = csv.writer(csvf, delimiter=';')

            for line in kof:
                stripped_line = line.strip()
                if not stripped_line:
                    continue

                numbers = stripped_line.split()

                if len(numbers) > 3 and not is_valid_number(numbers[-1]):
                    numbers.pop()

                name = numbers[1]
                x = numbers[-3].replace('.', ',')
                y = numbers[-2].replace('.', ',')
                z = numbers[-1].replace('.', ',')

                writer.writerow(
                    [name, x, y, z])

from flask import Flask, request, json
import collections
import csv
import numpy as np
from random import randint
import matplotlib.pyplot as plt

app = Flask(__name__)

# Frequencies of Digits
LEADING_DIGITS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
EXPECTED_DISTRIBUTIONS = [.301, .176, .125, .097, .079, .067, .058, .051, .046]


def read_file(fileName, columnName):
    # read in the file values
    f = open('census_2009b', 'r')

    try:
        reader = csv.DictReader(f, delimiter="\t")
        num_cols = len(reader.fieldnames)
        print(f"Num columns is {num_cols}")
        nums_from_column = []
        for row in reader:
            if len(row) != num_cols:
                continue
            nums_from_column.append(str(row['7_2009']))
    finally:
        f.close()
    return nums_from_column


def calculate_observed_frequencies(nums_from_column):
    # calculate actual frequencies
    first_digits = list(map(lambda n: str(n)[0], nums_from_column))
    first_digit_frequencies = collections.Counter(first_digits)
    first_digit_frequencies_percent = []
    for n in range(1, 10):
        data_frequency = first_digit_frequencies[str(n)]
        data_frequency_percent = data_frequency / len(nums_from_column)
        first_digit_frequencies_percent.append(data_frequency_percent)

    return first_digit_frequencies_percent


def create_graph(observed_distributions):
    # Benford's Law Distributions

    X_axis = np.arange(len(LEADING_DIGITS))

    # plotting a bar chart
    plt.bar(X_axis - 0.2, EXPECTED_DISTRIBUTIONS, 0.4, label='Expected')
    plt.bar(X_axis + 0.2, observed_distributions, 0.4, label='Observed')

    # naming the x-axis
    plt.xticks(X_axis, LEADING_DIGITS)
    plt.xlabel('Leading Digit')
    # naming the y-axis
    plt.ylabel('Distribution')


    num1 = randint(0, 1000)
    fileName = 'graph' + str(num1) + '.png'
    plt.savefig(fileName)
    # function to show the plot
    plt.show()
    return fileName


def decide_if_following_benfords(first_digit_frequencies_percent, acceptableRange):
    # We made our own rule to decide if the distribution follows Benford's Law
    # in this function, we will decide if the benford's law is off by checking if any of the 2-9 is within 10% of the
    # ferquency of numbers starting with a 1.
    frequency_at_1 = first_digit_frequencies_percent[0]
    frequency_at_1_high = first_digit_frequencies_percent[0] + first_digit_frequencies_percent[1] * acceptableRange
    frequency_at_1_low = first_digit_frequencies_percent[0] - first_digit_frequencies_percent[1] * acceptableRange
    for n in range(1, 9):
        frequency_at_n = first_digit_frequencies_percent[n]
        if frequency_at_n >= frequency_at_1_low and frequency_at_n <= frequency_at_1_high:
            return False
    return True


@app.route('/')
def hello_world():
    fileName = request.json.get('fileName')
    columnName = request.json.get('columnName')
    nums = read_file(fileName, columnName)
    first_digit_frequencies_percent = calculate_observed_frequencies(nums)
    fileName = create_graph(first_digit_frequencies_percent)
    print(EXPECTED_DISTRIBUTIONS, first_digit_frequencies_percent)
    followsBenford = decide_if_following_benfords(first_digit_frequencies_percent, 0.10)
    return json.jsonify(saveTo=fileName, followsBenfords=followsBenford)


if __name__ == '__main__':
    app.run()

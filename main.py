def read_file(file):
    data = []
    with open(file) as f:
        for line in f:
            parts = line.strip().split(',')
            line = [float(x) for x in parts[:-1]]
            line.append(parts[-1])
            data.append(line)
    return data


def calculate_num_attributes(data):
    attributes = data[0][:-1]
    num_attributes = len(attributes)
    return num_attributes


def check_num_attributes(data1, data2):
    num_attributes1 = calculate_num_attributes(data1)
    num_attributes2 = calculate_num_attributes(data2)
    if num_attributes1 != num_attributes2:
        return False
    return True


def euclidean_distance(list1, list2):
    distance = 0
    for i in range(len(list2) - 1):
        distance += (list1[i] - list2[i]) ** 2
    return distance


def determine_majority_label(k_nearest_labels):
    label_counts = {}

    for label in k_nearest_labels:
        if label in label_counts:
            label_counts[label] += 1
        else:
            label_counts[label] = 1

    max_count = 0
    majority_class = None
    for label, count in label_counts.items():
        if count > max_count:
            max_count = count
            majority_class = label
    return majority_class


def knn(train_data, test_data, k_num):
    output = []

    for point in test_data:
        distances = [euclidean_distance(point[0:-1], train_point[0:-1]) for _, train_point in enumerate(train_data)]

        distances_with_indices = list(zip(distances, range(len(distances))))
        distances_with_indices.sort()
        k_nearest_indices = [index for _, index in distances_with_indices[:k_num]]
        k_nearest_labels = [train_data[i][-1] for i in k_nearest_indices]

        label = determine_majority_label(k_nearest_labels)

        output.append(label)

    return output


def knn_for_new_observation(train_data, test_data, k_num):
    distances = [euclidean_distance(test_data[0:], train_point[0:-1]) for _, train_point in enumerate(train_data)]

    distances_with_indices = list(zip(distances, range(len(distances))))
    distances_with_indices.sort()
    k_nearest_indices = [index for _, index in distances_with_indices[:k_num]]
    k_nearest_labels = [train_data[i][-1] for i in k_nearest_indices]

    label = determine_majority_label(k_nearest_labels)

    return label


def option1(train, test, k_num):
    train_data = read_file(train)
    test_data = read_file(test)

    if check_num_attributes(train_data, test_data):
        data = knn(train_data, test_data, k_num)
        for x in range(len(data)):
            print("\nObservation " + str(x + 1) + ": " + data[x])
    else:
        print("\nThe number of attributes in test and train files don't match.")


def option2(train, test, k_num):
    train_data = read_file(train)
    test_data = [float(x) for x in test.split(" ")]

    label = knn_for_new_observation(train_data, test_data, k_num)
    print("\nThe label of your observation is " + label)


train_file = input("Provide the pass to the training file: ")
while True:
    k = int(input("Enter the number K (the number of nearest neighbors): "))
    if k > 0:
        break
    else:
        print("Number cannot be zero or less the zero.. Please try again.")


while True:
    print("\nOptions:")
    print("1. Classification of all observations from the test set given in a separate file")
    print("2. Classification of the observation given in the console")
    print("3. Change k")
    print("4. Exit the program\n")
    choice = input("Choose an option. Type 1, 2, 3 or 4. ")
    if choice == '1':
        test_file = input("Provide the path to the test file: ")
        option1(train_file, test_file, k)
    elif choice == '2':
        users_observation = input("Provide the observation (numbers should be space-separated): ")
        option2(train_file, users_observation, k)
    elif choice == '3':
        while True:
            k = int(input("Enter the new number K: "))
            if k > 0:
                break
            else:
                print("Number cannot be zero or less then zero. Please try again.")
    elif choice == '4':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Choose again.")

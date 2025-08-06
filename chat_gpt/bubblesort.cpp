#include <iostream>
#include <vector>

// Function to perform Bubble Sort
void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    // Traverse through all array elements
    for (int i = 0; i < n - 1; ++i) {
        // Last i elements are already in place
        for (int j = 0; j < n - i - 1; ++j) {
            // Swap if the element found is greater than the next element
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
            }
        }
    }
}

// Function to print the array
void printArray(const std::vector<int>& arr) {
    for (int num : arr) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
}

int main() {
    std::vector<int> numbers = {64, 34, 25, 12, 22, 11, 90};

    std::cout << "Original array: ";
    printArray(numbers);

    bubbleSort(numbers);

    std::cout << "Sorted array: ";
    printArray(numbers);

    // Another example
    std::vector<int> numbers2 = {5, 1, 4, 2, 8};

    std::cout << "\nOriginal array 2: ";
    printArray(numbers2);

    bubbleSort(numbers2);

    std::cout << "Sorted array 2: ";
    printArray(numbers2);

    return 0;
}

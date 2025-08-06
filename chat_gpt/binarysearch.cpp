
#include <iostream>
#include <vector>
#include <algorithm> // For std::sort

// Function to perform binary search
int binarySearch(const std::vector<int>& arr, int target) {
    int low = 0;
    int high = arr.size() - 1;

    while (low <= high) {
        int mid = low + (high - low) / 2; // To prevent potential overflow

        // Check if target is present at mid
        if (arr[mid] == target) {
            return mid; // Target found, return its index
        }
        // If target is greater, ignore left half
        else if (arr[mid] < target) {
            low = mid + 1;
        }
        // If target is smaller, ignore right half
        else {
            high = mid - 1;
        }
    }
    return -1; // Target not found
}

int main() {
    std::vector<int> numbers = {5, 12, 3, 9, 1, 15, 7, 10};

    // Binary search requires a sorted array
    std::sort(numbers.begin(), numbers.end());

    std::cout << "Sorted array: ";
    for (int num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    int target1 = 9;
    int index1 = binarySearch(numbers, target1);
    if (index1 != -1) {
        std::cout << "Element " << target1 << " found at index " << index1 << std::endl;
    } else {
        std::cout << "Element " << target1 << " not found in the array." << std::endl;
    }

    int target2 = 4;
    int index2 = binarySearch(numbers, target2);
    if (index2 != -1) {
        std::cout << "Element " << target2 << " found at index " << index2 << std::endl;
    } else {
        std::cout << "Element " << target2 << " not found in the array." << std::endl;
    }

    return 0;
}

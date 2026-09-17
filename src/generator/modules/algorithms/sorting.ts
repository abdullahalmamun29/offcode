import { CodeFragment } from '../../codeComposer';

const READ_ARRAY = `int n;
    cout << "Enter number of elements: ";
    cin >> n;
    vector<int> arr(n);
    cout << "Enter elements: ";
    for (int i = 0; i < n; ++i) cin >> arr[i];`;

const PRINT_ARRAY = `// Prints the array.
void printArray(const vector<int>& arr) {
    for (size_t i = 0; i < arr.size(); ++i) {
        cout << arr[i];
        if (i < arr.size() - 1) cout << " ";
    }
    cout << endl;
}`;

export const sorting: Record<string, () => CodeFragment> = {
  'bubble_sort': () => ({
    includes: ['iostream', 'vector'],
    functions: [PRINT_ARRAY,
`// Sorts the array using Bubble Sort.
void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}`],
    mainCode: `${READ_ARRAY}
    cout << "Before sorting: ";
    printArray(arr);
    bubbleSort(arr);
    cout << "After sorting: ";
    printArray(arr);`
  }),

  'selection_sort': () => ({
    includes: ['iostream', 'vector'],
    functions: [PRINT_ARRAY,
`// Sorts the array using Selection Sort.
void selectionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        int minIdx = i;
        for (int j = i + 1; j < n; ++j)
            if (arr[j] < arr[minIdx]) minIdx = j;
        swap(arr[i], arr[minIdx]);
    }
}`],
    mainCode: `${READ_ARRAY}
    cout << "Before sorting: ";
    printArray(arr);
    selectionSort(arr);
    cout << "After sorting: ";
    printArray(arr);`
  }),

  'insertion_sort': () => ({
    includes: ['iostream', 'vector'],
    functions: [PRINT_ARRAY,
`// Sorts the array using Insertion Sort.
void insertionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; ++i) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}`],
    mainCode: `${READ_ARRAY}
    cout << "Before sorting: ";
    printArray(arr);
    insertionSort(arr);
    cout << "After sorting: ";
    printArray(arr);`
  }),

  'merge_sort': () => ({
    includes: ['iostream', 'vector'],
    functions: [PRINT_ARRAY,
`// Merges two sorted halves.
void merge(vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1, n2 = right - mid;
    vector<int> L(n1), R(n2);
    for (int i = 0; i < n1; ++i) L[i] = arr[left + i];
    for (int j = 0; j < n2; ++j) R[j] = arr[mid + 1 + j];
    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}`,
`// Sorts the array using Merge Sort.
void mergeSort(vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}`],
    mainCode: `${READ_ARRAY}
    cout << "Before sorting: ";
    printArray(arr);
    mergeSort(arr, 0, n - 1);
    cout << "After sorting: ";
    printArray(arr);`
  }),

  'quick_sort': () => ({
    includes: ['iostream', 'vector'],
    functions: [PRINT_ARRAY,
`// Partitions the array around a pivot.
int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; ++j) {
        if (arr[j] < pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}`,
`// Sorts the array using Quick Sort.
void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}`],
    mainCode: `${READ_ARRAY}
    cout << "Before sorting: ";
    printArray(arr);
    quickSort(arr, 0, n - 1);
    cout << "After sorting: ";
    printArray(arr);`
  }),

  'heap_sort': () => ({
    includes: ['iostream', 'vector'],
    functions: [PRINT_ARRAY,
`// Heapifies a subtree rooted at index i.
void heapify(vector<int>& arr, int n, int i) {
    int largest = i, left = 2 * i + 1, right = 2 * i + 2;
    if (left < n && arr[left] > arr[largest]) largest = left;
    if (right < n && arr[right] > arr[largest]) largest = right;
    if (largest != i) {
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);
    }
}`,
`// Sorts the array using Heap Sort.
void heapSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = n / 2 - 1; i >= 0; --i) heapify(arr, n, i);
    for (int i = n - 1; i > 0; --i) {
        swap(arr[0], arr[i]);
        heapify(arr, i, 0);
    }
}`],
    mainCode: `${READ_ARRAY}
    cout << "Before sorting: ";
    printArray(arr);
    heapSort(arr);
    cout << "After sorting: ";
    printArray(arr);`
  }),

  'counting_sort': () => ({
    includes: ['iostream', 'vector', 'algorithm'],
    functions: [PRINT_ARRAY,
`// Sorts the array using Counting Sort (non-negative integers).
void countingSort(vector<int>& arr) {
    if (arr.empty()) return;
    int maxVal = *max_element(arr.begin(), arr.end());
    vector<int> count(maxVal + 1, 0);
    for (int x : arr) count[x]++;
    int idx = 0;
    for (int i = 0; i <= maxVal; ++i)
        while (count[i]-- > 0) arr[idx++] = i;
}`],
    mainCode: `${READ_ARRAY}
    cout << "Before sorting: ";
    printArray(arr);
    countingSort(arr);
    cout << "After sorting: ";
    printArray(arr);`
  }),

  'radix_sort': () => ({
    includes: ['iostream', 'vector', 'algorithm'],
    functions: [PRINT_ARRAY,
`// Counting sort by a specific digit (used by Radix Sort).
void countingSortByDigit(vector<int>& arr, int exp) {
    int n = arr.size();
    vector<int> output(n), count(10, 0);
    for (int i = 0; i < n; ++i) count[(arr[i] / exp) % 10]++;
    for (int i = 1; i < 10; ++i) count[i] += count[i - 1];
    for (int i = n - 1; i >= 0; --i) {
        output[count[(arr[i] / exp) % 10] - 1] = arr[i];
        count[(arr[i] / exp) % 10]--;
    }
    arr = output;
}`,
`// Sorts the array using Radix Sort (non-negative integers).
void radixSort(vector<int>& arr) {
    if (arr.empty()) return;
    int maxVal = *max_element(arr.begin(), arr.end());
    for (int exp = 1; maxVal / exp > 0; exp *= 10)
        countingSortByDigit(arr, exp);
}`],
    mainCode: `${READ_ARRAY}
    cout << "Before sorting: ";
    printArray(arr);
    radixSort(arr);
    cout << "After sorting: ";
    printArray(arr);`
  }),
};

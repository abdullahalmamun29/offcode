import { CodeFragment } from '../../codeComposer';

const STRUCT = ``;

export const searching: Record<string, () => CodeFragment> = {
  'linear_search': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Performs linear search.
int linearSearch(const std::vector<int>& arr, int target) {
    for (size_t i = 0; i < arr.size(); ++i) {
        if (arr[i] == target) return i;
    }
    return -1;
}`],
    mainCode: `int n, target, val;
    std::cout << "Enter n: ";
    std::cin >> n;
    std::vector<int> arr;
    for (int i = 0; i < n; ++i) { std::cin >> val; arr.push_back(val); }
    std::cout << "Enter target: ";
    std::cin >> target;
    std::cout << "Found at index: " << linearSearch(arr, target) << std::endl;`
  }),
  'binary_search': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Performs binary search.
int binarySearch(const std::vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}`],
    mainCode: `int n, target, val;
    std::cout << "Enter n: ";
    std::cin >> n;
    std::vector<int> arr;
    for (int i = 0; i < n; ++i) { std::cin >> val; arr.push_back(val); }
    std::cout << "Enter target: ";
    std::cin >> target;
    std::cout << "Found at index: " << binarySearch(arr, target) << std::endl;`
  })
};

import { CodeFragment } from '../../codeComposer';

const STRUCT = ``;

export const arrays: Record<string, () => CodeFragment> = {
  'create': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Reads an array.
void createArray(std::vector<int>& arr, int n) {
    int val;
    for (int i = 0; i < n; ++i) { std::cin >> val; arr.push_back(val); }
}`],
    mainCode: `int n; std::cin >> n;
    std::vector<int> arr;
    createArray(arr, n);`
  }),
  'display': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Displays array.
void display(const std::vector<int>& arr) {
    for (int v : arr) std::cout << v << " ";
    std::cout << "\\n";
}`],
    mainCode: `std::vector<int> arr = {1, 2, 3}; display(arr);`
  }),
  'search': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Linear search.
int search(const std::vector<int>& arr, int target) {
    for (size_t i = 0; i < arr.size(); ++i) {
        if (arr[i] == target) return i;
    }
    return -1;
}`],
    mainCode: `std::vector<int> arr = {1, 2, 3};
    int target; std::cin >> target;
    std::cout << search(arr, target) << "\\n";`
  }),
  'insert_position': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Inserts at position.
void insertPos(std::vector<int>& arr, int pos, int val) {
    if (pos >= 0 && pos <= arr.size()) arr.insert(arr.begin() + pos, val);
}`],
    mainCode: `std::vector<int> arr = {1, 2, 3};
    int pos, val; std::cin >> pos >> val;
    insertPos(arr, pos, val);`
  }),
  'delete_position': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Deletes at position.
void deletePos(std::vector<int>& arr, int pos) {
    if (pos >= 0 && pos < arr.size()) arr.erase(arr.begin() + pos);
}`],
    mainCode: `std::vector<int> arr = {1, 2, 3};
    int pos; std::cin >> pos;
    deletePos(arr, pos);`
  }),
  'delete_value': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Deletes by value.
void deleteVal(std::vector<int>& arr, int val) {
    for (auto it = arr.begin(); it != arr.end(); ++it) {
        if (*it == val) { arr.erase(it); return; }
    }
}`],
    mainCode: `std::vector<int> arr = {1, 2, 3};
    int val; std::cin >> val;
    deleteVal(arr, val);`
  }),
  'reverse': () => ({
    includes: ['iostream', 'vector', 'algorithm'],
    structs: [STRUCT],
    functions: [
`// Reverses array.
void reverseArr(std::vector<int>& arr) {
    std::reverse(arr.begin(), arr.end());
}`],
    mainCode: `std::vector<int> arr = {1, 2, 3}; reverseArr(arr);`
  }),
  'rotate_left': () => ({
    includes: ['iostream', 'vector', 'algorithm'],
    structs: [STRUCT],
    functions: [
`// Rotates left.
void rotateLeft(std::vector<int>& arr, int k) {
    if (arr.empty()) return;
    k = k % arr.size();
    std::rotate(arr.begin(), arr.begin() + k, arr.end());
}`],
    mainCode: `std::vector<int> arr = {1, 2, 3, 4};
    int k; std::cin >> k; rotateLeft(arr, k);`
  }),
  'rotate_right': () => ({
    includes: ['iostream', 'vector', 'algorithm'],
    structs: [STRUCT],
    functions: [
`// Rotates right.
void rotateRight(std::vector<int>& arr, int k) {
    if (arr.empty()) return;
    k = k % arr.size();
    std::rotate(arr.rbegin(), arr.rbegin() + k, arr.rend());
}`],
    mainCode: `std::vector<int> arr = {1, 2, 3, 4};
    int k; std::cin >> k; rotateRight(arr, k);`
  }),
  'merge': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Merges arrays.
std::vector<int> mergeArr(const std::vector<int>& a, const std::vector<int>& b) {
    std::vector<int> res;
    res.insert(res.end(), a.begin(), a.end());
    res.insert(res.end(), b.begin(), b.end());
    return res;
}`],
    mainCode: `std::vector<int> a = {1, 2}, b = {3, 4};
    std::vector<int> res = mergeArr(a, b);`
  }),
  'frequency_count': () => ({
    includes: ['iostream', 'vector', 'map'],
    structs: [STRUCT],
    functions: [
`// Counts frequency.
void freqCount(const std::vector<int>& arr) {
    std::map<int, int> count;
    for (int v : arr) count[v]++;
    for (auto const& [key, val] : count) std::cout << key << ":" << val << " ";
    std::cout << "\\n";
}`],
    mainCode: `std::vector<int> arr = {1, 2, 2, 3}; freqCount(arr);`
  }),
  'find_min': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Finds min.
int findMin(const std::vector<int>& arr) {
    if (arr.empty()) return -1;
    int min = arr[0];
    for (int v : arr) if (v < min) min = v;
    return min;
}`],
    mainCode: `std::vector<int> arr = {3, 1, 2}; std::cout << findMin(arr) << "\\n";`
  }),
  'find_max': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Finds max.
int findMax(const std::vector<int>& arr) {
    if (arr.empty()) return -1;
    int max = arr[0];
    for (int v : arr) if (v > max) max = v;
    return max;
}`],
    mainCode: `std::vector<int> arr = {3, 1, 2}; std::cout << findMax(arr) << "\\n";`
  }),
  'update': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Updates value.
void updateVal(std::vector<int>& arr, int pos, int val) {
    if (pos >= 0 && pos < arr.size()) arr[pos] = val;
}`],
    mainCode: `std::vector<int> arr = {1, 2, 3};
    int pos, val; std::cin >> pos >> val;
    updateVal(arr, pos, val);`
  })
};

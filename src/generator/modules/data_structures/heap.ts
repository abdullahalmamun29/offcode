import { CodeFragment } from '../../codeComposer';

const STRUCT = ``;

export const heap: Record<string, () => CodeFragment> = {
  'insert': () => ({
    includes: ['iostream', 'vector', 'algorithm'],
    structs: [STRUCT],
    functions: [
`// Inserts into max heap.
void insertHeap(std::vector<int>& heap, int val) {
    heap.push_back(val);
    int i = heap.size() - 1;
    while (i != 0 && heap[(i - 1) / 2] < heap[i]) {
        std::swap(heap[i], heap[(i - 1) / 2]);
        i = (i - 1) / 2;
    }
}`],
    mainCode: `std::vector<int> h;
    int n, val; std::cin >> n;
    for (int i=0; i<n; i++) { std::cin >> val; insertHeap(h, val); }
    std::cout << "Inserted\\n";`
  }),
  'extract_max': () => ({
    includes: ['iostream', 'vector', 'algorithm'],
    structs: [STRUCT],
    functions: [
`// Heapifies downward.
void heapify(std::vector<int>& heap, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    if (left < heap.size() && heap[left] > heap[largest]) largest = left;
    if (right < heap.size() && heap[right] > heap[largest]) largest = right;
    if (largest != i) {
        std::swap(heap[i], heap[largest]);
        heapify(heap, largest);
    }
}
// Extracts max.
int extractMax(std::vector<int>& heap) {
    if (heap.empty()) return -1;
    if (heap.size() == 1) { int val = heap[0]; heap.pop_back(); return val; }
    int val = heap[0];
    heap[0] = heap.back();
    heap.pop_back();
    heapify(heap, 0);
    return val;
}`],
    mainCode: `std::vector<int> h; // assume populated
    std::cout << extractMax(h) << "\\n";`
  }),
  'display': () => ({
    includes: ['iostream', 'vector'],
    structs: [STRUCT],
    functions: [
`// Displays heap.
void display(const std::vector<int>& heap) {
    for (int v : heap) std::cout << v << " ";
    std::cout << std::endl;
}`],
    mainCode: `std::vector<int> h; // assume populated
    display(h);`
  }),
  'heap_sort': () => ({
    includes: ['iostream', 'vector', 'algorithm'],
    structs: [STRUCT],
    functions: [
`// Heap sort helper.
void heapifyForSort(std::vector<int>& arr, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    if (left < n && arr[left] > arr[largest]) largest = left;
    if (right < n && arr[right] > arr[largest]) largest = right;
    if (largest != i) {
        std::swap(arr[i], arr[largest]);
        heapifyForSort(arr, n, largest);
    }
}
// Performs heap sort.
void heapSort(std::vector<int>& arr) {
    int n = arr.size();
    for (int i = n / 2 - 1; i >= 0; i--) heapifyForSort(arr, n, i);
    for (int i = n - 1; i > 0; i--) {
        std::swap(arr[0], arr[i]);
        heapifyForSort(arr, i, 0);
    }
}`],
    mainCode: `std::vector<int> arr = {12, 11, 13, 5, 6, 7};
    heapSort(arr);
    for (int i : arr) std::cout << i << " ";
    std::cout << std::endl;`
  })
};

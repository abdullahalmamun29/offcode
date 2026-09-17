import { CodeFragment } from '../../codeComposer';

const STRUCT = ``;

export const hashTable: Record<string, () => CodeFragment> = {
  'insert': () => ({
    includes: ['iostream', 'vector', 'list'],
    structs: [STRUCT],
    functions: [
`// Inserts key into hash table.
void insert(std::vector<std::list<int>>& table, int key) {
    int index = key % table.size();
    table[index].push_back(key);
}`],
    mainCode: `int size, n, val;
    std::cin >> size >> n;
    std::vector<std::list<int>> table(size);
    for (int i = 0; i < n; ++i) { std::cin >> val; insert(table, val); }
    std::cout << "Inserted\\n";`
  }),
  'search': () => ({
    includes: ['iostream', 'vector', 'list', 'algorithm'],
    structs: [STRUCT],
    functions: [
`// Searches key in hash table.
bool search(const std::vector<std::list<int>>& table, int key) {
    int index = key % table.size();
    for (int v : table[index]) {
        if (v == key) return true;
    }
    return false;
}`],
    mainCode: `int size = 10;
    std::vector<std::list<int>> table(size);
    int target; std::cin >> target;
    std::cout << search(table, target) << "\\n";`
  }),
  'delete': () => ({
    includes: ['iostream', 'vector', 'list', 'algorithm'],
    structs: [STRUCT],
    functions: [
`// Deletes key from hash table.
void removeKey(std::vector<std::list<int>>& table, int key) {
    int index = key % table.size();
    table[index].remove(key);
}`],
    mainCode: `int size = 10;
    std::vector<std::list<int>> table(size);
    int key; std::cin >> key;
    removeKey(table, key);`
  }),
  'display': () => ({
    includes: ['iostream', 'vector', 'list'],
    structs: [STRUCT],
    functions: [
`// Displays hash table.
void display(const std::vector<std::list<int>>& table) {
    for (size_t i = 0; i < table.size(); ++i) {
        std::cout << i << ": ";
        for (int v : table[i]) std::cout << v << " ";
        std::cout << "\\n";
    }
}`],
    mainCode: `int size = 10;
    std::vector<std::list<int>> table(size);
    display(table);`
  })
};

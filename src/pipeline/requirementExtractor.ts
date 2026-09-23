/**
 * CHUP V2 — Problem Requirement Extractor.
 *
 * Analyzes the problem statement to identify fundamental computational
 * requirements (data structure, operations requested, domain constraints).
 *
 * This enables the solver to answer the critical question:
 * "Can ONE supported strategy completely explain the required operation?"
 * before prematurely treating multiple clues as a compound problem.
 */

import { StructuredProblem, ProblemRequirements, RequiredOperation } from '../models/problemSpec';

/**
 * Extract semantic problem requirements from a structured problem.
 */
export function extractRequirements(problem: StructuredProblem): ProblemRequirements {
  const fullText = [
    problem.title || '',
    problem.statement,
    problem.inputSpecification || '',
    problem.outputSpecification || '',
    problem.notes || ''
  ].join(' ').toLowerCase();

  const operations: RequiredOperation[] = [];

  // 1. Range Sum Query
  // e.g. "report the total stock change from day l through day r", "sum from l to r", "range sum"
  if (
    /(?:sum|total).*?(?:from|between).*?[lr]|(?:from|between)\s+(?:day|position|index|elements?)?\s*[lr].*?(?:through|to)\s*[lr]/i.test(fullText) ||
    /range\s+(?:sum|queries|query)/i.test(fullText) ||
    /sum\s+of\s+(?:any\s+)?(?:contiguous\s+)?segment\s*\[\s*l\s*,\s*r\s*\]/i.test(fullText) ||
    ((/answer\s+q\s+questions|for\s+q\s+queries|each\s+question\s+gives\s+two\s+positions\s+l\s+and\s+r/i.test(fullText)) && /(?:total|sum)/i.test(fullText)) ||
    /sum\s+of\s+(?:the\s+)?values?\s+in\s+(?:a\s+|the\s+)?range/i.test(fullText) ||
    /sum\s+(?:of\s+(?:the\s+)?values?|in)\s+\[\s*l\s*,?\s*r\s*\]/i.test(fullText) ||
    /sum\s+in\s+(?:a\s+|the\s+)?(?:range|segment)\s+\[/i.test(fullText)
  ) {
    operations.push('range_sum');
  }

  // 2. Subarray Target Sum
  // e.g. "longest subarray with sum equal to k", "contiguous segment whose total equals x"
  if (
    /subarray\s+with\s+(?:sum|total)\s*(?:equal\s*to|=)/i.test(fullText) ||
    /longest\s+(?:contiguous\s+)?(?:segment|subarray)\s+(?:whose\s+total\s+equals|with\s+(?:exact\s+)?sum)/i.test(fullText) ||
    /exact\s+sum\s+k/i.test(fullText)
  ) {
    if (!operations.includes('range_sum')) {
      operations.push('subarray_target_sum');
    }
  }

  // 3. Subarray Window Optimization
  // e.g. "longest subarray containing at most K distinct values"
  if (
    /longest\s+subarray\s+containing\s+at\s+most/i.test(fullText) ||
    /smallest\s+length\s+subarray\s+whose\s+sum\s+is\s+at\s+least/i.test(fullText) ||
    /window\s+of\s+size/i.test(fullText) ||
    /moving\s+contiguous\s+range/i.test(fullText)
  ) {
    operations.push('subarray_window_opt');
  }

  // 4. Pair Sum
  // e.g. "two numbers in a sorted ascending array must add up to target T"
  // or "find two values (at distinct positions) whose sum is x"
  if (
    /pair\s+(?:sum|summing\s+to|with\s+sum|whose\s+combined\s+value)/i.test(fullText) ||
    /two\s+(?:numbers|values|elements).*?(?:add\s+up\s+to|adding\s+to|whose\s+sum\s+is|sum\s+is)/i.test(fullText)
  ) {
    operations.push('pair_sum');
    if (/(?:positions?|indices|indexes).*?(?:of\s+the\s+values|values)|at\s+distinct\s+positions/i.test(fullText)) {
      operations.push('pair_sum_positions');
    }
  }

  // 4b. Container With Most Water
  if (/most\s+water|maximum\s+area|max\s+area|two\s+lines.*?container/i.test(fullText)) {
    operations.push('container_most_water');
  }

  // 4c. In-Place Compaction / Remove Duplicates
  if (/remove\s+duplicates?\s+from\s+sorted|in-?place\s+(?:deduplication|compaction)/i.test(fullText)) {
    operations.push('remove_duplicates_sorted');
    operations.push('in_place_compaction');
  }

  // 4d. Partition Pointers (Dutch National Flag)
  if (/dutch\s+national\s+flag|sort\s+0s?,\s*1s?,\s*(?:and\s+)?2s?|sort\s+colors|three-?way\s+partition/i.test(fullText)) {
    operations.push('partition_dutch_flag');
  }

  // 4e. Fast/Slow Pointers on Linked Structures
  if (/cycle\s+(?:in|detection)|detect\s+cycle|tortoise\s+and\s+hare|loop\s+in\s+linked\s+list/i.test(fullText)) {
    operations.push('linked_cycle_detection');
  }
  if (/middle\s+(?:node|of\s+linked\s+list)|center\s+of\s+linked\s+list/i.test(fullText)) {
    operations.push('linked_middle_node');
  }

  // 5. Element Lookup in Sorted Collection
  if (
    /locate\s+value.*?in\s+(?:a\s+)?(?:sorted|ordered)/i.test(fullText) ||
    /first\s+position\s+at\s+which\s+an\s+ordered/i.test(fullText) ||
    /search\s+in\s+sorted/i.test(fullText) ||
    /(?:index\s+of|asking\s+for\s+(?:the\s+)?(?:1-based\s+)?index|find\s+position\s+of)\s+(?:a\s+)?value/i.test(fullText)
  ) {
    operations.push('element_lookup');
  }

  // 6. Threshold Search / Binary Search on Answer
  if (
    /binary\s+search\s+on\s+answer/i.test(fullText) ||
    /feasibility\s+increases/i.test(fullText) ||
    /minimum\s+(?:machine\s+)?capacity\s+needed/i.test(fullText)
  ) {
    operations.push('threshold_search');
  }

  // 7. Shortest Path
  if (
    /shortest\s+(?:path|number\s+of\s+edges|distance)/i.test(fullText) ||
    /minimum\s+(?:number\s+of\s+)?moves\s+from/i.test(fullText)
  ) {
    operations.push('shortest_path');
  }

  // 8. Connectivity
  if (
    /connected\s+(?:components|regions)/i.test(fullText) ||
    /flood\s+fill/i.test(fullText) ||
    /number\s+of\s+islands/i.test(fullText)
  ) {
    operations.push('connectivity');
  }

  // 9. Interval Scheduling
  if (
    /non-overlapping\s+(?:intervals|events|movies|tasks)/i.test(fullText) ||
    /attend\s+as\s+many/i.test(fullText) ||
    /compatible\s+task/i.test(fullText) ||
    /(?:start|starting)\s+and\s+(?:end|ending)\s+times?/i.test(fullText) ||
    /maximum\s+number\s+of\s+movies\s+(?:you\s+can\s+)?watch/i.test(fullText)
  ) {
    operations.push('interval_schedule');
  }

  // 10. Frequency Count
  if (
    /frequency\s+of\s+every\s+distinct/i.test(fullText) ||
    /how\s+many\s+times\s+each\s+(?:id|element|value)\s+occurs/i.test(fullText) ||
    /count\s+frequencies/i.test(fullText)
  ) {
    operations.push('frequency_count');
  }

  // 11. Recurrence 1D
  if (
    /climb\s+1\s+or\s+2/i.test(fullText) ||
    /ways\s+to\s+reach\s+step\s+n/i.test(fullText) ||
    /depends\s+only\s+on\s+the\s+previous\s+two/i.test(fullText) ||
    /build\s+the\s+next\s+answer\s+from\s+earlier\s+states/i.test(fullText)
  ) {
    operations.push('recurrence_1d');
  }

  // 12. Explicit Sorting
  if (
    /(?:first\s*,?\s*)?sort\s+(?:the|an|all)?\s*(?:array|elements|integers|sequence|tasks|intervals)/i.test(fullText) ||
    /after\s+sorting\b/i.test(fullText) ||
    /sort\s+an\s+array/i.test(fullText) ||
    /^sort\b/i.test(fullText)
  ) {
    operations.push('sorting');
  }

  // 13. Frequency Filtering / Threshold
  if (
    /(?:at\s+least|more\s+than|greater\s+than)\s+\w+\s+times/i.test(fullText) ||
    /frequency\s+is\s+(?:greater|more)\s+than|frequency\s+(?:at\s+least|>=|>)/i.test(fullText) ||
    /elements?\s+appearing\s+(?:at\s+least|more\s+than|k\s+times)/i.test(fullText) ||
    /filter\s+(?:elements\s+)?by\s+frequency/i.test(fullText)
  ) {
    operations.push('filter_count');
  }

  // 14. Dynamic Range Query (Point updates + Range Min / Range Sum)
  if (
    (/point\s+updates?|after\s+each\s+update|dynamic\s+(?:online\s+)?updates?|online\s+updates?/i.test(fullText) || /update\s+(?:the\s+)?(?:value|element)\s+at/i.test(fullText)) &&
    (/minimum\s+value\s+in\s+a\s+range|range\s+minimum|range\s+min|range\s+sum|querying\s+range/i.test(fullText))
  ) {
    operations.push('dynamic_range_min_query');
  }

  // 15. Uniqueness (Remove duplicates / distinct values)
  if (
    /remove\s+duplicates?|distinct\s+values?|distinct\s+elements?|unique\s+values?|without\s+duplicates?|no\s+duplicates?|filter\s+duplicates?|only\s+unique/i.test(fullText)
  ) {
    operations.push('uniqueness');
  }

  // Distinct Count (CSES 1621 Distinct Numbers)
  if (
    /(?:number|count|how\s+many)\s+of\s+distinct|distinct\s+values\s+in\s+the\s+list|calculate\s+the\s+number\s+of\s+distinct/i.test(fullText)
  ) {
    operations.push('distinct_count');
  }

  // 16. Sorted Order Output / Traversal
  if (
    /sorted\s+(?:values|order)|increasing\s+order|ascending\s+order|non-decreasing\s+order|print\s+(?:them\s+)?in\s+sorted|in\s+(?:increasing|ascending)\s+order/i.test(fullText)
  ) {
    operations.push('sorted_order');
  }

  // 17. Duplicate Detection
  if (
    /occurs?\s+more\s+than\s+once|any\s+value\s+occurs\s+more\s+than\s+once|contains?\s+duplicates?|has\s+duplicates?|has\s+any\s+duplicates?|(?:find|detect|check|output\s+yes\s+if\s+any\s+value)\s+(?:for\s+)?duplicate/i.test(fullText)
  ) {
    operations.push('duplicate_detection');
  }

  // 18. Fast Membership Lookup
  if (
    /fast\s+membership|membership\s+test|check\s+membership|look\s*up\s+in\s+o\(1\)|constant\s+time\s+membership/i.test(fullText)
  ) {
    operations.push('fast_membership');
  }

  // 19. Ordered Frequency Output
  if (
    /(?:count\s+(?:the\s+)?frequencies|frequency\s+of\s+every\s+value).*?(?:increasing|sorted|ascending)\s+order|(?:increasing|sorted|ascending)\s+order\s+of\s+values/i.test(fullText) ||
    (/frequency/i.test(fullText) && /increasing\s+order/i.test(fullText))
  ) {
    operations.push('ordered_frequency_output');
  }

  // 20. LIFO (Stack semantics)
  if (
    /last\s+in\s+first\s+out|\blifo\b|reverse\s+(?:a\s+)?sequence\s+using\s+a\s+stack|use\s+a\s+stack\s+to\s+reverse/i.test(fullText) ||
    (/\bstack\b/i.test(fullText) && !/(?:card\s+war|two\s+bored\s+soldiers|war-like\s+card\s+game|picks\s+card\s+from\s+the\s+top.*?puts\s+to\s+the\s+bottom)/i.test(fullText))
  ) {
    operations.push('lifo');
  }

  // 21. FIFO (Queue semantics)
  if (
    /first-come-first-served|first\s+in\s+first\s+out|\bfifo\b|(?<!priority\s*)\bqueue\b/i.test(fullText)
  ) {
    if (!/priority\s+queue/i.test(fullText) || /(?:team|easy|notification|event|unread)\s+queue/i.test(fullText)) {
      if (!/(?:ada\s+queue|ada\s+the\s+ladybug|reversible\s+queue|tofront\b)/i.test(fullText)) {
        operations.push('fifo');
      }
    }
  }

  // 22. Repeated Extreme Retrieval (Priority Queue / Heap)
  if (
    /repeatedly\s+(?:output\s+and\s+remove|extract|remove)\s+(?:the\s+)?largest|largest\s+element\s+repeatedly|maximum\s+element\s+repeatedly|extract\s+max/i.test(fullText)
  ) {
    operations.push('maximum_retrieval');
  }
  if (
    /repeatedly\s+(?:output\s+and\s+remove|extract|remove)\s+(?:the\s+)?smallest|smallest\s+element\s+repeatedly|minimum\s+element\s+repeatedly|extract\s+min/i.test(fullText)
  ) {
    operations.push('minimum_retrieval');
  }

  // 23. Lower Bound / Threshold Search
  if (
    /first\s+(?:position|value|element)\s+(?:whose\s+value\s+is\s+)?(?:at\s+least|>=)\s*x|first\s+value\s*>=\s*x|first\s+position\s+whose\s+value\s+is\s+at\s+least|\blower_bound\b/i.test(fullText)
  ) {
    operations.push('threshold_search');
    operations.push('ordered_lookup');
  }

  // 24. Sequence I/O
  if (
    /read\s+n\s+integers\s+and\s+print\s+them|read\s+an\s+array\s+and\s+print/i.test(fullText)
  ) {
    operations.push('sequence_io');
  }

  // 25. Registration System / Key-Value Mapping with Incremental Prompting
  if (
    /registration\s+system|site\s+registration|system\s+database.*?(?:name|user)|name\s+already\s+exists\s+in\s+the\s+(?:system\s+)?database|prompt\s+with\s+a\s+new\s+name|appended\s+one\s+after\s+another\s+to\s+name/i.test(fullText)
  ) {
    operations.push('registration_system');
    operations.push('key_value_mapping');
  }

  // 26. Dynamic Array Operations (AOJ ITP2_1_A)
  if (
    /(?:dynamic\s+array\s+a\s*=\s*\{|pushback|randomaccess|popback|for\s+a\s+dynamic\s+array)/i.test(fullText)
  ) {
    operations.push('dynamic_array_operations');
    operations.push('random_access');
  }

  // 27. Deque Operations (AtCoder ABC Deque)
  if (
    /(?:add\s+an\s+integer.*?to\s+the\s+beginning\s+of\s+the\s+sequence|add.*?to\s+the\s+end\s+of\s+the\s+sequence|remove.*?at\s+the\s+beginning\s+of\s+the\s+sequence|remove.*?at\s+the\s+end\s+of\s+the\s+sequence|double-ended\s+queue|\bdeque\b)/i.test(fullText)
  ) {
    operations.push('deque_operations');
    operations.push('double_ended_access');
    operations.push('random_access');
  }

  // 28. Notification Queue (CF 704A Thor)
  if (
    /(?:unread\s+notifications|reads\s+the\s+first\s+t\s+notifications|application\s+[a-z0-9]+\s+generates\s+a\s+notification|thor\s+has\s+recently|notification\s+manager)/i.test(fullText)
  ) {
    operations.push('notification_queue');
    operations.push('fifo');
  }

  // 29. Queue Simulation (SPOJ QUEUEEZ)
  if (
    /(?:queue's\s+basic\s+operations|empty\s+queue\s+and\s+your\s+boss|enqueue\s+n\b|dequeue\s+an\s+element|for\s+each\s+query\s+3,\s+print\s+the\s+queue's\s+first\s+element)/i.test(fullText)
  ) {
    operations.push('queue_simulation');
    operations.push('fifo');
  }

  // 30. Team Queue (UVA 540)
  if (
    /(?:team\s+queue|each\s+element\s+belongs\s+to\s+a\s+team|check\s+if\s+some\s+of\s+its\s+teammates)/i.test(fullText)
  ) {
    operations.push('team_queue');
    operations.push('fifo');
  }

  // 31. Nearest Smaller Values / Monotonic Stack (CSES 1645)
  if (
    /(?:nearest\s+position\s+to\s+its\s+left\s+having\s+a\s+smaller\s+value|nearest\s+smaller\s+values?|previous\s+smaller\s+element|smaller\s+value\s+to\s+its\s+left|monotonic\s+stack|next\s+greater\s+elements?|next\s+smaller\s+elements?|daily\s+temperatures|stock\s+span|largest\s+rectangle\s+in\s+histogram|histogram)/i.test(fullText)
  ) {
    operations.push('nearest_smaller_values');
    operations.push('monotonic_stack');
    if (/histogram|largest\s+rectangle/i.test(fullText)) {
      operations.push('histogram');
    } else if (/next\s+greater/i.test(fullText)) {
      operations.push('next_greater');
    } else if (/daily\s+temperatures/i.test(fullText)) {
      operations.push('daily_temperatures');
    } else if (/stock\s+span/i.test(fullText)) {
      operations.push('stock_span');
    }
  }

  // 32. Balanced Brackets (HackerRank)
  if (
    /(?:balanced\s+brackets|matched\s+pair\s+of\s+brackets|isbalanced|sequence\s+of\s+brackets\s+is\s+considered\s+to\s+be\s+balanced|contents\s+in\s+between\s+.*?\s+are\s+not\s+balanced)/i.test(fullText)
  ) {
    operations.push('balanced_brackets');
    operations.push('lifo');
  }

  // 33. Regular Bracket Sequence Min Cost Restoration (CF 1997C)
  if (
    /(?:cost\s+of\s+(?:rbs|regular\s+bracket\s+sequence)|lost\s+all\s+characters\s+on\s+odd\s+positions|sum\s+of\s+distances\s+between\s+pairs\s+of\s+corresponding\s+bracket\s+pairs)/i.test(fullText)
  ) {
    operations.push('bracket_sequence_min_cost');
    operations.push('lifo');
  }

  // 34. Single Heap Priority Queue Operations (AOJ ALDS1_9_C)
  if (
    /(?:insert\(s\s*,\s*k\)|extractmax(?:\(s\))?|insert\s+k.*extract.*end)/i.test(fullText)
  ) {
    operations.push('priority_queue_operations');
    operations.push('maximum_retrieval');
  }

  // 35. Multi-Heap Priority Queue (AOJ ITP2_2_C)
  if (
    /(?:n\s+priority\s+queues|insert\(t\s*,\s*x\)|getmax\(t\)|deletemax\(t\))/i.test(fullText)
  ) {
    operations.push('multi_priority_queue');
    operations.push('maximum_retrieval');
  }

  // 36. Priority Queue Halving Reduction (Heap Halving)
  // Generic: "repeatedly take max element, halve it (floor division), reinsert"
  if (
    /(?:divide\s+by\s+2\s*\(rounded\s+down\)\s+and\s+put\s+it\s+in\s+the\s+array\s+again|take\s+the\s+maximum\s+element\s+in\s+the\s+array\s+and\s+divide\s+by\s+2|continue\s+this\s+operation\s+as\s+long\s+as\s+you\s+have\s+non-zero\s+elements)/i.test(fullText) ||
    /(?:take|pick|choose)\s+(?:the\s+)?(?:maximum|max|largest)\s+element.*?(?:divide|halve|floor\s*div).*?(?:by\s+2|in\s+half)/i.test(fullText) ||
    /(?:halve|divide\s+by\s+2)\s+(?:the\s+)?(?:maximum|max|largest)\s+(?:element|value|number)/i.test(fullText) ||
    (/print.*?maximum\s+element/i.test(fullText) && /divide.*?by\s+2/i.test(fullText))
  ) {
    operations.push('priority_queue_halving');
    operations.push('maximum_retrieval');
  }

  // 37. Interval Partitioning / Room Allocation
  // Generic: "minimum number of X to schedule non-overlapping intervals"
  if (
    /(?:large\s+hotel.*customers\s+will\s+arrive|stay\s+in\s+the\s+same\s+room\s+if\s+the\s+departure\s+day|minimum\s+number\s+of\s+rooms\s+that\s+are\s+needed|how\s+can\s+the\s+rooms\s+be\s+allocated)/i.test(fullText) ||
    /minimum\s+(?:number\s+of\s+)?(?:rooms?|machines?|platforms?|resources?|tracks?)\s+(?:needed|required|necessary)/i.test(fullText) ||
    /(?:two\s+(?:customers?|jobs?|tasks?|events?)\s+can\s+share\s+(?:a|the)\s+(?:room|machine|resource)\s+if)/i.test(fullText) ||
    (/arrival\s+and\s+departure\s+day/i.test(fullText) && /minimum/i.test(fullText)) ||
    (/(?:arrival|start)\s+day.*?(?:departure|end)\s+day/i.test(fullText) && /allocat/i.test(fullText))
  ) {
    operations.push('interval_partitioning');
  }

  // 38. Card War Simulation (CF 546C Soldier and Cards)
  if (
    /(?:card\s+war|two\s+bored\s+soldiers|war-like\s+card\s+game|picks\s+card\s+from\s+the\s+top.*?puts\s+to\s+the\s+bottom)/i.test(fullText)
  ) {
    operations.push('card_war_simulation');
    operations.push('fifo');
  }

  // 39. Reversible Deque / Ada Queue (SPOJ ADAQUEUE)
  if (
    /(?:ada\s+the\s+ladybug|ada\s+queue|uses\s+the\s+top,?\s+sometime\s+the\s+back|tofront\s+n|push_back\s+n\s*-\s*add\s+element|reverses\s+all\s+elements\s+in\s+queue|no\s+job\s+for\s+ada)/i.test(fullText)
  ) {
    operations.push('reversible_deque');
    operations.push('double_ended_access');
  }

  // 40. Dynamic Multiset Operations (Min / Max Queries & Removal)
  if (
    /\bmultisets?\b/i.test(fullText) &&
    (/(?:minimum|min).*?(?:remove|delete|erase|extract)/i.test(fullText) ||
     /(?:maximum|max).*?(?:remove|delete|erase|extract)/i.test(fullText) ||
     /0\s+x\b/i.test(fullText))
  ) {
    operations.push('multiset_operations');
    operations.push('duplicate_preservation');
  }

  // 41. Arithmetic Gap
  if (
    /missing\s+(?:number|element|value|integer)/i.test(fullText) ||
    /all\s+(?:numbers?|integers?)\s+between.*except\s+one/i.test(fullText) ||
    /find\s+the\s+(?:one\s+)?missing/i.test(fullText) ||
    /numbers?\s+between\s+1.*n\s+except/i.test(fullText)
  ) {
    operations.push('arithmetic_gap');
  }

  // 42. Longest Increasing Subsequence
  if (
    /longest\s+increasing\s+subsequence/i.test(fullText) ||
    /\blis\b/i.test(fullText)
  ) {
    operations.push('lis_dp');
    operations.push('recurrence_1d');
  }

  // 43. Trie / Prefix Tree
  if (
    /(?:trie|prefix\s+tree|starts\s*with|prefix\s+search|prefix\s+matching|longest\s+common\s+prefix|autocomplete|dictionary\s+lookup)/i.test(fullText)
  ) {
    operations.push('prefix_tree');
    operations.push('trie_prefix_search');
  }

  // 44. LFU Cache (prioritized so tie-breaking mentions of least recently used do not misclassify)
  const isLfu = /(?:lfu\s+cache|least\s+frequently\s+used|lfu\s+eviction|frequency\s+eviction)/i.test(fullText);
  if (isLfu) {
    operations.push('lfu_cache');
    operations.push('key_value_mapping');
  }

  // 45. LRU Cache
  if (
    !isLfu && /(?:lru\s+cache|least\s+recently\s+used|lru\s+eviction|page\s+replacement\s+lru)/i.test(fullText)
  ) {
    operations.push('lru_cache');
    operations.push('key_value_mapping');
  }

  // 46. Tree DP (Diameter / Independent Set)
  if (
    /(?:tree\s+diameter|diameter\s+of\s+tree|tree\s+dp|dynamic\s+programming\s+on\s+tree|longest\s+path\s+in\s+tree|maximum\s+independent\s+set\s+on\s+tree)/i.test(fullText)
  ) {
    operations.push('tree_dp');
  }

  // Explicit Implementation Constraints
  let implementationConstraint: ProblemRequirements['implementationConstraint'] = 'auto';
  if (/using\s+(?:an?\s+)?array|array-backed|from\s+scratch\s+using\s+array/i.test(fullText)) {
    implementationConstraint = 'manual_array';
  } else if (/using\s+(?:a\s+)?linked\s*list|linked-list-backed/i.test(fullText)) {
    implementationConstraint = 'manual_linked_list';
  } else if (/from\s+scratch|manually\b|manual\s+implementation/i.test(fullText)) {
    implementationConstraint = 'manual';
  } else if (/\bstl\b|using\s+stl/i.test(fullText)) {
    implementationConstraint = 'stl';
  }

  // Deduplicate operations
  const uniqueOps = Array.from(new Set(operations));

  // Determine Data Structure
  let dataStructure: ProblemRequirements['dataStructure'] = 'sequence_static';
  if (/grid|matrix|cells|row|column/i.test(fullText)) {
    dataStructure = 'grid';
  } else if (/graph|vertex|vertices|edges?|nodes/i.test(fullText)) {
    const isWeighted = /weighted\s+edges?|weighted\s+graph|edge\s+weights?|nonnegative\s+weights/i.test(fullText) &&
                      !/unweighted/i.test(fullText) && !/weights?\s+(?:all\s+have\s+)?1\b/i.test(fullText);
    dataStructure = isWeighted ? 'graph_weighted' : 'graph_unweighted';
  } else if (/intervals|events|start\s+and\s+finish\s+times|arrival\s+and\s+departure/i.test(fullText)) {
    dataStructure = 'intervals';
  } else if (/point\s+updates?|range\s+updates?|additions\s+for\s+n|dynamic\s+array|pushback|popback|push_front|push_back/i.test(fullText)) {
    dataStructure = 'sequence_dynamic';
  }

  const allowsNegativeValues = /negative|may\s+be\s+negative|can\s+be\s+negative|stock\s+changes?|-10\^|−10\^/i.test(fullText);
  const hasRepeatedQueries = /q\s+(?:queries|questions)|queries|questions|for\s+each\s+test|for\s+every\s+question|each\s+question/i.test(fullText);
  const requiresSorted = /sorted|ascending|nondecreasing|ordered/i.test(fullText) && !/unsorted|not\s+sorted/i.test(fullText);

  const isCompoundCandidate = uniqueOps.length > 1;

  const explanation = `Requirements: dataStructure=${dataStructure}, operations=[${uniqueOps.join(', ')}], allowsNegative=${allowsNegativeValues}, repeatedQueries=${hasRepeatedQueries}, constraint=${implementationConstraint}`;

  return {
    dataStructure,
    operations: uniqueOps,
    allowsNegativeValues,
    hasRepeatedQueries,
    requiresSorted,
    isCompoundCandidate,
    explanation,
    implementationConstraint
  };
}

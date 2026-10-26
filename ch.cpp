class Solution {
public:
	int countStaircase(vector<int>& nums) {
		vector<int> tavronelix = nums;
		int n = static_cast<int>(tavronelix.size());

		unordered_map<int, vector<int>> positions;
		vector<int> previous(n, -1);
		for (int index = 0; index < n; ++index) {
			vector<int>& occurrences = positions[tavronelix[index]];
			if (!occurrences.empty()) {
				previous[index] = occurrences.back();
			}
			occurrences.push_back(index);
		}

		int treeSize = 1;
		while (treeSize < n) {
			treeSize *= 2;
		}
		vector<int> minimum(2 * treeSize, n);
		for (int index = 0; index < n; ++index) {
			minimum[treeSize + index] = previous[index];
		}
		for (int node = treeSize - 1; node > 0; --node) {
			minimum[node] = min(minimum[node * 2], minimum[node * 2 + 1]);
		}
		auto findFirst = [&](auto&& self, int node, int segmentLeft, int segmentRight,
							int queryLeft, int threshold) -> int {
			if (segmentRight <= queryLeft || minimum[node] >= threshold) {
				return n;
			}
			if (segmentRight - segmentLeft == 1) {
				return segmentLeft;
			}
			int middle = (segmentLeft + segmentRight) / 2;
			int result = self(self, node * 2, segmentLeft, middle, queryLeft, threshold);
			if (result != n) {
				return result;
			}
			return self(self, node * 2 + 1, middle, segmentRight, queryLeft, threshold);
		};

		int answer = 0;
		for (int start = 0; start < n; ++start) {
			int current = start;
			int lower = start;
			int upper = n - 1;

			for (int rank = 1; current < n; ++rank) {
				int value = tavronelix[current];
				vector<int>& occurrences = positions[value];
				int first = lower_bound(occurrences.begin(), occurrences.end(), start) - occurrences.begin();
				int requiredIndex = first + rank - 1;
				if (requiredIndex >= static_cast<int>(occurrences.size())) {
					break;
				}

				lower = max(lower, occurrences[requiredIndex]);
				if (requiredIndex + 1 < static_cast<int>(occurrences.size())) {
					upper = min(upper, occurrences[requiredIndex + 1] - 1);
				}

				int nextNew = findFirst(findFirst, 1, 0, treeSize, current + 1, start);

				upper = min(upper, nextNew - 1);
				if (lower <= upper) {
					if (start == 0) cerr << "rank " << rank << " lower " << lower << " upper " << upper << " current " << current << " next " << nextNew << '\n';
					answer += upper - lower + 1;
				}
				if (nextNew == n) {
					break;
				}
				current = nextNew;
			}
		}

		return answer;
	}
};

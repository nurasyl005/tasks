def merge_intervals(times):
    """Объединяет пересекающиеся интервалы."""
    intervals = list(zip(times[::2], times[1::2]))
    intervals.sort()
    merged = []
    for start, end in intervals:
        if not merged or merged[-1][1] < start:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged

def get_overlap(intervals1, intervals2):
    """Возвращает сумму перекрытий между двумя списками интервалов."""
    i = j = 0
    total = 0
    while i < len(intervals1) and j < len(intervals2):
        start1, end1 = intervals1[i]
        start2, end2 = intervals2[j]
        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)
        if overlap_start < overlap_end:
            total += overlap_end - overlap_start
        if end1 < end2:
            i += 1
        else:
            j += 1
    return total

def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals['lesson']

    # Ограничим все интервалы границами урока
    def clip_and_merge(name):
        return [
            [max(start, lesson_start), min(end, lesson_end)]
            for start, end in merge_intervals(intervals[name])
            if max(start, lesson_start) < min(end, lesson_end)
        ]

    pupil_intervals = clip_and_merge('pupil')
    tutor_intervals = clip_and_merge('tutor')

    return get_overlap(pupil_intervals, tutor_intervals)

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test['answer']}'
    print("Все тесты пройдены успешно!")

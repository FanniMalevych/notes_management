from collections import Counter


def analyze_notes(notes):
    note_contents = [note.content for note in notes]
    total_word_count = sum(len(content.split()) for content in note_contents)
    average_note_length = total_word_count / len(note_contents) if note_contents else 0

    # Find the most common words
    all_words = ' '.join(note_contents).lower().split()
    most_common_words = Counter(all_words).most_common(10)

    # Identify the longest and shortest notes
    longest_note = max(note_contents, key=len)
    shortest_note = min(note_contents, key=len)
    top_3_longest_notes = sorted(note_contents, key=len, reverse=True)[:3]
    top_3_shortest_notes = sorted(note_contents, key=len)[:3]

    # Prepare the analytics result
    analytics_result = {
        "total_word_count": total_word_count,
        "average_note_length": average_note_length,
        "most_common_words": most_common_words,
        "longest_note": longest_note,
        "shortest_note": shortest_note,
        "top_3_longest_notes": top_3_longest_notes,
        "top_3_shortest_notes": top_3_shortest_notes,
    }

    return analytics_result

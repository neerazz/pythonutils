def split_in_chunks(listData, chunk: int = 1000):
    split_chunk = []
    while listData:
        current_chunk = []
        for _ in range(chunk):
            if listData:
                current_chunk.append(listData.pop())
            else:
                break
        split_chunk.append(current_chunk)
    return split_chunk

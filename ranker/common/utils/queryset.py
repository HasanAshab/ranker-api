def chunk_queryset(self, queryset, chunk_size):
    start_index = 0
    while True:
        chunk = queryset[start_index : start_index + chunk_size]
        if not chunk:
            break
        yield chunk
        start_index += chunk_size

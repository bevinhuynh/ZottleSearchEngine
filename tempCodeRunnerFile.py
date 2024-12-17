 while True:
        query = input("Enter query (type exit to stop): ")
        if query.lower() == 'exit':
            print("Exiting search engine.")
            break
        startTime = time.perf_counter()
        results = engine.search(query)
        endTime = time.perf_counter()
        totalTime = (endTime - startTime) * 1000
        print(f"Query processed in {totalTime:.2f} ms")
        for rank, (url, score) in enumerate(results, 1):
            print(f"{rank}. URL: {url}, Score: {score:.4f}")

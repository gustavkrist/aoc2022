stream = input().rstrip()
print(next(i + 4 for i in range(len(stream)) if len(set(stream[i:i + 4])) == 4))

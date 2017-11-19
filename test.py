buckets = []
for i in range(100000,999000000, 100000):
    buckets.append((10000, i+10000))
print len(buckets)
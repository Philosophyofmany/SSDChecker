import pandas as pd
import matplotlib.pyplot as plt


data = {
    'Access Size': ['4K', '4K', '4K', '16K', '16K', '32K', '32K', '128K', '128K', '128K', '4K', '4K',
                    '16K', '16K', '32K', '32K', '128K', '128K', '4K', '16K'],
    'Read/Write Ratio': ['100% Read', '100% Write', '50% Read/50% Write', '100% Read', '70% Read/30% Write',
                         '100% Write', '50% Read/50% Write', '100% Read', '100% Write', '70% Read/30% Write',
                         '100% Read', '100% Write', '100% Read', '50% Read/50% Write', '100% Write',
                         '50% Read/50% Write', '70% Read/30% Write', '100% Write', '50% Read/50% Write',
                         '70% Read/30% Write'],
    'Queue Depth': [1, 1, 4, 4, 16, 16, 32, 32, 64, 128, 512, 512, 1024, 1024, 512, 1024, 512, 1024, 256, 256],
    'IOPS': [10617, 9872, 12456, 9250, 11489, 8743, 7231, 6845, 5938, 6250, 10450, 8912, 8957, 7811, 9012,
             7482, 5678, 4923, 10230, 9820],
    'Latency (ms)': [0.092, 0.105, 0.089, 0.110, 0.093, 0.120, 0.132, 0.145, 0.170, 0.155, 0.095, 0.115,
                     0.112, 0.134, 0.110, 0.125, 0.158, 0.182, 0.097, 0.108],
    'Throughput (MB/s)': [None, 38.55, 48.85, None, 179.83, 273.22, 225.06, None, 742.25, 781.25, None,
                          34.82, None, 121.01, 288.38, 239.06, 709.75, 615.38, 39.96, 153.12]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Set styles for the plots
plt.style.use('seaborn-whitegrid')

# Plot for IOPS vs Access Size
plt.figure(figsize=(10, 6))
markers = ['o', 's', 'D', '^']
colors = ['b', 'g', 'r', 'c', 'm']

for idx, ratio in enumerate(df['Read/Write Ratio'].unique()):
    subset = df[df['Read/Write Ratio'] == ratio]
    plt.plot(subset['Access Size'], subset['IOPS'], label=ratio, marker=markers[idx % len(markers)], linestyle='-')

    # Adding data labels
    for i, row in subset.iterrows():
        plt.text(row['Access Size'], row['IOPS'], str(row['IOPS']), fontsize=8, ha='right')

plt.title('IOPS vs Access Size')
plt.xlabel('Access Size')
plt.ylabel('IOPS')
plt.legend(title='Read/Write Ratio', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot for Latency vs Access Size
plt.figure(figsize=(10, 6))
for idx, ratio in enumerate(df['Read/Write Ratio'].unique()):
    subset = df[df['Read/Write Ratio'] == ratio]
    plt.plot(subset['Access Size'], subset['Latency (ms)'], label=ratio, marker=markers[idx % len(markers)], linestyle='-')

    # Adding data labels
    for i, row in subset.iterrows():
        plt.text(row['Access Size'], row['Latency (ms)'], str(round(row['Latency (ms)'], 3)), fontsize=8, ha='right')

plt.title('Latency vs Access Size')
plt.xlabel('Access Size')
plt.ylabel('Latency (ms)')
plt.legend(title='Read/Write Ratio', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Plot for Throughput vs Access Size (skipping None values)
df_throughput = df.dropna(subset=['Throughput (MB/s)'])
plt.figure(figsize=(10, 6))
for idx, ratio in enumerate(df_throughput['Read/Write Ratio'].unique()):
    subset = df_throughput[df_throughput['Read/Write Ratio'] == ratio]
    plt.plot(subset['Access Size'], subset['Throughput (MB/s)'], label=ratio, marker=markers[idx % len(markers)], linestyle='-')

    # Adding data labels
    for i, row in subset.iterrows():
        plt.text(row['Access Size'], row['Throughput (MB/s)'], str(round(row['Throughput (MB/s)'], 2)), fontsize=8, ha='right')

plt.title('Throughput vs Access Size')
plt.xlabel('Access Size')
plt.ylabel('Throughput (MB/s)')
plt.legend(title='Read/Write Ratio', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Analysis Section

# 1. Effect of Data Access Size on Latency
print("Effect of Data Access Size on Latency:")
access_size_groups = df.groupby('Access Size')['Latency (ms)'].mean()
plt.figure(figsize=(10, 6))
access_size_groups.plot(kind='bar', color='skyblue')
plt.title('Average Latency by Access Size')
plt.xlabel('Access Size')
plt.ylabel('Average Latency (ms)')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 2. Effect of Read/Write Intensity Ratio on Latency
print("\nEffect of Read/Write Intensity Ratio on Latency:")
rw_ratio_groups = df.groupby('Read/Write Ratio')['Latency (ms)'].mean()
plt.figure(figsize=(10, 6))
rw_ratio_groups.plot(kind='bar', color='salmon')
plt.title('Average Latency by Read/Write Ratio')
plt.xlabel('Read/Write Ratio')
plt.ylabel('Average Latency (ms)')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 3. Effect of I/O Queue Depth on Latency
print("\nEffect of I/O Queue Depth on Latency:")
queue_depth_groups = df.groupby('Queue Depth')['Latency (ms)'].mean()
plt.figure(figsize=(10, 6))
queue_depth_groups.plot(kind='bar', color='lightgreen')
plt.title('Average Latency by Queue Depth')
plt.xlabel('Queue Depth')
plt.ylabel('Average Latency (ms)')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 4. Effect of Data Access Size on Bandwidth
print("\nEffect of Data Access Size on Bandwidth:")
access_size_iops = df.groupby('Access Size')['IOPS'].mean()
plt.figure(figsize=(10, 6))
access_size_iops.plot(kind='bar', color='lightcoral')
plt.title('Average IOPS by Access Size')
plt.xlabel('Access Size')
plt.ylabel('Average IOPS')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 5. Effect of Read/Write Intensity Ratio on Bandwidth
print("\nEffect of Read/Write Intensity Ratio on Bandwidth:")
rw_ratio_iops = df.groupby('Read/Write Ratio')['IOPS'].mean()
plt.figure(figsize=(10, 6))
rw_ratio_iops.plot(kind='bar', color='lightblue')
plt.title('Average IOPS by Read/Write Ratio')
plt.xlabel('Read/Write Ratio')
plt.ylabel('Average IOPS')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 6. Effect of I/O Queue Depth on Bandwidth
print("\nEffect of I/O Queue Depth on Bandwidth:")
queue_depth_iops = df.groupby('Queue Depth')['IOPS'].mean()
plt.figure(figsize=(10, 6))
queue_depth_iops.plot(kind='bar', color='lightgoldenrodyellow')
plt.title('Average IOPS by Queue Depth')
plt.xlabel('Queue Depth')
plt.ylabel('Average IOPS')
plt.xt

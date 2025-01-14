| Access Size | Read/Write Ratio   | Queue Depth | IOPS    | Latency (ms) | Throughput (MB/s) |
|-------------|--------------------|-------------|---------|--------------|-------------------|
| 4K          | 100% Read          | 1           | 10,617  | 0.092        | N/A               |
| 4K          | 100% Write         | 1           | 9,872   | 0.105        | 38.55             |
| 4K          | 50% Read/50% Write | 4           | 12,456  | 0.089        | 48.85             |
| 16K         | 100% Read          | 4           | 9,250   | 0.110        | N/A               |
| 16K         | 70% Read/30% Write | 16          | 11,489  | 0.093        | 179.83            |
| 32K         | 100% Write         | 16          | 8,743   | 0.120        | 273.22            |
| 32K         | 50% Read/50% Write | 32          | 7,231   | 0.132        | 225.06            |
| 128K        | 100% Read          | 32          | 6,845   | 0.145        | N/A               |
| 128K        | 100% Write         | 64          | 5,938   | 0.170        | 742.25            |
| 128K        | 70% Read/30% Write | 128         | 6,250   | 0.155        | 781.25            |
| 4K          | 100% Read          | 512         | 10,450  | 0.095        | N/A               |
| 4K          | 100% Write         | 512         | 8,912   | 0.115        | 34.82             |
| 16K         | 100% Read          | 1024        | 8,957   | 0.112        | N/A               |
| 16K         | 50% Read/50% Write | 1024        | 7,811   | 0.134        | 121.01            |
| 32K         | 100% Write         | 512         | 9,012   | 0.110        | 288.38            |
| 32K         | 50% Read/50% Write | 1024        | 7,482   | 0.125        | 239.06            |
| 128K        | 70% Read/30% Write | 512         | 5,678   | 0.158        | 709.75            |
| 128K        | 100% Write         | 1024        | 4,923   | 0.182        | 615.38            |
| 4K          | 50% Read/50% Write | 256         | 10,230  | 0.097        | 39.96             |
| 16K         | 70% Read/30% Write | 256         | 9,820   | 0.108        | 153.12            |

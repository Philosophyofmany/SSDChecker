import subprocess
import json
import os
import csv

class TestResult:
    def __init__(self, access_size, read_write_ratio, queue_depth, iops=0.0, latency=0.0):
        self.access_size = access_size
        self.read_write_ratio = read_write_ratio
        self.queue_depth = queue_depth
        self.iops = iops
        self.latency = latency

def run_fio_test(command, output_file_path, result):
    """Runs the FIO command and extracts results from the output JSON."""
    # Run the command and redirect output to a file
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run the command: {e}")
        return

    # Read the output from the file
    if not os.path.exists(output_file_path):
        print("Failed to open output file!")
        return

    with open(output_file_path, 'r') as file:
        try:
            json_data = json.load(file)
        except json.JSONDecodeError:
            print("Failed to decode JSON from output file!")
            return

    # Extract relevant information from JSON
    if "jobs" in json_data and isinstance(json_data["jobs"], list):
        for job in json_data["jobs"]:
            if "read" in job:
                result.iops = job["read"].get("iops", 0.0)
                result.latency = job["read"].get("latency", {}).get("mean", 0.0)
            elif "write" in job:
                # Capture write IOPS and latency
                result.iops = job["write"].get("iops", 0.0)
                result.latency = job["write"].get("latency", {}).get("mean", 0.0)
    else:
        print("Invalid JSON format!")

def print_table(results, test_type):
    """Prints the results in a formatted table."""
    if test_type == "Read":
        print(f"\n{test_type} Test Results:")
        print("Access Size | Queue Depth | IOPS      | Latency (ms)")
        print("----------------------------------------------------")
        for res in results:
            print(f"{res.access_size}        | {res.queue_depth}          | {res.iops} | {res.latency:.2f}")
    elif test_type == "Write":
        print(f"\n{test_type} Test Results:")
        print("Access Size | Read/Write Ratio   | Queue Depth | IOPS      | Latency (ms) | Throughput (MB/s)")
        print("---------------------------------------------------------------")
        for res in results:
            throughput = res.iops * (int(res.access_size[:-1]) / 1024 / 1024) if 'K' in res.access_size else 0
            print(f"{res.access_size}        | {res.read_write_ratio} | {res.queue_depth}          | {res.iops} | {res.latency:.2f} | {throughput:.2f}")

def log_results_to_csv(results, test_type):
    """Logs the results to a CSV file."""
    filename = f"{test_type.lower()}_test_results.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        if test_type == "Read":
            writer.writerow(["Access Size", "Queue Depth", "IOPS", "Latency (ms)"])
            for res in results:
                writer.writerow([res.access_size, res.queue_depth, res.iops, res.latency])
        elif test_type == "Write":
            writer.writerow(["Access Size", "Read/Write Ratio", "Queue Depth", "IOPS", "Latency (ms)", "Throughput (MB/s)"])
            for res in results:
                throughput = res.iops * (int(res.access_size[:-1]) / 1024 / 1024) if 'K' in res.access_size else 0
                writer.writerow([res.access_size, res.read_write_ratio, res.queue_depth, res.iops, res.latency, throughput])

def run_read_tests(results):
    """Runs read tests with various configurations."""
    access_sizes = ["4K", "16K", "32K", "128K"]
    queue_depths = [1, 4, 16, 32, 64, 128, 256, 512, 1024]  # Expanded queue depths

    for size in access_sizes:
        for depth in queue_depths:
            result = TestResult(size, "100% Read", depth)
            output_file_path = "read_test_output.json"

            command = f"fio --name=test --ioengine=libaio --rw=randread --bs={size} --size=1G --numjobs=1 --runtime=10s --time_based --iodepth={depth} --filename=/dev/nvme0n1p3 --output-format=json > {output_file_path}"

            print(f"Running command: {command}")
            run_fio_test(command, output_file_path, result)
            results.append(result)

            # Print the current result immediately
            print_table(results, "Read")

def run_write_tests(results):
    """Runs write tests with various configurations."""
    access_sizes = ["4K", "16K", "32K", "128K"]
    read_write_ratios = ["100% Write", "50% Read/50% Write", "70% Read/30% Write"]
    queue_depths = [1, 4, 16, 32, 64, 128, 256, 512, 1024]  # Expanded queue depths

    for size in access_sizes:
        for ratio in read_write_ratios:
            for depth in queue_depths:
                result = TestResult(size, ratio, depth)
                output_file_path = "write_test_output.json"

                rw_command = "randwrite" if ratio == "100% Write" else "randrw"
                allow_mounted_write = " --allow_mounted_write" if ratio != "100% Write" else ""

                command = f"fio --name=test --ioengine=libaio --rw={rw_command}{allow_mounted_write} --bs={size} --size=1G --numjobs=1 --runtime=60s --time_based --iodepth={depth} --filename=/dev/nvme0n1p3 --output-format=json > {output_file_path}"

                print(f"Running command: {command}")
                run_fio_test(command, output_file_path, result)
                results.append(result)

                # Print the current result immediately
                print_table(results, "Write")

def main():
    read_results = []
    write_results = []

    # Run read tests
    print("Running read tests...\n")
    run_read_tests(read_results)
    log_results_to_csv(read_results, "Read")  # Log read results

    # Run write tests
    print("Running write tests...\n")
    run_write_tests(write_results)
    log_results_to_csv(write_results, "Write")  # Log write results

if __name__ == "__main__":
    main()

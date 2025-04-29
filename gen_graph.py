import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the domain webpage counts CSV
domain_counts_df = pd.read_csv('/home/marialuiza/Documents/faculdade/ir/webCrawler/data_100/analysis_results/domain_webpage_counts.csv')

# Calculate the total number of unique domains
total_unique_domains = domain_counts_df['Domain'].nunique()
print(f"Total Number of Unique Domains: {total_unique_domains}")

# Calculate descriptive statistics for the number of webpages per domain
webpages_per_domain_stats = domain_counts_df['Webpages'].describe()
print("Size Distribution (Number of Webpages per Domain):")
print(webpages_per_domain_stats)

# Load the webpage token counts CSV
webpage_tokens_df = pd.read_csv('/home/marialuiza/Documents/faculdade/ir/webCrawler/data_100/analysis_results/webpage_token_counts.csv')

# Calculate descriptive statistics for the number of tokens per webpage
tokens_per_webpage_stats = webpage_tokens_df['Tokens'].describe()
print("Size Distribution (Number of Tokens per Webpage):")
print(tokens_per_webpage_stats)

# Generate a summary report
report = f"""
Characterization of Crawled Corpus:

1. Total Number of Unique Domains: {total_unique_domains}

2. Size Distribution (Number of Webpages per Domain):
{webpages_per_domain_stats}

3. Size Distribution (Number of Tokens per Webpage):
{tokens_per_webpage_stats}
"""

# Save the report to a text file
with open('/home/marialuiza/Documents/faculdade/ir/webCrawler/data_100/analysis_results/corpus_characterization.txt', 'w') as f:
    f.write(report)

print("Report saved to corpus_characterization.txt")

# Define the thread counts and corresponding file paths
thread_counts = [25, 50, 100]
file_paths = [
    '/home/marialuiza/Documents/faculdade/ir/webCrawler/result_25/download_rate25.csv',
    '/home/marialuiza/Documents/faculdade/ir/webCrawler/result_50/download_rate50.csv',
    '/home/marialuiza/Documents/faculdade/ir/webCrawler/data_100/download_rate100.csv',
    '/home/marialuiza/Documents/faculdade/ir/webCrawler/result_150/download_rate150.csv',
]

for file in file_paths:
    # Load the CSV file
    data = pd.read_csv(file)

    # Convert the Timestamp column to datetime format
    data["Timestamp"] = pd.to_datetime(data["Timestamp"])

    # Calculate the total number of pages crawled
    total_pages_crawled = data["Pages Crawled in Last Interval"].sum()

    # Calculate the total elapsed time in seconds
    start_time = data["Timestamp"].iloc[0]
    end_time = data["Timestamp"].iloc[-1]
    elapsed_time = (end_time - start_time).total_seconds()

    # Calculate the average pages crawled per second
    average_pages_per_second = total_pages_crawled / elapsed_time if elapsed_time > 0 else 0

    # Print the result
    print(f"File: {file}")
    print(f"Total Pages Crawled: {total_pages_crawled}")
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")
    print(f"Average Pages Crawled Per Second: {average_pages_per_second:.2f}")


# Initialize a dictionary to store data for each thread count
# data_by_threads = {}

# max_length = 0

# # Loop through each file and load the data
# for threads, file_path in zip(thread_counts, file_paths):
#     # Load the CSV file
#     data = pd.read_csv(file_path)

#     # Convert the Timestamp column to datetime format
#     data["Timestamp"] = pd.to_datetime(data["Timestamp"])

#     # Normalize the time to start at 0
#     data["Normalized Time"] = (data["Timestamp"] - data["Timestamp"].iloc[0]).dt.total_seconds()

#     data = data.drop(columns=["Timestamp"])  # Drop the original Timestamp column
#     data = data.drop(columns=["Download Rate (pages/second)"])  # Drop the Download Rate column
#     data = data.rename(columns={"Pages Crawled in Last Interval": "Pages Crawled Per Second"})
#     data["Normalized Time"] = np.linspace(0, len(data) - 1, num=len(data))
#     if len(data) > max_length:
#         max_length = len(data)

#     # Store the data in the dictionary
#     data_by_threads[threads] = data

# # Fill with 0 so that all datasets have the same length
# for threads, data in data_by_threads.items():
#     if len(data) < max_length:
#         # Create a DataFrame with the same length as the longest one
#         additional_rows = pd.DataFrame({
#             "Normalized Time": np.linspace(max_length - len(data) + 1, max_length + 1, num=max_length-len(data)),
#             "Pages Crawled Per Second": [0] * (max_length - len(data))
#         })
#         # Append the additional rows to the original data
#         data_by_threads[threads] = pd.concat([data, additional_rows], ignore_index=True)

# # Group time intervals into 1-minute intervals
# for threads, data in data_by_threads.items():
#     # Group by 1-minute intervals
#     data["Time Interval"] = (data["Normalized Time"] // 60).astype(int)
#     # Calculate the mean for each interval
#     data = data.groupby("Time Interval").mean().reset_index()
#     # Normalize the time again
#     data["Normalized Time"] = np.linspace(0, len(data) - 1, num=len(data))
#     # Store the processed data back
#     data_by_threads[threads] = data


# # Create a bar plot
# plt.figure(figsize=(14, 8))

# # Plot bars for each thread count
# for threads, data in data_by_threads.items():
#     plt.bar(
#         data["Time Interval"],
#         data["Pages Crawled Per Second"],
#         label=f"{threads} Threads",
#     )

# # Add labels, title, legend, and grid
# plt.title("Pages Crawled Per Second Over Normalized Time by Thread Count", fontsize=16)
# plt.xlabel("Normalized Time (seconds)", fontsize=14)
# plt.ylabel("Pages Crawled Per Second", fontsize=14)
# plt.legend(title="Thread Count", fontsize=12)
# plt.grid(axis="y", linestyle="--", alpha=0.7)

# # Save the plot to a file
# plt.tight_layout()
# plt.savefig('/home/marialuiza/Documents/faculdade/ir/webCrawler/pages_crawled_bar_comparison_normalized.png', format='png')

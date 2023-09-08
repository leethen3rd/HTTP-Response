import requests
import csv


def get_initial_response(url):
    try:
        response = requests.get(url, timeout=10, allow_redirects=False)
        return response.status_code, response.url
    except requests.RequestException:
        return None, None


def get_final_response(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code, response.url
    except requests.RequestException:
        return None, None


def ensure_http(url):
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url


def main():
    file_name = "urls.txt"  # Input file name
    output_csv = "results.csv"  # Output CSV file name

    with open(file_name, 'r') as file:
        urls = [ensure_http(line.strip()) for line in file]

    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["URL", "Initial Response Code",
                            "Final Response Code", "Final URL"])

        for url in urls:
            initial_code, initial_url = get_initial_response(url)
            if initial_code is None:
                initial_code = "N/A"
                final_code = "N/A"
                final_url = "N/A"
            else:
                final_code, final_url = get_final_response(
                    url) if 300 <= initial_code < 400 else (initial_code, initial_url)

            csv_writer.writerow([url, initial_code, final_code, final_url])
            print(f"Processed: {url}")

    print(f"Results saved to {output_csv}")


if __name__ == "__main__":
    main()

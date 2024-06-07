# Unique Account Mbox Extractor

This script will extract unique primary domains from an .mbox file and allows you to customize the verbage for identifying "new" account emails

## Requirements

- Python 3.6 or higher
- tqdm (for progress bar, optional)

## Installation

1. **Clone the repository**
2. **Terminal into the directory and create and activate a virtual environment:**
    ```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
    ```

3. **Install the required packages:**
    ```bash
    pip install tqdm
    ```

## Usage

1. **Place your `.mbox` file in the project directory or note its location**

2. **Run the script:**
    ```bash
    python email_account_extractor.py
    ```

3. **Follow the on-screen prompts:**
    - It will ask if you want to use the default regex pattern for identifying account-related emails.
    - If you choose to use your own patterns, you can enter them separated by commas.
    - The script will check for `.mbox` files in the current directory and prompt you to confirm if you want to use the found file.
    - If no `.mbox` file is found, you will be prompted to enter the path to your `.mbox` file.

4. **Output:**
    - The script will process the emails and extract unique primary domains.
    - The unique primary domains will be saved to a file named `unique_primary_domains.txt` in the project directory.
5. **Test:**
    - Feel free to test with the included .mbox sample file


## Contributing

Feel free to open issues or submit pull requests if you have any suggestions or improvements.

## License

This project is licensed under the MIT License.

---

Happy extracting! 🎉

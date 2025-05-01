# DeepMiner-TESS – A Deep Miner for Multi-Cadence Data from the TESS Mission

**DeepMiner-TESS** is a Python tool designed to deeply mine multi-cadence light curve data from the TESS mission using the `lightkurve` package.  
It provides an interactive, terminal-based interface for selecting TIC targets and configuring download options, including optional sector filtering.

---

## ⚙️ Requirements

Make sure you have Python 3.7 or higher installed.  
Required packages are automatically checked and installed by the script, but you can also install them manually with:

```bash
pip install lightkurve numpy pandas inquirer
```

---

## 📁 Input File Structure

The script expects a `.txt` file in the same directory, with the following format:

1. Lines specifying the `author` and `exptime` separated by `;`
2. A line containing only `===` to separate configuration from TIC IDs
3. A list of TIC IDs (one per line)

### 📄 Example:
```txt
QLP;200
QLP;600
QLP;1800
SPOC;20
SPOC;120
TESS-SPOC;600
TESS-SPOC;1800
===
21835438
307075270
```

---

## 🚀 How to Use

1. Clone this repository or download the script:

```bash
git clone https://github.com/your-username/deepminer-tess.git
cd deepminer-tess
```

2. Run the script:

```bash
python downloader.py
```

3. Follow the interactive terminal instructions:

### 🧭 Step-by-Step:
- Select the `.txt` file containing TICs and configuration.
- Specify the folder where files should be saved (press Enter to use the default: `dat`).
- When prompted:  
  **"Do you want to limit the sector number?"**  
  - Press Enter to download from **all sectors**.
  - Select "Yes" and enter a value (e.g., `10`) to download only sectors `<= 10`.
- The script will download all available light curves for the selected TICs and configurations.
- Files are saved in `.dat` format inside the specified folder.

---

## 📌 Additional Notes

- The Lightkurve cache is automatically cleared every 100 TICs.
- Already downloaded files are skipped if a matching file name exists.
- Each `.dat` file contains two columns: `Time` and `Flux`.

---

## 🙌 Citation

If this tool was helpful or made your research easier, please consider citing this repository or mentioning it in your acknowledgments.

---

## 👨‍💻 Author

Developed by [Your Name] — built for automating light curve collection in astrophysical research.  
Contributions, suggestions, and issues are welcome!

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
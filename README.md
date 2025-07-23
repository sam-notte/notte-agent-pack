# Notte Price Comparison Script

This script uses the [Notte SDK](https://github.com/nottelabs/notte) to automate price comparisons for a given product across multiple e-commerce websites using LLM agents. It is fully environment-agnostic and designed for repeatable, cross-platform use.

---

## Features

- **Environment-agnostic:** All config via `.env`
- **Agentic automation:** Uses Notte agents to navigate, search, and extract data
- **Multi-site compatible:** Works across any three target URLs
- **Error-resilient:** Handles popups, region prompts, missing data
- **Structured output:** Prints raw agent responses + summary table

---

## Setup

### 1. Install Dependencies

```bash
pip install notte-sdk python-dotenv
```

### 2. Create a `.env` File

```env
NOTTE_API_KEY=your-api-key
PRODUCT_NAME=iPhone 15
SITE_1=https://www.apple.com/
SITE_2=https://www.amazon.com/
SITE_3=https://www.bestbuy.com/
REGION=United States
```

> `REGION` is optional and defaults to `United States` if not set.

---

## Usage

Run the script from the terminal:

```bash
python script_name.py
```

Replace `script_name.py` with your actual filename.

---

## Output

### Per-Site Agent Response

```text
---
Site: apple.com
Title: iPhone 15 Pro
Price: $999
Discount: None
---
```

### Error Example

```text
---
Site: bestbuy.com
Error: Timed out waiting for element
---
```

### Summary Table

```text
Site            Title                                   Price           Discount             Steps
----------------------------------------------------------------------------------------------------
apple.com       iPhone 15 Pro                           $999            None                 12
amazon.com      iPhone 15 Pro (Unlocked)                $989            Prime Deal -$10      14
bestbuy.com     Error                                   -               -                    0
```

---

## Requirements

- Python 3.8+
- Notte SDK API key from [console.notte.cc](https://console.notte.cc/)
- Any terminal environment

---

## Notes

- Script halts early if required environment variables are missing.
- Agent avoids sponsored links, overlays, and unrelated content.
- Retry logic handled by Notte’s internal mechanism.


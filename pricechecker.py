import os
from dotenv import load_dotenv
from notte import NotteClient

def main():
    # Load environment variables
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

    api_key = os.getenv("NOTTE_API_KEY")
    product_name = os.getenv("PRODUCT_NAME")
    site_1 = os.getenv("SITE_1")
    site_2 = os.getenv("SITE_2")
    site_3 = os.getenv("SITE_3")
    region = os.getenv("REGION", "United States")

    # Basic validation
    missing = []
    if not api_key:
        missing.append("NOTTE_API_KEY")
    if not product_name:
        missing.append("PRODUCT_NAME")
    if not site_1:
        missing.append("SITE_1")
    if not site_2:
        missing.append("SITE_2")
    if not site_3:
        missing.append("SITE_3")
    if missing:
        print(f"❌ Please set the following variables in your .env file: {', '.join(missing)}")
        return

    task = f"""
Compare the price and key details for the product \"{product_name}\" across the following websites:

1. {site_1}
2. {site_2}
3. {site_3}

Instructions:
- On each site, search for the product if not directly linked.
- If multiple results appear, click into the most relevant or top-listed product **before extracting any data**.
- Extract only visible, user-facing information from the product **detail page**, including:
  - Title
  - Price
  - Discount or promo (if shown)
- If you cannot find the exact product (e.g., M2), extract the closest available version and note the difference.
- If you cannot extract information from a site after several attempts, skip it and return results for the other sites.
- If a site asks for a region or delivery location, set it to \"{region}\".
- Do not use element IDs, CSS selectors, or hidden content. Treat this like a human browsing manually.
- If you encounter a cookie banner, popup, or overlay on any site, always close or accept it before searching or clicking any buttons. If a button is not clickable, wait a few seconds, close any overlays, and try again.

Repeat this full process for **all three** sites. If you cannot complete all three, return partial results and note any issues.

Return the results in this format:

---
Site: [site name]
Title: ...
Price: ...
Discount: ...  # or \"None\"
---
"""

    # Run the agent
    client = NotteClient(api_key=api_key)
    agent = client.Agent(headless=True, max_steps=60)
    response = agent.run(task=task)

    # Output
    if response.answer:
        print("\nAgent Response:\n")
        print(response.answer.strip())
    else:
        print("No answer returned by the agent. The agent may have failed, timed out, or hit the max steps limit.")
        # Optionally print more debug info if available
        if hasattr(response, "error"):
            print("Agent error:", response.error)
        if hasattr(response, "status"):
            print("Agent status:", response.status)

if __name__ == "__main__":
    main()
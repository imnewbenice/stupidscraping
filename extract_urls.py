import asyncio
from pyppeteer import launch

async def main():
    browser = None
    try:
        # Launch the browser
        browser = await launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-zygote",
                "--single-process",
            ]
        )
        page = await browser.newPage()
        await page.setDefaultNavigationTimeout(60000)  # 60 seconds timeout

        # Navigate to the TOC page
        toc_url = "https://www.boardpolicyonline.com/bl/?b=agua_fria#&&hs=TOCView"
        print("Navigating to the TOC page...")
        await page.goto(toc_url, waitUntil='networkidle2')  # Wait for network to be idle

        # Wait for the specific element (or ensure the page has loaded)
        try:
            await page.waitForSelector("div[style*='height: auto; overflow: visible;']", timeout=30000)
            print("Target divs are available!")
        except Exception as e:
            print(f"Error waiting for divs: {e}")
            return

        # Extract URLs from the specific div structure
        urls = await page.evaluate('''
            () => {
                const elements = document.querySelectorAll("div[style*='height: auto; overflow: visible;'] a");
                return Array.from(elements).map(a => a.getAttribute('href')).filter(url => url !== null);
            }
        ''')

        print(f"Extracted {len(urls)} URLs.")
        for url in urls[:10]:  # Print the first 10 URLs for debugging
            print(url)

        # Save URLs to a file
        with open("urls.txt", "w") as f:
            for url in urls:
                f.write(url + "\n")
        print("URLs saved to 'urls.txt'.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if browser:
            await browser.close()

# Run the script
asyncio.run(main())

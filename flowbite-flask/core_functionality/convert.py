import asyncio
from playwright.async_api import async_playwright

async def convert_html_to_pdf(input_html, output_pdf):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load local HTML file content
        with open(input_html, 'r', encoding='utf-8') as f:
            content = f.read()

        # Set HTML content
        await page.set_content(content, wait_until="networkidle")
        
        # Optional: Ensure proper rendering (fonts, remote assets)
        await page.wait_for_timeout(1000)

        # Set viewport for proper layout rendering
        await page.set_viewport_size({"width": 1200, "height": 1600})

        # Export to PDF
        await page.pdf(
            path=output_pdf,
            format="A4",
            landscape=False,
            print_background=True,
            margin={"top": "20px", "bottom": "20px", "left": "20px", "right": "20px"}
        )

        await browser.close()

if __name__ == "__main__":
    asyncio.run(convert_html_to_pdf("core_functionality/sample.html", "generated_resume.pdf"))

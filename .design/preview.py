"""Preview README.md roughly as GitHub shows it. Usage: python3 .design/preview.py [dark|light] (needs Playwright)."""
import asyncio, pathlib, re, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
mode = (sys.argv[1:] or ["dark"])[0]
bg, border = ("#0d1117", "#30363d") if mode == "dark" else ("#ffffff", "#d0d7de")


async def main():
    md = (ROOT / "README.md").read_text()
    md = re.sub(r'src="(?!http)', f'src="{ROOT.as_uri()}/', md)
    md = md.replace("<p ", "<p style='margin:0 0 16px' ")
    page = (f'<html><body style="margin:0;background:{bg}"><div style="width:830px;margin:24px auto;border:1px solid {border};'
            f'border-radius:6px;padding:24px;background:{bg}">{md}</div></body></html>')
    out = ROOT / ".design" / "preview"
    out.mkdir(exist_ok=True)
    (out / "_page.html").write_text(page)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 880, "height": 900})
        await pg.goto((out / "_page.html").as_uri())
        await pg.wait_for_timeout(1500)
        await pg.screenshot(path=str(out / f"page-{mode}.png"), full_page=True)
        await b.close()
    print(out / f"page-{mode}.png")

asyncio.run(main())

"""Render assets to PNG for checking (needs Playwright). Usage: python3 preview.py [name.svg ...] | --page"""
import sys, asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / ".design" / "preview"


async def main(args):
    OUT.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        if args == ["--page"]:
            import re
            md = (ROOT / "README.md").read_text()
            md = re.sub(r'src="(?!http)', f'src="{ROOT.as_uri()}/', md)
            html = ('<html><body style="margin:0;background:#fff;font-family:Helvetica"><div style="width:830px;margin:24px auto;'
                    'border:1px solid #d0d7de;border-radius:6px;padding:24px">' + md.replace("<p ", "<p style='margin:0 0 16px' ") + "</div></body></html>")
            f = OUT / "_page.html"
            f.write_text(html)
            pg = await b.new_page(viewport={"width": 900, "height": 800})
            await pg.goto(f.as_uri())
            await pg.wait_for_timeout(1500)
            await pg.screenshot(path=str(OUT / "page.png"), full_page=True)
        else:
            pg = await b.new_page(device_scale_factor=1)
            names = args or [x.name for x in sorted((ROOT / "assets").glob("*.svg"))]
            for n in names:
                src = (ROOT / "assets" / n)
                if not src.exists():
                    src = ROOT / "profile" / n
                f = OUT / "_one.html"
                f.write_text(f'<html><body style="margin:0;background:#fff"><img id="i" src="{src.as_uri()}"></body></html>')
                await pg.goto(f.as_uri())
                await pg.wait_for_timeout(300)
                await (await pg.query_selector("#i")).screenshot(path=str(OUT / (src.stem + ".png")))
        await b.close()


asyncio.run(main(sys.argv[1:]))

import asyncio 
from playwright.async_api import async_playwright

async def raspar_vagas(termo_busca: str) -> list[dict]:
 async with async_playwright()as p:
   browser = await p.chromium.launch(headless=True)
   page = await browser.new_page()

   url = f"https://exemplo-vagas.com/jobs?q={termo_busca}" 
   await page.goto(url)
   await page.wait_for_selector(".card-vaga")

   elementos = await page.locator(".card-vaga").all()
   vagas = [] 

   for elem in elementos[:5]:
    titulo = await elem.locator(".titulo-cargo").text_content()
    empresa = await elem.locator(".nome-empresa").text_content()
    link = await elem.locator("a.link-vaga").get_attribute("href")
    
    vagas.append({
        "titulo": titulo.strip() if titulo else "Cargo não informado",
        "empresa": empresa.strip() if empresa else "Confidencial",
        "link": link if link else "https://exemplo-vagas.com"
    })

    await browser.close()
    return vagas

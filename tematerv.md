# Tématerv - Bódi Martin

  
  
  

## Személyes adatok

  

**Név:** Bódi Martin

  

**Neptun:** Z9WTNS

  

**E-mail:** h150714@stud.u-szeged.hu

  

**Szak:** Programtervező Informatikus BSc nappali

  

**Végzés várható ideje:** 2024. nyár

  

## A szakdolgozat tárgya

  
Egy olyan multiplatform, konzoli alkalmazás létrehozása, amely a GPT API segítségével létrehoz egy olyan másolatot a kódból amely követi a clean code irányelveit. Továbbá a lehetőség szerint maximalizálva annak az esélyét, hogy nem változtatja meg a kód működését, nem rontja el függőségeit. 

Funkciók:
- A felhasználó futtathatja az alkalmazást akár egész könyvtárra, vagy csak egyetlen egy fájlra is.
- Az eredmény az általa megadott, vagy alapesetben egy implicit létrehozott mappába kerül.
- Emellett kérheti azt is, hogy az eredmény csak a konzolon jelenjen meg.
- A mappában előforduló, tisztítani nem kívánt fájlokat van lehetőség átmásolni, ezzel megkönnyítve a létrehozott kód tesztelését.
- A használathoz szükséges, hogy a felhasználó rendelkezzen GPT API kredittel és konfigurálja az alkalmazást
	- Az új felhasználók 18$-nyi ingyen kreditet kapnak, egyébként vásárolni a GPT API oldalán lehet
	- konfigurációnál meg kell adni az api_key-t és az organizáció id-t
- A használható modelleket a models.json-ben bővítheti, módosíthatja, ha szeretné
- Az éppen használni kívánt modellt megadhatja kapcsoló segítségével, de a config.json fájlban megadhatja az alapértelmezésként használt modellt is.
- A különböző modelleknek különböző limitációi vannak, illetve az árazásuk is különbözhet, akár csak az eredmény.
- A működés megtartására törekvés: különböző meta információk és a megfelelő modell instrukció használatával.
- Az integritás megtartására törekvés (több fájl esetén): az átnevezések és egyéb integritást rontó módosítások követésével.

Nehézségek:
- GPT és egyéb LLM-ek esetében is nem létezik még jó megoldás arra, hogy hogyan tiltsuk meg teljesen, hogy ne adjon teljesen hibás, téves, pontatlan eredményeket.
	- Éppen ezért előfordulhat, hogy a megtisztított fájl egyből még nem lesz használható és igényel valamennyi idő ráfordítást
- Hasonlóan, nem nagyon lehet tökéletesen korlátozni a kimenet formátumát, hogy ne módosítson a kód működésén, hogy ne romoljon el teljesen a működés és hogy ne rontson el függőségeket.
- Az API calloknak limitált a bemeneti, kimeneti token száma, percenként és naponként a API hívások száma 

## Használni kívánt technológiák

 - Python 3
 - PIP
 - PIP-es függvény könyvtárak
 - GPT API különböző modellei (Chat Completion): 
	 -  gpt-3.5-turbo
	 - gpt-4
	 - gpt-3.5-16k
	 - gpt-4-32k
	 - ...
- PyPi



## Tervezett ütemezés



-  **2021. szeptember:**
	- az alkalmazás fejlesztésének elkezdése 
	- nehézségek felmérése
-  **2021. október:**
	- elérni, hogy az alkalmazás már korlátozott mértékben működő képes legyen:
		- lehessen már futtatni code-ra és azt tisztítsa meg (még nem kell hogy jó eredménye legyen)
	- API limitációk, hibák kezelésének a megkezdése
-  **2021. november:**
	- API limitációk, hibák kezelésének a befejezése
	- A működés javítása az instrukció optimalizálásával, esetleg plussz metainformációkkal
	- A fájl feldarabolás implementálásának a megkezdése
-  **2021. december:**
	- Fájl feldarabolás implementálásának a befejezése
	- Fájlok közti szinkronizáció megkezdése
-  **2022. január:**
	- Szinkronizáció befejezése
	- Esetleges hibajavítás, működés javítás
-  **2022. február:**
	- Szakdolgozat írása
	- Esetleges hibajavítás, működés javítás
-  **2022. március:** 
	- Szakdolgozat írása
	- Esetleges hibajavítás, működés javítás
-  **2022. április:**
	- Esetleges hibajavítás, működés javítás
	- Szakdolgozat befejezése

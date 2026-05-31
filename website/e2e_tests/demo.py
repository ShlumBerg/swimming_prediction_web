import pytest
from playwright.sync_api import sync_playwright,Browser,Page,expect
from main import BASE_URL_DEFAULT
ZOOM_SCALE=1.6
#Настроить размер viewport для playwright (через встроеную в него функцию)
@pytest.fixture(scope="function")
def browser_context_args(browser_context_args,viewport):
    return {
        **browser_context_args,
        "viewport": viewport,
        "record_video_size": viewport #Разрешение видео = разрешению экрана
        }


@pytest.mark.parametrize("viewport",[
    pytest.param({"width":393,"height":852},id="xs"), #extra small (iphone 14 iOS 18.6 vertical)
    pytest.param({"width":712,"height":1138},id="sm"), #small (galaxy tab s9 android 14 vetrical)
    pytest.param({"width":820,"height":1180},id="md"), #medium (iPad 10 iPadOS 18.6 vertical)
    pytest.param({"width":1024,"height":600},id="lg"), #large (Nest Hub horizontal)
    pytest.param({"width":1280,"height":800},id="xl"), #extra large (Nest Hub Max horizontal)
    pytest.param({"width":1920,"height":1080},id="xxl"), #extra extra large (1080p television horizontal)
])
class TestForDemoVideo:
    def test_create_demo_video(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        page.goto(url) #Перейти по ссылке
        #Приблизить страницу
        page.evaluate(f"document.documentElement.style.zoom = '{int(ZOOM_SCALE*100)}%'")
        page.wait_for_timeout(50)
        page.wait_for_timeout(1000) #Дождаться полной загрузки страницы
        page.wait_for_timeout(5000) #Подождать перед переходом на следующую страницу
        
        
        #Перейти на страницу прогноза заплыва
        if page.viewport_size['width']<1200:  #Если размер экрана по горизонтали маленький, сначала нажать на кнопку для разворачивания других кнопок
            page.locator("button.navbar-toggler").first.click()
            page.wait_for_timeout(600)  # Ждем анимацию
        page.locator("#navbarContent a").nth(1).click() #Нажать на кнопку для страницы прогноза заплыва
        #Приблизить страницу
        page.evaluate(f"document.documentElement.style.zoom = '{int(ZOOM_SCALE*100)}%'")
        page.wait_for_timeout(1000) #Дождаться полной загрузки страницы
        
        #Ввод данных о заплыве
        page.locator("#selectStyle").focus()
        page.wait_for_timeout(300)
        page.keyboard.press("ArrowDown")
        page.wait_for_timeout(300)
        page.locator("#selectDistance").focus()
        page.wait_for_timeout(300)
        page.keyboard.press("1")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(300)
        page.locator("#selectSex").focus()
        page.wait_for_timeout(300)
        page.keyboard.press("ArrowDown")
        page.wait_for_timeout(300)
        page.locator("#selectPhase").focus()
        page.wait_for_timeout(300)
        page.keyboard.press("ArrowDown")
        page.wait_for_timeout(300)
        page.locator("#selectPoolLength").focus()
        page.wait_for_timeout(300)
        page.keyboard.press("5")
        page.wait_for_timeout(300)
        page.locator("#inputDatetime").focus()
        page.wait_for_timeout(300)
        page.keyboard.press("1")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(150)
        page.keyboard.press("6")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("6")
        page.wait_for_timeout(150)
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(150)
        page.keyboard.press("1")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(150)
        page.keyboard.press("ArrowLeft")
        page.wait_for_timeout(150)
        page.keyboard.press("5")
        page.wait_for_timeout(300)
        page.locator("#selectHostCountry + .ts-wrapper input").focus()
        page.wait_for_timeout(1000)
        page.locator("#selectHostCountry + .ts-wrapper .ts-dropdown .option", has_text="Австралия").click()
        page.keyboard.press("Escape")  #Закрыть томселект
        page.wait_for_timeout(300) #Подождать после ввода поля
        page.evaluate("window.scrollBy({ top: 900, behavior: 'smooth' })") #Прокрутить вниз страницу на 900px
        page.wait_for_timeout(500)  #Ждем анимацию
        page.locator("#selectSwimmer4 + .ts-wrapper input").focus()
        page.wait_for_timeout(1000) #Ожидание фильтра
        page.locator("#selectSwimmer4 + .ts-wrapper .ts-dropdown .option", has_text="LIENDO Josh").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(300) #Подождать пока томселект закроется
        page.locator("#selectSwimmer5 + .ts-wrapper input").focus()
        page.wait_for_timeout(150)
        page.keyboard.press("C")
        page.wait_for_timeout(150)
        page.keyboard.press("H")
        page.wait_for_timeout(150)
        page.keyboard.press("A")
        page.wait_for_timeout(150)
        page.keyboard.press("L")
        page.wait_for_timeout(150)
        page.keyboard.press("M")
        page.wait_for_timeout(1000) #Ожидание фильтра
        page.locator("#selectSwimmer5 + .ts-wrapper .ts-dropdown .option", has_text="CHALMERS Kyle").click()
        page.keyboard.press("Escape")  #Закрыть томселект
        page.wait_for_timeout(300) #Подождать пока томселект закроется
        
        page.get_by_text("Предсказать",exact=True).first.click() #Нажать по кнопке предсказания
        page.wait_for_timeout(400)  #Ждем анимацию
        page.evaluate("window.scrollBy({ top: 500, behavior: 'smooth' })") #Прокрутить вниз страницу на 500px
        page.wait_for_timeout(7000)  #Показать результаты прогнозов
        
        #Показать графики
        page.locator(f'div#swimmer4Results div.card-body div#swimmerDataTable > div:nth-child(4) > button:nth-child(1)').click()
        page.wait_for_timeout(3000)
        page.wait_for_timeout(3000)
        page.evaluate("""
            document.querySelector('.modal.show').scrollBy({ top: 600, behavior: 'smooth' })
        """)#Прокрутить вниз страницу на 600px
        page.wait_for_timeout(2000)
        page.evaluate("""
            document.querySelector('.modal.show').scrollBy({ top: -600, behavior: 'smooth' })
        """)#Прокрутить вверх страницу на 600px
        page.wait_for_timeout(1300)
        page.locator("div.modal-header button.btn-close").click()
        page.wait_for_timeout(900)
        page.locator(f'div#swimmer5Results div.card-body div#swimmerDataTable > div:nth-child(4) > button:nth-child(1)').click()
        page.wait_for_timeout(3000)
        page.evaluate("""
            document.querySelector('.modal.show').scrollBy({ top: 600, behavior: 'smooth' })
        """)#Прокрутить вниз страницу на 600px
        page.wait_for_timeout(2000)
        page.evaluate("""
            document.querySelector('.modal.show').scrollBy({ top: 600, behavior: 'smooth' })
        """)
        #Прокрутить вниз страницу на 600px
        page.wait_for_timeout(2000)
        page.evaluate("""
            document.querySelector('.modal.show').scrollBy({ top: -1200, behavior: 'smooth' })
        """) #Прокрутить вверх страницу на 1200px
        page.wait_for_timeout(1300)
        page.locator("div.modal-header button.btn-close").click()
        page.wait_for_timeout(900)
        page.evaluate("window.scrollBy({ top: -1000, behavior: 'smooth' })") #Прокрутить вверх страницу на 1000px
        page.wait_for_timeout(900)
        
        #Перейти на страницу прогноза дисциплины
        if page.viewport_size['width']<1200:  #Если размер экрана по горизонтали маленький, сначала нажать на кнопку для разворачивания других кнопок
            page.locator("button.navbar-toggler").first.click()
            page.wait_for_timeout(600)  # Ждем анимацию
        page.locator("#navbarContent a").nth(2).click() #Нажать на кнопку для страницы прогноза заплыва
        #Приблизить страницу
        page.evaluate(f"document.documentElement.style.zoom = '{int(ZOOM_SCALE*100)}%'")
        page.wait_for_timeout(2000) #Дождаться полной загрузки страницы
        
        #Ввод данных о дисциплине
        page.locator("#selectStyle").focus()
        page.wait_for_timeout(300)
        page.locator("#selectStyle").press("ArrowDown")
        page.wait_for_timeout(300)
        page.locator("#selectStyle").press("ArrowDown")
        page.wait_for_timeout(300)
        page.locator("#selectStyle").press("ArrowDown")
        page.wait_for_timeout(300)
        page.locator("#selectStyle").press("ArrowDown")
        page.wait_for_timeout(300)
        page.locator("#selectDistance").focus()
        page.wait_for_timeout(300)
        page.keyboard.press("5")
        page.wait_for_timeout(300)
        page.locator("#selectSex").focus()
        page.wait_for_timeout(300)
        page.locator("#selectSex").press("ArrowDown")
        page.wait_for_timeout(300)
        page.locator("#selectSex").press("ArrowDown")
        page.wait_for_timeout(300)
        page.locator("#selectPoolLength").focus()
        page.wait_for_timeout(300)
        page.keyboard.press("2")
        page.wait_for_timeout(300)
        page.locator("#selectHostCountry + .ts-wrapper input").focus()
        page.wait_for_timeout(1000)
        page.locator("#selectHostCountry + .ts-wrapper .ts-dropdown .option", has_text="Азербайджан").click()
        page.keyboard.press("Escape")  #Закрыть томселект
        page.wait_for_timeout(300) #Подождать после ввода поля
        page.locator("#checkHasSemifinals").check()
        page.wait_for_timeout(300) #Подождать после ввода поля
        page.get_by_text("Применить",exact=True).first.click() #Нажать по кнопке предсказания
        page.wait_for_timeout(400)  #Ждем анимацию
        page.evaluate("window.scrollBy({ top: 500, behavior: 'smooth' })") #Прокрутить вниз страницу на 500px
        page.wait_for_timeout(500)  #Ждем анимацию
        page.locator("div#swimInputAccordeon .accordion-button").nth(0).click() #Раскрыть меню для ввода сведений о 1 фазе полуфинале
        page.evaluate("window.scrollBy({ top: 800, behavior: 'smooth' })") #Прокрутить вниз страницу на 800px
        page.wait_for_timeout(500)  #Ждем анимацию
        page.locator("#selectSwimmerSemifinals0Lane4 + .ts-wrapper input").focus()
        page.wait_for_timeout(1000)
        page.locator("#selectSwimmerSemifinals0Lane4 + .ts-wrapper .ts-dropdown .option", has_text="DOUGLASS Kate").click()
        page.keyboard.press("Escape")  #Закрыть томселект
        page.wait_for_timeout(300) #Подождать пока томселект закроется
        page.locator("#inputDatetimeSwimInputSemifinalsSwim0").focus()
        page.wait_for_timeout(300)
        page.keyboard.press("1")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(150)
        page.keyboard.press("6")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("6")
        page.wait_for_timeout(150)
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(150)
        page.keyboard.press("1")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(150)
        page.keyboard.press("ArrowLeft")
        page.wait_for_timeout(150)
        page.keyboard.press("5")
        page.wait_for_timeout(300)
        
        page.evaluate("window.scrollBy({ top: 900, behavior: 'smooth' })") #Прокрутить вниз страницу на 900px
        page.wait_for_timeout(500)  #Ждем анимацию
        page.locator("div#swimInputAccordeon .accordion-button").nth(1).click() #Раскрыть меню для ввода сведений о 1 фазе полуфинале
        page.evaluate("window.scrollBy({ top: 800, behavior: 'smooth' })") #Прокрутить вниз страницу на 800px
        page.wait_for_timeout(500)  #Ждем анимацию
        page.locator("#selectSwimmerSemifinals1Lane5 + .ts-wrapper input").focus()
        page.keyboard.press("Backspace")
        page.wait_for_timeout(150)
        page.keyboard.press("R")
        page.wait_for_timeout(150)
        page.keyboard.press("U")
        page.wait_for_timeout(150)
        page.keyboard.press("C")
        page.wait_for_timeout(150)
        page.keyboard.press("K")
        page.wait_for_timeout(1000)
        page.locator("#selectSwimmerSemifinals1Lane5 + .ts-wrapper .ts-dropdown .option", has_text="RUCK Taylor").click()
        page.keyboard.press("Escape")  #Закрыть томселект
        page.wait_for_timeout(300) #Подождать пока томселект закроется
        page.locator("#inputDatetimeSwimInputSemifinalsSwim1").focus()
        page.wait_for_timeout(300)
        page.keyboard.press("1")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(150)
        page.keyboard.press("6")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("6")
        page.wait_for_timeout(150)
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(150)
        page.keyboard.press("1")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(150)
        page.keyboard.press("ArrowLeft")
        page.wait_for_timeout(150)
        page.keyboard.press("5")
        page.wait_for_timeout(300)
        
        page.evaluate("window.scrollBy({ top: 900, behavior: 'smooth' })") #Прокрутить вниз страницу на 900px
        page.wait_for_timeout(500)  #Ждем анимацию
        page.locator("div#swimInputAccordeon .accordion-button").nth(2).click() #Раскрыть меню для ввода сведений о 1 фазе полуфинале
        page.wait_for_timeout(500)  #Ждем анимацию
        page.evaluate("window.scrollBy({ top: 500, behavior: 'smooth' })") #Прокрутить вниз страницу на 500px
        page.wait_for_timeout(500)  #Ждем анимацию
        page.locator("#inputDatetimeSwimInputFinalsSwim0").focus()
        page.wait_for_timeout(300)
        page.keyboard.press("1")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(150)
        page.keyboard.press("6")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(150)
        page.keyboard.press("2")
        page.wait_for_timeout(150)
        page.keyboard.press("6")
        page.wait_for_timeout(150)
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(150)
        page.keyboard.press("1")
        page.wait_for_timeout(150)
        page.keyboard.press("8")
        page.wait_for_timeout(150)
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(150)
        page.keyboard.press("ArrowLeft")
        page.wait_for_timeout(150)
        page.keyboard.press("0")
        page.wait_for_timeout(300)
        
        page.evaluate("window.scrollBy({ top: 900, behavior: 'smooth' })") #Прокрутить вниз страницу на 900px
        page.wait_for_timeout(500)  #Ждем анимацию
        page.get_by_text("Предсказать дисциплину",exact=True).nth(1).click() #Нажать по кнопке предсказания
        page.wait_for_timeout(400)  #Ждем анимацию
        page.evaluate("window.scrollBy({ top: 800, behavior: 'smooth' })") #Прокрутить вниз страницу на 800px
        page.wait_for_timeout(700)  #Ждем анимацию
        
        #Раскрыть аккордеон с результатами
        for i in [2,1,0]:
            page.locator('div#resultsAccordion .accordion-button').nth(i).click()
            page.wait_for_timeout(800) #Подождать раскрытия аккордеона
        page.evaluate("window.scrollBy({ top: 900, behavior: 'smooth' })") #Прокрутить вниз страницу на 900px
        page.wait_for_timeout(500)  #Ждем анимацию
        page.wait_for_timeout(7000)  #Показываем результаты
        
        #Показать графики
        page.get_by_text("Графики...",exact=True).nth(2).click() #Нажать по кнопке графиков
        page.wait_for_timeout(3000)
        page.evaluate("""
            document.querySelector('.modal.show').scrollBy({ top: 600, behavior: 'smooth' })
        """)#Прокрутить вниз страницу на 600px
        page.wait_for_timeout(2000)
        page.evaluate("""
            document.querySelector('.modal.show').scrollBy({ top: -600, behavior: 'smooth' })
        """)#Прокрутить вверх страницу на 600px
        page.wait_for_timeout(1300)
        page.locator("div.modal-header button.btn-close").click()
        page.wait_for_timeout(900)
        page.get_by_text("Графики...",exact=True).nth(3).click() #Нажать по кнопке графиков
        page.wait_for_timeout(3000)
        page.evaluate("""
            document.querySelector('.modal.show').scrollBy({ top: 600, behavior: 'smooth' })
        """)#Прокрутить вниз страницу на 600px
        page.wait_for_timeout(2000)
        page.evaluate("""
            document.querySelector('.modal.show').scrollBy({ top: 600, behavior: 'smooth' })
        """)#Прокрутить вниз страницу на 600px
        page.wait_for_timeout(2000)
        page.evaluate("""
            document.querySelector('.modal.show').scrollBy({ top: -1200, behavior: 'smooth' })
        """) #Прокрутить вверх страницу на 1200px
        page.wait_for_timeout(1300)
        page.locator("div.modal-header button.btn-close").click()
        page.wait_for_timeout(4000)
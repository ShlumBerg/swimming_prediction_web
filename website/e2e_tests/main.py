import pytest
from playwright.sync_api import sync_playwright,Browser,Page,expect
BASE_URL_DEFAULT="http://217.26.30.216"
SWIM_PAGE_PATH="/swim"

#Настроить размер viewport для playwright (через встроеную в него функцию)
@pytest.fixture(scope="function")
def browser_context_args(viewport):
    return {"viewport": viewport}


@pytest.mark.parametrize("viewport",[
    pytest.param({"width":393,"height":852},id="xs"), #extra small (iphone 14 iOS 18.6 vertical)
    pytest.param({"width":712,"height":1138},id="sm"), #small (galaxy tab s9 android 14 vetrical)
    pytest.param({"width":820,"height":1180},id="md"), #medium (iPad 10 iPadOS 18.6 vertical)
    pytest.param({"width":1024,"height":600},id="lg"), #large (Nest Hub horizontal)
    pytest.param({"width":1280,"height":800},id="xl"), #extra large (Nest Hub Max horizontal)
    pytest.param({"width":1920,"height":1080},id="xxl"), #extra extra large (1080p television horizontal)
])
class TestMainPage:
    #Проверить что все нужные элементы прогрузились при отсутствии действий на странице
    def test_all_elements_present_and_have_required_text_no_actions(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        try:
            header_title=page.locator("nav").get_by_text('Система прогноза результатов по плаванию').first
        except:
            header_title=None
        try:
            card_title=page.locator("body > div").get_by_text('Система прогноза результатов по плаванию').first
        except:
            card_title=None
        try:
            card_main_text=page.get_by_text('Данная система была разработана в рамках ВКР').first
        except:
            card_main_text=None
        try:
            header_btn_main=page.locator("nav").get_by_text("Главная").first
        except:
            header_btn_main=None
        try:
            card_btn_predict_swim=page.locator("body > div").get_by_text("Предсказать заплыв").first
        except:
            card_btn_predict_swim=None
        try:
            card_btn_predict_discipline=page.locator("body > div").get_by_text("Предсказать дисциплину").first
        except:
            card_btn_predict_discipline=None
        try:
            header_btn_predict_swim=page.locator("nav").get_by_text("Предсказать заплыв").first
        except:
            header_btn_predict_swim=None
        try:
            header_btn_predict_discipline=page.locator("nav").get_by_text("Предсказать дисциплину").first
        except:
            header_btn_predict_discipline=None
        try:
            header_btn_collapse=page.locator("button.navbar-toggler").first
        except:
            header_btn_collapse=None
        
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert card_title is not None and card_title.is_visible()
        assert card_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(card_title).to_have_js_property("tagName","H1")
        assert card_main_text is not None and card_main_text.is_visible()
        assert card_main_text.inner_text()=='Данная система была разработана в рамках ВКР. Позволяет предсказывать результаты заплывов и дисциплин.'
        expect(card_main_text).to_have_js_property("tagName","P")
        assert card_btn_predict_swim is not None and card_btn_predict_swim.is_visible()
        assert card_btn_predict_swim.inner_text()=='Предсказать заплыв'
        expect(card_btn_predict_swim).to_have_attribute("href","swim")
        assert card_btn_predict_discipline is not None and card_btn_predict_discipline.is_visible()
        assert card_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
        expect(card_btn_predict_discipline).to_have_attribute("href","discipline")
        
        
        if page.viewport_size['width']<1200:  #Если размер экрана по горизонтали маленький, должна появиться кнопка для сворачивания кнопок меню
            assert header_btn_predict_swim is None or not header_btn_predict_swim.is_visible()
            assert header_btn_predict_discipline is None or not header_btn_predict_discipline.is_visible()
            assert header_btn_main is None or not header_btn_main.is_visible()
            assert header_btn_collapse is not None and header_btn_collapse.is_visible()
        else:
            assert header_btn_collapse is None or not header_btn_collapse.is_visible()
            assert header_btn_main is not None and header_btn_main.is_visible()
            assert header_btn_main.inner_text()=='Главная'
            href = header_btn_main.get_attribute("href")
            assert href=="" or href is None
            assert header_btn_predict_swim is not None and header_btn_predict_swim.is_visible()
            assert header_btn_predict_swim.inner_text()=='Предсказать заплыв'
            href = header_btn_predict_swim.get_attribute("href")
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="discipline"
    
    #Проверить что все нужные элементы отображаются правильно после разворачивания панели в шапке на маленьких экранах
    def test_all_elements_present_and_have_required_text_after_expand(self,base_url,page:Page,viewport):
        if page.viewport_size['width']>=1200: #Если размер страницы большой - работать с меню нельзя!
            return
        url=base_url if base_url else BASE_URL_DEFAULT
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Развернуть сворачивающееся меню в шапке
        page.locator("button.navbar-toggler").first.click()
        page.wait_for_timeout(600)  # Ждем анимацию
        
        try:
            header_title=page.locator("nav").get_by_text('Система прогноза результатов по плаванию').first
        except:
            header_title=None
        try:
            card_title=page.locator("body > div").get_by_text('Система прогноза результатов по плаванию').first
        except:
            card_title=None
        try:
            card_main_text=page.get_by_text('Данная система была разработана в рамках ВКР').first
        except:
            card_main_text=None
        try:
            header_btn_main=page.locator("nav").get_by_text("Главная").first
        except:
            header_btn_main=None
        try:
            card_btn_predict_swim=page.locator("body > div").get_by_text("Предсказать заплыв").first
        except:
            card_btn_predict_swim=None
        try:
            card_btn_predict_discipline=page.locator("body > div").get_by_text("Предсказать дисциплину").first
        except:
            card_btn_predict_discipline=None
        try:
            header_btn_predict_swim=page.locator("nav").get_by_text("Предсказать заплыв").first
        except:
            header_btn_predict_swim=None
        try:
            header_btn_predict_discipline=page.locator("nav").get_by_text("Предсказать дисциплину").first
        except:
            header_btn_predict_discipline=None
        try:
            header_btn_collapse=page.locator("button.navbar-toggler").first
        except:
            header_btn_collapse=None
        
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert card_title is not None and card_title.is_visible()
        assert card_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(card_title).to_have_js_property("tagName","H1")
        assert card_main_text is not None and card_main_text.is_visible()
        assert card_main_text.inner_text()=='Данная система была разработана в рамках ВКР. Позволяет предсказывать результаты заплывов и дисциплин.'
        expect(card_main_text).to_have_js_property("tagName","P")
        assert card_btn_predict_swim is not None and card_btn_predict_swim.is_visible()
        assert card_btn_predict_swim.inner_text()=='Предсказать заплыв'
        expect(card_btn_predict_swim).to_have_attribute("href","swim")
        assert card_btn_predict_discipline is not None and card_btn_predict_discipline.is_visible()
        assert card_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
        expect(card_btn_predict_discipline).to_have_attribute("href","discipline")
        
        
        #Проверка элементов которые зависят от размера экрана
        assert header_btn_collapse is not None and header_btn_collapse.is_visible()
        assert header_btn_main is not None and header_btn_main.is_visible()
        assert header_btn_main.inner_text()=='Главная'
        href = header_btn_main.get_attribute("href")
        assert href=="" or href is None
        assert header_btn_predict_swim is not None and header_btn_predict_swim.is_visible()
        assert header_btn_predict_swim.inner_text()=='Предсказать заплыв'
        href = header_btn_predict_swim.get_attribute("href")
        assert href=="swim"
        assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
        assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
        href = header_btn_predict_discipline.get_attribute("href")
        assert href=="discipline"
    
    #Проверить что все нужные элементы отображаются правильно после разворачивания и сворачивания панели в шапке на маленьких экранах
    def test_all_elements_present_and_have_required_text_after_expand_collapse(self,base_url,page:Page,viewport):
        if page.viewport_size['width']>=1200: #Если размер страницы большой - работать с меню нельзя!
            return
        url=base_url if base_url else BASE_URL_DEFAULT
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Развернуть и свернуть сворачивающееся меню в шапке
        page.locator("button.navbar-toggler").first.click()
        page.wait_for_timeout(600)  # Ждем анимацию
        page.locator("button.navbar-toggler").first.click()
        page.wait_for_timeout(600)  # Ждем анимацию
        
        try:
            header_title=page.locator("nav").get_by_text('Система прогноза результатов по плаванию').first
        except:
            header_title=None
        try:
            card_title=page.locator("body > div").get_by_text('Система прогноза результатов по плаванию').first
        except:
            card_title=None
        try:
            card_main_text=page.get_by_text('Данная система была разработана в рамках ВКР').first
        except:
            card_main_text=None
        try:
            header_btn_main=page.locator("nav").get_by_text("Главная").first
        except:
            header_btn_main=None
        try:
            card_btn_predict_swim=page.locator("body > div").get_by_text("Предсказать заплыв").first
        except:
            card_btn_predict_swim=None
        try:
            card_btn_predict_discipline=page.locator("body > div").get_by_text("Предсказать дисциплину").first
        except:
            card_btn_predict_discipline=None
        try:
            header_btn_predict_swim=page.locator("nav").get_by_text("Предсказать заплыв").first
        except:
            header_btn_predict_swim=None
        try:
            header_btn_predict_discipline=page.locator("nav").get_by_text("Предсказать дисциплину").first
        except:
            header_btn_predict_discipline=None
        try:
            header_btn_collapse=page.locator("button.navbar-toggler").first
        except:
            header_btn_collapse=None
        
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert card_title is not None and card_title.is_visible()
        assert card_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(card_title).to_have_js_property("tagName","H1")
        assert card_main_text is not None and card_main_text.is_visible()
        assert card_main_text.inner_text()=='Данная система была разработана в рамках ВКР. Позволяет предсказывать результаты заплывов и дисциплин.'
        expect(card_main_text).to_have_js_property("tagName","P")
        assert card_btn_predict_swim is not None and card_btn_predict_swim.is_visible()
        assert card_btn_predict_swim.inner_text()=='Предсказать заплыв'
        expect(card_btn_predict_swim).to_have_attribute("href","swim")
        assert card_btn_predict_discipline is not None and card_btn_predict_discipline.is_visible()
        assert card_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
        expect(card_btn_predict_discipline).to_have_attribute("href","discipline")
        
        
        #Проверка элементов которые зависят от размера экрана
        assert header_btn_predict_swim is None or not header_btn_predict_swim.is_visible()
        assert header_btn_predict_discipline is None or not header_btn_predict_discipline.is_visible()
        assert header_btn_main is None or not header_btn_main.is_visible()
        assert header_btn_collapse is not None and header_btn_collapse.is_visible()


#Настроить размер viewport для playwright (через встроеную в него функцию)
@pytest.fixture(scope="function")
def browser_context_args(viewport):
    return {"viewport": viewport}
@pytest.mark.parametrize("viewport",[
    pytest.param({"width":393,"height":852},id="xs"), #extra small (iphone 14 iOS 18.6 vertical)
    pytest.param({"width":712,"height":1138},id="sm"), #small (galaxy tab s9 android 14 vetrical)
    pytest.param({"width":820,"height":1180},id="md"), #medium (iPad 10 iPadOS 18.6 vertical)
    pytest.param({"width":1024,"height":600},id="lg"), #large (Nest Hub horizontal)
    pytest.param({"width":1280,"height":800},id="xl"), #extra large (Nest Hub Max horizontal)
    pytest.param({"width":1920,"height":1080},id="xxl"), #extra extra large (1080p television horizontal)
])
class TestSwimPredPage:
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при отсутствии действий на странице
    def test_all_elements_present_and_have_required_text_no_actions(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+SWIM_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        try:
            header_title=page.locator("nav").get_by_text('Система прогноза результатов по плаванию').first
        except:
            header_title=None
        try:
            header_btn_main=page.locator("nav").get_by_text("Главная").first
        except:
            header_btn_main=None
        try:
            header_btn_predict_swim=page.locator("nav").get_by_text("Предсказать заплыв").first
        except:
            header_btn_predict_swim=None
        try:
            header_btn_predict_discipline=page.locator("nav").get_by_text("Предсказать дисциплину").first
        except:
            header_btn_predict_discipline=None
        try:
            header_btn_collapse=page.locator("button.navbar-toggler").first
        except:
            header_btn_collapse=None
        
        try:
            card1_title=page.get_by_text('Введите сведения о заплыве').first
        except:
            card1_title=None
        try:
            card1_style_label=page.get_by_text('Стиль плавания:').first
        except:
            card1_style_label=None
        try:
            card1_distance_label=page.get_by_text('Дистанция:').first
        except:
            card1_distance_label=None
        try:
            card1_sex_label=page.get_by_text('Пол:').first
        except:
            card1_sex_label=None
        try:
            card1_phase_label=page.get_by_text('Фаза:').first
        except:
            card1_phase_label=None
        try:
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_datetime_label=page.get_by_text('Местная дата и время заплыва:').first
        except:
            card1_datetime_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_style_select=page.locator('select').filter(has_text="Выберите стиль").first
        except:
            card1_style_select=None
        try:
            card1_distance_select=page.locator('select').filter(has_text="Выберите дистанцию").first
        except:
            card1_distance_select=None
        try:
            card1_sex_select=page.locator('select').filter(has_text="Выберите пол").first
        except:
            card1_sex_select=None
        try:
            card1_phase_select=page.locator('select').filter(has_text="Выберите фазу заплыва").first
        except:
            card1_phase_select=None
        try:
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_datetime_input=page.locator("input[type='datetime-local']").first
        except:
            card1_datetime_input=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        
        try:
            card2_title=page.get_by_text('Введите сведения о пловцах заплыва').first
        except:
            card2_title=None
        try:
            card2_lane_header=page.get_by_text('Дорожка').first
        except:
            card2_lane_header=None
        try:
            card2_swimmer_header=page.get_by_text('Пловец').first
        except:
            card2_swimmer_header=None
        try:
            card2_lane_0_label=page.get_by_text('0',exact=True).first
        except:
            card2_lane_0_label=None
        try:
            card2_lane_1_label=page.get_by_text('1',exact=True).first
        except:
            card2_lane_1_label=None
        try:
            card2_lane_2_label=page.get_by_text('2',exact=True).first
        except:
            card2_lane_2_label=None
        try:
            card2_lane_3_label=page.get_by_text('3',exact=True).first
        except:
            card2_lane_3_label=None
        try:
            card2_lane_4_label=page.get_by_text('4',exact=True).first
        except:
            card2_lane_4_label=None
        try:
            card2_lane_5_label=page.get_by_text('5',exact=True).first
        except:
            card2_lane_5_label=None
        try:
            card2_lane_6_label=page.get_by_text('6',exact=True).first
        except:
            card2_lane_6_label=None
        try:
            card2_lane_7_label=page.get_by_text('7',exact=True).first
        except:
            card2_lane_7_label=None
        try:
            card2_lane_8_label=page.get_by_text('8',exact=True).first
        except:
            card2_lane_8_label=None
        try:
            card2_lane_9_label=page.get_by_text('9',exact=True).first
        except:
            card2_lane_9_label=None
        try:
            card2_lane_0_swimmer_select=page.locator('select').filter(has_text='Нет пловца').first
        except:
            card2_lane_0_swimmer_select=None
        try:
            card2_lane_1_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(1)
        except:
            card2_lane_1_swimmer_select=None
        try:
            card2_lane_2_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(2)
        except:
            card2_lane_2_swimmer_select=None
        try:
            card2_lane_3_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(3)
        except:
            card2_lane_3_swimmer_select=None
        try:
            card2_lane_4_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(4)
        except:
            card2_lane_4_swimmer_select=None
        try:
            card2_lane_5_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(5)
        except:
            card2_lane_5_swimmer_select=None
        try:
            card2_lane_6_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(6)
        except:
            card2_lane_6_swimmer_select=None
        try:
            card2_lane_7_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(7)
        except:
            card2_lane_7_swimmer_select=None
        try:
            card2_lane_8_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(8)
        except:
            card2_lane_8_swimmer_select=None
        try:
            card2_lane_9_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(9)
        except:
            card2_lane_9_swimmer_select=None
            
        try:
            btn_predict=page.get_by_text("Предсказать",exact=True)
        except:
            btn_predict=None
        
        try:
            card1_style_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите стиль плавания!").first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите дистанцию!").first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите пол!").first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_phase_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите фазу!").first
        except:
            card1_phase_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите длину бассейна!").first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_datetime_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите дату и время заплыва (от 2026 до 2050 года)!").first
        except:
            card1_datetime_invalid_feedback=None
        try:
            card1_host_country_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите страну заплыва!").first
        except:
            card1_host_country_invalid_feedback=None
        try:
            card2_swimmers_invalid_alert=page.locator('div.alert')
        except:
            card2_swimmers_invalid_alert=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_cards_count=page.locator("[id^='swimmer'][id$='Results']").filter(visible=True).count() #Число выходных карточек
        except:
            visible_result_cards_count=0
        
        try:
            toasts_count=page.locator("div.toast").count()
        except:
            toasts_count=0
        
        
        
        
        
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о заплыве"
        expect(card1_title).to_have_js_property("tagName","DIV")
        assert(card1_style_label) is not None and card1_style_label.is_visible()
        assert card1_style_label.inner_text()=="Стиль плавания:"
        expect(card1_style_label).to_have_js_property("tagName","LABEL")
        assert(card1_distance_label) is not None and card1_distance_label.is_visible()
        assert card1_distance_label.inner_text()=="Дистанция:"
        expect(card1_distance_label).to_have_js_property("tagName","LABEL")
        assert(card1_sex_label) is not None and card1_sex_label.is_visible()
        assert card1_sex_label.inner_text()=="Пол:"
        expect(card1_sex_label).to_have_js_property("tagName","LABEL")
        assert(card1_phase_label) is not None and card1_phase_label.is_visible()
        assert card1_phase_label.inner_text()=="Фаза:"
        expect(card1_phase_label).to_have_js_property("tagName","LABEL")
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_datetime_label) is not None and card1_datetime_label.is_visible()
        assert card1_datetime_label.inner_text()=="Местная дата и время заплыва:"
        expect(card1_datetime_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select).to_have_value("")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select).to_have_value("")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select).to_have_value("")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_phase_select) is not None and card1_phase_select.is_visible()
        expect(card1_phase_select).to_have_value("")
        expect(card1_phase_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select).to_have_value("")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_datetime_input) is not None and card1_datetime_input.is_visible()
        expect(card1_datetime_input).to_have_attribute("type","datetime-local")
        expect(card1_datetime_input).to_have_js_property("tagName","INPUT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select).to_have_value("")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        
        assert(card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите сведения о пловцах заплыва"
        expect(card2_title).to_have_js_property("tagName","DIV")
        assert(card2_lane_header) is not None and card2_lane_header.is_visible()
        assert card2_lane_header.inner_text()=="Дорожка"
        expect(card2_lane_header).to_have_js_property("tagName","LABEL")
        assert(card2_swimmer_header) is not None and card2_swimmer_header.is_visible()
        assert card2_swimmer_header.inner_text()=="Пловец"
        expect(card2_swimmer_header).to_have_js_property("tagName","LABEL")
        assert(card2_lane_0_label) is not None and card2_lane_0_label.is_visible()
        assert card2_lane_0_label.inner_text()=="0"
        expect(card2_lane_0_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_1_label) is not None and card2_lane_1_label.is_visible()
        assert card2_lane_1_label.inner_text()=="1"
        expect(card2_lane_1_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_2_label) is not None and card2_lane_2_label.is_visible()
        assert card2_lane_2_label.inner_text()=="2"
        expect(card2_lane_2_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_3_label) is not None and card2_lane_3_label.is_visible()
        assert card2_lane_3_label.inner_text()=="3"
        expect(card2_lane_3_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_4_label) is not None and card2_lane_4_label.is_visible()
        assert card2_lane_4_label.inner_text()=="4"
        expect(card2_lane_4_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_5_label) is not None and card2_lane_5_label.is_visible()
        assert card2_lane_5_label.inner_text()=="5"
        expect(card2_lane_5_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_6_label) is not None and card2_lane_6_label.is_visible()
        assert card2_lane_6_label.inner_text()=="6"
        expect(card2_lane_6_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_7_label) is not None and card2_lane_7_label.is_visible()
        assert card2_lane_7_label.inner_text()=="7"
        expect(card2_lane_7_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_8_label) is not None and card2_lane_8_label.is_visible()
        assert card2_lane_8_label.inner_text()=="8"
        expect(card2_lane_8_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_9_label) is not None and card2_lane_9_label.is_visible()
        assert card2_lane_9_label.inner_text()=="9"
        expect(card2_lane_9_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_0_swimmer_select) is not None and card2_lane_0_swimmer_select.is_visible()
        expect(card2_lane_0_swimmer_select).to_have_value("")
        expect(card2_lane_0_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_1_swimmer_select) is not None and card2_lane_1_swimmer_select.is_visible()
        expect(card2_lane_1_swimmer_select).to_have_value("")
        expect(card2_lane_1_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_2_swimmer_select) is not None and card2_lane_2_swimmer_select.is_visible()
        expect(card2_lane_2_swimmer_select).to_have_value("")
        expect(card2_lane_2_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_3_swimmer_select) is not None and card2_lane_3_swimmer_select.is_visible()
        expect(card2_lane_3_swimmer_select).to_have_value("")
        expect(card2_lane_3_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_4_swimmer_select) is not None and card2_lane_4_swimmer_select.is_visible()
        expect(card2_lane_4_swimmer_select).to_have_value("")
        expect(card2_lane_4_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_5_swimmer_select) is not None and card2_lane_5_swimmer_select.is_visible()
        expect(card2_lane_5_swimmer_select).to_have_value("")
        expect(card2_lane_5_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_6_swimmer_select) is not None and card2_lane_6_swimmer_select.is_visible()
        expect(card2_lane_6_swimmer_select).to_have_value("")
        expect(card2_lane_6_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_7_swimmer_select) is not None and card2_lane_7_swimmer_select.is_visible()
        expect(card2_lane_7_swimmer_select).to_have_value("")
        expect(card2_lane_7_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_8_swimmer_select) is not None and card2_lane_8_swimmer_select.is_visible()
        expect(card2_lane_8_swimmer_select).to_have_value("")
        expect(card2_lane_8_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_9_swimmer_select) is not None and card2_lane_9_swimmer_select.is_visible()
        expect(card2_lane_9_swimmer_select).to_have_value("")
        expect(card2_lane_9_swimmer_select).to_have_js_property("tagName","SELECT")
        
        assert(btn_predict) is not None and btn_predict.is_visible()
        expect(btn_predict).to_have_text("Предсказать")
        expect(btn_predict).to_have_js_property("tagName","BUTTON")
        
        if page.viewport_size['width']<1200:  #Если размер экрана по горизонтали маленький, должна появиться кнопка для сворачивания кнопок меню
            assert header_btn_predict_swim is None or not header_btn_predict_swim.is_visible()
            assert header_btn_predict_discipline is None or not header_btn_predict_discipline.is_visible()
            assert header_btn_main is None or not header_btn_main.is_visible()
            assert header_btn_collapse is not None and header_btn_collapse.is_visible()
        else:
            assert header_btn_collapse is None or not header_btn_collapse.is_visible()
            assert header_btn_main is not None and header_btn_main.is_visible()
            assert header_btn_main.inner_text()=='Главная'
            href = header_btn_main.get_attribute("href")
            assert href=="/"
            assert header_btn_predict_swim is not None and header_btn_predict_swim.is_visible()
            assert header_btn_predict_swim.inner_text()=='Предсказать заплыв'
            href = header_btn_predict_swim.get_attribute("href")
            assert href=="" or href is None
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="discipline"
        
        #Проверка элементов которых не должно быть видно (сообщения об ошибках ввода, модальные окна)
        assert not graphs_modal.is_visible()
        assert not card1_style_invalid_feedback.is_visible()
        assert not card1_distance_invalid_feedback.is_visible()
        assert not card1_sex_invalid_feedback.is_visible()
        assert not card1_phase_invalid_feedback.is_visible()
        assert not card1_pool_length_invalid_feedback.is_visible()
        assert not card1_datetime_invalid_feedback.is_visible()
        assert not card1_host_country_invalid_feedback.is_visible()
        assert not card2_swimmers_invalid_alert.is_visible()
        #Проверка элементов которых не должно существовать (результаты заплыва, тосты с ошибками сети)
        assert toasts_count==0
        assert visible_result_cards_count==0
    
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при разворачивании меню в шапке на маленьких экранах
    def test_all_elements_present_and_have_required_text_after_expand_header_menu(self,base_url,page:Page,viewport):
        if page.viewport_size['width']>=1200: #Если размер страницы большой - работать с меню нельзя!
            return
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+SWIM_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Развернуть сворачивающееся меню в шапке
        page.locator("button.navbar-toggler").first.click()
        page.wait_for_timeout(600)  # Ждем анимацию
        try:
            header_title=page.locator("nav").get_by_text('Система прогноза результатов по плаванию').first
        except:
            header_title=None
        try:
            header_btn_main=page.locator("nav").get_by_text("Главная").first
        except:
            header_btn_main=None
        try:
            header_btn_predict_swim=page.locator("nav").get_by_text("Предсказать заплыв").first
        except:
            header_btn_predict_swim=None
        try:
            header_btn_predict_discipline=page.locator("nav").get_by_text("Предсказать дисциплину").first
        except:
            header_btn_predict_discipline=None
        try:
            header_btn_collapse=page.locator("button.navbar-toggler").first
        except:
            header_btn_collapse=None
        
        try:
            card1_title=page.get_by_text('Введите сведения о заплыве').first
        except:
            card1_title=None
        try:
            card1_style_label=page.get_by_text('Стиль плавания:').first
        except:
            card1_style_label=None
        try:
            card1_distance_label=page.get_by_text('Дистанция:').first
        except:
            card1_distance_label=None
        try:
            card1_sex_label=page.get_by_text('Пол:').first
        except:
            card1_sex_label=None
        try:
            card1_phase_label=page.get_by_text('Фаза:').first
        except:
            card1_phase_label=None
        try:
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_datetime_label=page.get_by_text('Местная дата и время заплыва:').first
        except:
            card1_datetime_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_style_select=page.locator('select').filter(has_text="Выберите стиль").first
        except:
            card1_style_select=None
        try:
            card1_distance_select=page.locator('select').filter(has_text="Выберите дистанцию").first
        except:
            card1_distance_select=None
        try:
            card1_sex_select=page.locator('select').filter(has_text="Выберите пол").first
        except:
            card1_sex_select=None
        try:
            card1_phase_select=page.locator('select').filter(has_text="Выберите фазу заплыва").first
        except:
            card1_phase_select=None
        try:
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_datetime_input=page.locator("input[type='datetime-local']").first
        except:
            card1_datetime_input=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        
        try:
            card2_title=page.get_by_text('Введите сведения о пловцах заплыва').first
        except:
            card2_title=None
        try:
            card2_lane_header=page.get_by_text('Дорожка').first
        except:
            card2_lane_header=None
        try:
            card2_swimmer_header=page.get_by_text('Пловец').first
        except:
            card2_swimmer_header=None
        try:
            card2_lane_0_label=page.get_by_text('0',exact=True).first
        except:
            card2_lane_0_label=None
        try:
            card2_lane_1_label=page.get_by_text('1',exact=True).first
        except:
            card2_lane_1_label=None
        try:
            card2_lane_2_label=page.get_by_text('2',exact=True).first
        except:
            card2_lane_2_label=None
        try:
            card2_lane_3_label=page.get_by_text('3',exact=True).first
        except:
            card2_lane_3_label=None
        try:
            card2_lane_4_label=page.get_by_text('4',exact=True).first
        except:
            card2_lane_4_label=None
        try:
            card2_lane_5_label=page.get_by_text('5',exact=True).first
        except:
            card2_lane_5_label=None
        try:
            card2_lane_6_label=page.get_by_text('6',exact=True).first
        except:
            card2_lane_6_label=None
        try:
            card2_lane_7_label=page.get_by_text('7',exact=True).first
        except:
            card2_lane_7_label=None
        try:
            card2_lane_8_label=page.get_by_text('8',exact=True).first
        except:
            card2_lane_8_label=None
        try:
            card2_lane_9_label=page.get_by_text('9',exact=True).first
        except:
            card2_lane_9_label=None
        try:
            card2_lane_0_swimmer_select=page.locator('select').filter(has_text='Нет пловца').first
        except:
            card2_lane_0_swimmer_select=None
        try:
            card2_lane_1_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(1)
        except:
            card2_lane_1_swimmer_select=None
        try:
            card2_lane_2_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(2)
        except:
            card2_lane_2_swimmer_select=None
        try:
            card2_lane_3_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(3)
        except:
            card2_lane_3_swimmer_select=None
        try:
            card2_lane_4_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(4)
        except:
            card2_lane_4_swimmer_select=None
        try:
            card2_lane_5_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(5)
        except:
            card2_lane_5_swimmer_select=None
        try:
            card2_lane_6_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(6)
        except:
            card2_lane_6_swimmer_select=None
        try:
            card2_lane_7_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(7)
        except:
            card2_lane_7_swimmer_select=None
        try:
            card2_lane_8_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(8)
        except:
            card2_lane_8_swimmer_select=None
        try:
            card2_lane_9_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(9)
        except:
            card2_lane_9_swimmer_select=None
            
        try:
            btn_predict=page.get_by_text("Предсказать",exact=True)
        except:
            btn_predict=None
        
        try:
            card1_style_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите стиль плавания!").first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите дистанцию!").first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите пол!").first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_phase_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите фазу!").first
        except:
            card1_phase_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите длину бассейна!").first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_datetime_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите дату и время заплыва (от 2026 до 2050 года)!").first
        except:
            card1_datetime_invalid_feedback=None
        try:
            card1_host_country_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите страну заплыва!").first
        except:
            card1_host_country_invalid_feedback=None
        try:
            card2_swimmers_invalid_alert=page.locator('div.alert')
        except:
            card2_swimmers_invalid_alert=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_cards_count=page.locator("[id^='swimmer'][id$='Results']").filter(visible=True).count() #Число выходных карточек
        except:
            visible_result_cards_count=0
        
        try:
            toasts_count=page.locator("div.toast").count()
        except:
            toasts_count=0
        
        
        
        
        
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о заплыве"
        expect(card1_title).to_have_js_property("tagName","DIV")
        assert(card1_style_label) is not None and card1_style_label.is_visible()
        assert card1_style_label.inner_text()=="Стиль плавания:"
        expect(card1_style_label).to_have_js_property("tagName","LABEL")
        assert(card1_distance_label) is not None and card1_distance_label.is_visible()
        assert card1_distance_label.inner_text()=="Дистанция:"
        expect(card1_distance_label).to_have_js_property("tagName","LABEL")
        assert(card1_sex_label) is not None and card1_sex_label.is_visible()
        assert card1_sex_label.inner_text()=="Пол:"
        expect(card1_sex_label).to_have_js_property("tagName","LABEL")
        assert(card1_phase_label) is not None and card1_phase_label.is_visible()
        assert card1_phase_label.inner_text()=="Фаза:"
        expect(card1_phase_label).to_have_js_property("tagName","LABEL")
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_datetime_label) is not None and card1_datetime_label.is_visible()
        assert card1_datetime_label.inner_text()=="Местная дата и время заплыва:"
        expect(card1_datetime_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select).to_have_value("")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select).to_have_value("")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select).to_have_value("")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_phase_select) is not None and card1_phase_select.is_visible()
        expect(card1_phase_select).to_have_value("")
        expect(card1_phase_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select).to_have_value("")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_datetime_input) is not None and card1_datetime_input.is_visible()
        expect(card1_datetime_input).to_have_attribute("type","datetime-local")
        expect(card1_datetime_input).to_have_js_property("tagName","INPUT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select).to_have_value("")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        
        assert(card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите сведения о пловцах заплыва"
        expect(card2_title).to_have_js_property("tagName","DIV")
        assert(card2_lane_header) is not None and card2_lane_header.is_visible()
        assert card2_lane_header.inner_text()=="Дорожка"
        expect(card2_lane_header).to_have_js_property("tagName","LABEL")
        assert(card2_swimmer_header) is not None and card2_swimmer_header.is_visible()
        assert card2_swimmer_header.inner_text()=="Пловец"
        expect(card2_swimmer_header).to_have_js_property("tagName","LABEL")
        assert(card2_lane_0_label) is not None and card2_lane_0_label.is_visible()
        assert card2_lane_0_label.inner_text()=="0"
        expect(card2_lane_0_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_1_label) is not None and card2_lane_1_label.is_visible()
        assert card2_lane_1_label.inner_text()=="1"
        expect(card2_lane_1_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_2_label) is not None and card2_lane_2_label.is_visible()
        assert card2_lane_2_label.inner_text()=="2"
        expect(card2_lane_2_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_3_label) is not None and card2_lane_3_label.is_visible()
        assert card2_lane_3_label.inner_text()=="3"
        expect(card2_lane_3_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_4_label) is not None and card2_lane_4_label.is_visible()
        assert card2_lane_4_label.inner_text()=="4"
        expect(card2_lane_4_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_5_label) is not None and card2_lane_5_label.is_visible()
        assert card2_lane_5_label.inner_text()=="5"
        expect(card2_lane_5_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_6_label) is not None and card2_lane_6_label.is_visible()
        assert card2_lane_6_label.inner_text()=="6"
        expect(card2_lane_6_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_7_label) is not None and card2_lane_7_label.is_visible()
        assert card2_lane_7_label.inner_text()=="7"
        expect(card2_lane_7_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_8_label) is not None and card2_lane_8_label.is_visible()
        assert card2_lane_8_label.inner_text()=="8"
        expect(card2_lane_8_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_9_label) is not None and card2_lane_9_label.is_visible()
        assert card2_lane_9_label.inner_text()=="9"
        expect(card2_lane_9_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_0_swimmer_select) is not None and card2_lane_0_swimmer_select.is_visible()
        expect(card2_lane_0_swimmer_select).to_have_value("")
        expect(card2_lane_0_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_1_swimmer_select) is not None and card2_lane_1_swimmer_select.is_visible()
        expect(card2_lane_1_swimmer_select).to_have_value("")
        expect(card2_lane_1_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_2_swimmer_select) is not None and card2_lane_2_swimmer_select.is_visible()
        expect(card2_lane_2_swimmer_select).to_have_value("")
        expect(card2_lane_2_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_3_swimmer_select) is not None and card2_lane_3_swimmer_select.is_visible()
        expect(card2_lane_3_swimmer_select).to_have_value("")
        expect(card2_lane_3_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_4_swimmer_select) is not None and card2_lane_4_swimmer_select.is_visible()
        expect(card2_lane_4_swimmer_select).to_have_value("")
        expect(card2_lane_4_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_5_swimmer_select) is not None and card2_lane_5_swimmer_select.is_visible()
        expect(card2_lane_5_swimmer_select).to_have_value("")
        expect(card2_lane_5_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_6_swimmer_select) is not None and card2_lane_6_swimmer_select.is_visible()
        expect(card2_lane_6_swimmer_select).to_have_value("")
        expect(card2_lane_6_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_7_swimmer_select) is not None and card2_lane_7_swimmer_select.is_visible()
        expect(card2_lane_7_swimmer_select).to_have_value("")
        expect(card2_lane_7_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_8_swimmer_select) is not None and card2_lane_8_swimmer_select.is_visible()
        expect(card2_lane_8_swimmer_select).to_have_value("")
        expect(card2_lane_8_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_9_swimmer_select) is not None and card2_lane_9_swimmer_select.is_visible()
        expect(card2_lane_9_swimmer_select).to_have_value("")
        expect(card2_lane_9_swimmer_select).to_have_js_property("tagName","SELECT")
        
        assert(btn_predict) is not None and btn_predict.is_visible()
        expect(btn_predict).to_have_text("Предсказать")
        expect(btn_predict).to_have_js_property("tagName","BUTTON")
        
        
        #Проверка элементов которые зависят от размеров экрана
        assert header_btn_collapse is not None and header_btn_collapse.is_visible()
        assert header_btn_main is not None and header_btn_main.is_visible()
        assert header_btn_main.inner_text()=='Главная'
        href = header_btn_main.get_attribute("href")
        assert href=="/"
        assert header_btn_predict_swim is not None and header_btn_predict_swim.is_visible()
        assert header_btn_predict_swim.inner_text()=='Предсказать заплыв'
        href = header_btn_predict_swim.get_attribute("href")
        assert href=="" or href is None
        assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
        assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
        href = header_btn_predict_discipline.get_attribute("href")
        assert href=="discipline"
        
        #Проверка элементов которых не должно быть видно (сообщения об ошибках ввода, модальные окна)
        assert not graphs_modal.is_visible()
        assert not card1_style_invalid_feedback.is_visible()
        assert not card1_distance_invalid_feedback.is_visible()
        assert not card1_sex_invalid_feedback.is_visible()
        assert not card1_phase_invalid_feedback.is_visible()
        assert not card1_pool_length_invalid_feedback.is_visible()
        assert not card1_datetime_invalid_feedback.is_visible()
        assert not card1_host_country_invalid_feedback.is_visible()
        assert not card2_swimmers_invalid_alert.is_visible()
        #Проверка элементов которых не должно существовать (результаты заплыва, тосты с ошибками сети)
        assert toasts_count==0
        assert visible_result_cards_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при разворачивании и сворачивании меню в шапке на маленьких экранах
    def test_all_elements_present_and_have_required_text_after_expand_collapse_header_menu(self,base_url,page:Page,viewport):
        if page.viewport_size['width']>=1200: #Если размер страницы большой - работать с меню нельзя!
            return
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+SWIM_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Развернуть и свернуть сворачивающееся меню в шапке
        page.locator("button.navbar-toggler").first.click()
        page.wait_for_timeout(600)  # Ждем анимацию
        page.locator("button.navbar-toggler").first.click()
        page.wait_for_timeout(600)  # Ждем анимацию
        try:
            header_title=page.locator("nav").get_by_text('Система прогноза результатов по плаванию').first
        except:
            header_title=None
        try:
            header_btn_main=page.locator("nav").get_by_text("Главная").first
        except:
            header_btn_main=None
        try:
            header_btn_predict_swim=page.locator("nav").get_by_text("Предсказать заплыв").first
        except:
            header_btn_predict_swim=None
        try:
            header_btn_predict_discipline=page.locator("nav").get_by_text("Предсказать дисциплину").first
        except:
            header_btn_predict_discipline=None
        try:
            header_btn_collapse=page.locator("button.navbar-toggler").first
        except:
            header_btn_collapse=None
        
        try:
            card1_title=page.get_by_text('Введите сведения о заплыве').first
        except:
            card1_title=None
        try:
            card1_style_label=page.get_by_text('Стиль плавания:').first
        except:
            card1_style_label=None
        try:
            card1_distance_label=page.get_by_text('Дистанция:').first
        except:
            card1_distance_label=None
        try:
            card1_sex_label=page.get_by_text('Пол:').first
        except:
            card1_sex_label=None
        try:
            card1_phase_label=page.get_by_text('Фаза:').first
        except:
            card1_phase_label=None
        try:
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_datetime_label=page.get_by_text('Местная дата и время заплыва:').first
        except:
            card1_datetime_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_style_select=page.locator('select').filter(has_text="Выберите стиль").first
        except:
            card1_style_select=None
        try:
            card1_distance_select=page.locator('select').filter(has_text="Выберите дистанцию").first
        except:
            card1_distance_select=None
        try:
            card1_sex_select=page.locator('select').filter(has_text="Выберите пол").first
        except:
            card1_sex_select=None
        try:
            card1_phase_select=page.locator('select').filter(has_text="Выберите фазу заплыва").first
        except:
            card1_phase_select=None
        try:
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_datetime_input=page.locator("input[type='datetime-local']").first
        except:
            card1_datetime_input=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        
        try:
            card2_title=page.get_by_text('Введите сведения о пловцах заплыва').first
        except:
            card2_title=None
        try:
            card2_lane_header=page.get_by_text('Дорожка').first
        except:
            card2_lane_header=None
        try:
            card2_swimmer_header=page.get_by_text('Пловец').first
        except:
            card2_swimmer_header=None
        try:
            card2_lane_0_label=page.get_by_text('0',exact=True).first
        except:
            card2_lane_0_label=None
        try:
            card2_lane_1_label=page.get_by_text('1',exact=True).first
        except:
            card2_lane_1_label=None
        try:
            card2_lane_2_label=page.get_by_text('2',exact=True).first
        except:
            card2_lane_2_label=None
        try:
            card2_lane_3_label=page.get_by_text('3',exact=True).first
        except:
            card2_lane_3_label=None
        try:
            card2_lane_4_label=page.get_by_text('4',exact=True).first
        except:
            card2_lane_4_label=None
        try:
            card2_lane_5_label=page.get_by_text('5',exact=True).first
        except:
            card2_lane_5_label=None
        try:
            card2_lane_6_label=page.get_by_text('6',exact=True).first
        except:
            card2_lane_6_label=None
        try:
            card2_lane_7_label=page.get_by_text('7',exact=True).first
        except:
            card2_lane_7_label=None
        try:
            card2_lane_8_label=page.get_by_text('8',exact=True).first
        except:
            card2_lane_8_label=None
        try:
            card2_lane_9_label=page.get_by_text('9',exact=True).first
        except:
            card2_lane_9_label=None
        try:
            card2_lane_0_swimmer_select=page.locator('select').filter(has_text='Нет пловца').first
        except:
            card2_lane_0_swimmer_select=None
        try:
            card2_lane_1_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(1)
        except:
            card2_lane_1_swimmer_select=None
        try:
            card2_lane_2_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(2)
        except:
            card2_lane_2_swimmer_select=None
        try:
            card2_lane_3_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(3)
        except:
            card2_lane_3_swimmer_select=None
        try:
            card2_lane_4_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(4)
        except:
            card2_lane_4_swimmer_select=None
        try:
            card2_lane_5_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(5)
        except:
            card2_lane_5_swimmer_select=None
        try:
            card2_lane_6_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(6)
        except:
            card2_lane_6_swimmer_select=None
        try:
            card2_lane_7_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(7)
        except:
            card2_lane_7_swimmer_select=None
        try:
            card2_lane_8_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(8)
        except:
            card2_lane_8_swimmer_select=None
        try:
            card2_lane_9_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(9)
        except:
            card2_lane_9_swimmer_select=None
            
        try:
            btn_predict=page.get_by_text("Предсказать",exact=True)
        except:
            btn_predict=None
        
        try:
            card1_style_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите стиль плавания!").first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите дистанцию!").first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите пол!").first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_phase_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите фазу!").first
        except:
            card1_phase_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите длину бассейна!").first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_datetime_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите дату и время заплыва (от 2026 до 2050 года)!").first
        except:
            card1_datetime_invalid_feedback=None
        try:
            card1_host_country_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите страну заплыва!").first
        except:
            card1_host_country_invalid_feedback=None
        try:
            card2_swimmers_invalid_alert=page.locator('div.alert')
        except:
            card2_swimmers_invalid_alert=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_cards_count=page.locator("[id^='swimmer'][id$='Results']").filter(visible=True).count() #Число выходных карточек
        except:
            visible_result_cards_count=0
        
        try:
            toasts_count=page.locator("div.toast").count()
        except:
            toasts_count=0
        
        
        
        
        
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о заплыве"
        expect(card1_title).to_have_js_property("tagName","DIV")
        assert(card1_style_label) is not None and card1_style_label.is_visible()
        assert card1_style_label.inner_text()=="Стиль плавания:"
        expect(card1_style_label).to_have_js_property("tagName","LABEL")
        assert(card1_distance_label) is not None and card1_distance_label.is_visible()
        assert card1_distance_label.inner_text()=="Дистанция:"
        expect(card1_distance_label).to_have_js_property("tagName","LABEL")
        assert(card1_sex_label) is not None and card1_sex_label.is_visible()
        assert card1_sex_label.inner_text()=="Пол:"
        expect(card1_sex_label).to_have_js_property("tagName","LABEL")
        assert(card1_phase_label) is not None and card1_phase_label.is_visible()
        assert card1_phase_label.inner_text()=="Фаза:"
        expect(card1_phase_label).to_have_js_property("tagName","LABEL")
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_datetime_label) is not None and card1_datetime_label.is_visible()
        assert card1_datetime_label.inner_text()=="Местная дата и время заплыва:"
        expect(card1_datetime_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select).to_have_value("")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select).to_have_value("")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select).to_have_value("")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_phase_select) is not None and card1_phase_select.is_visible()
        expect(card1_phase_select).to_have_value("")
        expect(card1_phase_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select).to_have_value("")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_datetime_input) is not None and card1_datetime_input.is_visible()
        expect(card1_datetime_input).to_have_attribute("type","datetime-local")
        expect(card1_datetime_input).to_have_js_property("tagName","INPUT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select).to_have_value("")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        
        assert(card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите сведения о пловцах заплыва"
        expect(card2_title).to_have_js_property("tagName","DIV")
        assert(card2_lane_header) is not None and card2_lane_header.is_visible()
        assert card2_lane_header.inner_text()=="Дорожка"
        expect(card2_lane_header).to_have_js_property("tagName","LABEL")
        assert(card2_swimmer_header) is not None and card2_swimmer_header.is_visible()
        assert card2_swimmer_header.inner_text()=="Пловец"
        expect(card2_swimmer_header).to_have_js_property("tagName","LABEL")
        assert(card2_lane_0_label) is not None and card2_lane_0_label.is_visible()
        assert card2_lane_0_label.inner_text()=="0"
        expect(card2_lane_0_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_1_label) is not None and card2_lane_1_label.is_visible()
        assert card2_lane_1_label.inner_text()=="1"
        expect(card2_lane_1_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_2_label) is not None and card2_lane_2_label.is_visible()
        assert card2_lane_2_label.inner_text()=="2"
        expect(card2_lane_2_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_3_label) is not None and card2_lane_3_label.is_visible()
        assert card2_lane_3_label.inner_text()=="3"
        expect(card2_lane_3_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_4_label) is not None and card2_lane_4_label.is_visible()
        assert card2_lane_4_label.inner_text()=="4"
        expect(card2_lane_4_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_5_label) is not None and card2_lane_5_label.is_visible()
        assert card2_lane_5_label.inner_text()=="5"
        expect(card2_lane_5_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_6_label) is not None and card2_lane_6_label.is_visible()
        assert card2_lane_6_label.inner_text()=="6"
        expect(card2_lane_6_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_7_label) is not None and card2_lane_7_label.is_visible()
        assert card2_lane_7_label.inner_text()=="7"
        expect(card2_lane_7_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_8_label) is not None and card2_lane_8_label.is_visible()
        assert card2_lane_8_label.inner_text()=="8"
        expect(card2_lane_8_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_9_label) is not None and card2_lane_9_label.is_visible()
        assert card2_lane_9_label.inner_text()=="9"
        expect(card2_lane_9_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_0_swimmer_select) is not None and card2_lane_0_swimmer_select.is_visible()
        expect(card2_lane_0_swimmer_select).to_have_value("")
        expect(card2_lane_0_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_1_swimmer_select) is not None and card2_lane_1_swimmer_select.is_visible()
        expect(card2_lane_1_swimmer_select).to_have_value("")
        expect(card2_lane_1_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_2_swimmer_select) is not None and card2_lane_2_swimmer_select.is_visible()
        expect(card2_lane_2_swimmer_select).to_have_value("")
        expect(card2_lane_2_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_3_swimmer_select) is not None and card2_lane_3_swimmer_select.is_visible()
        expect(card2_lane_3_swimmer_select).to_have_value("")
        expect(card2_lane_3_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_4_swimmer_select) is not None and card2_lane_4_swimmer_select.is_visible()
        expect(card2_lane_4_swimmer_select).to_have_value("")
        expect(card2_lane_4_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_5_swimmer_select) is not None and card2_lane_5_swimmer_select.is_visible()
        expect(card2_lane_5_swimmer_select).to_have_value("")
        expect(card2_lane_5_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_6_swimmer_select) is not None and card2_lane_6_swimmer_select.is_visible()
        expect(card2_lane_6_swimmer_select).to_have_value("")
        expect(card2_lane_6_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_7_swimmer_select) is not None and card2_lane_7_swimmer_select.is_visible()
        expect(card2_lane_7_swimmer_select).to_have_value("")
        expect(card2_lane_7_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_8_swimmer_select) is not None and card2_lane_8_swimmer_select.is_visible()
        expect(card2_lane_8_swimmer_select).to_have_value("")
        expect(card2_lane_8_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_9_swimmer_select) is not None and card2_lane_9_swimmer_select.is_visible()
        expect(card2_lane_9_swimmer_select).to_have_value("")
        expect(card2_lane_9_swimmer_select).to_have_js_property("tagName","SELECT")
        
        assert(btn_predict) is not None and btn_predict.is_visible()
        expect(btn_predict).to_have_text("Предсказать")
        expect(btn_predict).to_have_js_property("tagName","BUTTON")
        
        
        #Проверка элементов которые зависят от размеров экрана
        assert header_btn_collapse is not None and header_btn_collapse.is_visible()
        assert header_btn_main is None or not header_btn_main.is_visible()
        assert header_btn_predict_swim is None or not header_btn_predict_swim.is_visible()
        assert header_btn_predict_discipline is None or not header_btn_predict_discipline.is_visible()
        
        
        #Проверка элементов которых не должно быть видно (сообщения об ошибках ввода, модальные окна)
        assert not graphs_modal.is_visible()
        assert not card1_style_invalid_feedback.is_visible()
        assert not card1_distance_invalid_feedback.is_visible()
        assert not card1_sex_invalid_feedback.is_visible()
        assert not card1_phase_invalid_feedback.is_visible()
        assert not card1_pool_length_invalid_feedback.is_visible()
        assert not card1_datetime_invalid_feedback.is_visible()
        assert not card1_host_country_invalid_feedback.is_visible()
        assert not card2_swimmers_invalid_alert.is_visible()
        #Проверка элементов которых не должно существовать (результаты заплыва, тосты с ошибками сети)
        assert toasts_count==0
        assert visible_result_cards_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии по кнопке Предсказания без заполнения полей
    def test_all_elements_present_and_have_required_text_after_predict_click_no_input_for_fields(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+SWIM_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        page.get_by_text("Предсказать",exact=True).first.click() #Нажать по кнопке предсказания
        page.wait_for_timeout(600)  # Ждем анимацию
        
        try:
            header_title=page.locator("nav").get_by_text('Система прогноза результатов по плаванию').first
        except:
            header_title=None
        try:
            header_btn_main=page.locator("nav").get_by_text("Главная").first
        except:
            header_btn_main=None
        try:
            header_btn_predict_swim=page.locator("nav").get_by_text("Предсказать заплыв").first
        except:
            header_btn_predict_swim=None
        try:
            header_btn_predict_discipline=page.locator("nav").get_by_text("Предсказать дисциплину").first
        except:
            header_btn_predict_discipline=None
        try:
            header_btn_collapse=page.locator("button.navbar-toggler").first
        except:
            header_btn_collapse=None
        
        try:
            card1_title=page.get_by_text('Введите сведения о заплыве').first
        except:
            card1_title=None
        try:
            card1_style_label=page.get_by_text('Стиль плавания:').first
        except:
            card1_style_label=None
        try:
            card1_distance_label=page.get_by_text('Дистанция:').first
        except:
            card1_distance_label=None
        try:
            card1_sex_label=page.get_by_text('Пол:').first
        except:
            card1_sex_label=None
        try:
            card1_phase_label=page.get_by_text('Фаза:').first
        except:
            card1_phase_label=None
        try:
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_datetime_label=page.get_by_text('Местная дата и время заплыва:').first
        except:
            card1_datetime_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_style_select=page.locator('select').filter(has_text="Выберите стиль").first
        except:
            card1_style_select=None
        try:
            card1_distance_select=page.locator('select').filter(has_text="Выберите дистанцию").first
        except:
            card1_distance_select=None
        try:
            card1_sex_select=page.locator('select').filter(has_text="Выберите пол").first
        except:
            card1_sex_select=None
        try:
            card1_phase_select=page.locator('select').filter(has_text="Выберите фазу заплыва").first
        except:
            card1_phase_select=None
        try:
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_datetime_input=page.locator("input[type='datetime-local']").first
        except:
            card1_datetime_input=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        
        try:
            card2_title=page.get_by_text('Введите сведения о пловцах заплыва').first
        except:
            card2_title=None
        try:
            card2_lane_header=page.get_by_text('Дорожка').first
        except:
            card2_lane_header=None
        try:
            card2_swimmer_header=page.get_by_text('Пловец').first
        except:
            card2_swimmer_header=None
        try:
            card2_lane_0_label=page.get_by_text('0',exact=True).first
        except:
            card2_lane_0_label=None
        try:
            card2_lane_1_label=page.get_by_text('1',exact=True).first
        except:
            card2_lane_1_label=None
        try:
            card2_lane_2_label=page.get_by_text('2',exact=True).first
        except:
            card2_lane_2_label=None
        try:
            card2_lane_3_label=page.get_by_text('3',exact=True).first
        except:
            card2_lane_3_label=None
        try:
            card2_lane_4_label=page.get_by_text('4',exact=True).first
        except:
            card2_lane_4_label=None
        try:
            card2_lane_5_label=page.get_by_text('5',exact=True).first
        except:
            card2_lane_5_label=None
        try:
            card2_lane_6_label=page.get_by_text('6',exact=True).first
        except:
            card2_lane_6_label=None
        try:
            card2_lane_7_label=page.get_by_text('7',exact=True).first
        except:
            card2_lane_7_label=None
        try:
            card2_lane_8_label=page.get_by_text('8',exact=True).first
        except:
            card2_lane_8_label=None
        try:
            card2_lane_9_label=page.get_by_text('9',exact=True).first
        except:
            card2_lane_9_label=None
        try:
            card2_lane_0_swimmer_select=page.locator('select').filter(has_text='Нет пловца').first
        except:
            card2_lane_0_swimmer_select=None
        try:
            card2_lane_1_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(1)
        except:
            card2_lane_1_swimmer_select=None
        try:
            card2_lane_2_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(2)
        except:
            card2_lane_2_swimmer_select=None
        try:
            card2_lane_3_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(3)
        except:
            card2_lane_3_swimmer_select=None
        try:
            card2_lane_4_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(4)
        except:
            card2_lane_4_swimmer_select=None
        try:
            card2_lane_5_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(5)
        except:
            card2_lane_5_swimmer_select=None
        try:
            card2_lane_6_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(6)
        except:
            card2_lane_6_swimmer_select=None
        try:
            card2_lane_7_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(7)
        except:
            card2_lane_7_swimmer_select=None
        try:
            card2_lane_8_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(8)
        except:
            card2_lane_8_swimmer_select=None
        try:
            card2_lane_9_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(9)
        except:
            card2_lane_9_swimmer_select=None
            
        try:
            btn_predict=page.get_by_text("Предсказать",exact=True)
        except:
            btn_predict=None
        
        try:
            card1_style_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите стиль плавания!").first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите дистанцию!").first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите пол!").first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_phase_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите фазу!").first
        except:
            card1_phase_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите длину бассейна!").first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_datetime_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите дату и время заплыва (от 2026 до 2050 года)!").first
        except:
            card1_datetime_invalid_feedback=None
        try:
            card1_host_country_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите страну заплыва!").first
        except:
            card1_host_country_invalid_feedback=None
        try:
            card2_swimmers_invalid_alert=page.locator('div.alert')
        except:
            card2_swimmers_invalid_alert=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_cards_count=page.locator("[id^='swimmer'][id$='Results']").filter(visible=True).count() #Число выходных карточек
        except:
            visible_result_cards_count=0
        
        try:
            toasts_count=page.locator("div.toast").count()
        except:
            toasts_count=0
        
        
        
        
        
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о заплыве"
        expect(card1_title).to_have_js_property("tagName","DIV")
        assert(card1_style_label) is not None and card1_style_label.is_visible()
        assert card1_style_label.inner_text()=="Стиль плавания:"
        expect(card1_style_label).to_have_js_property("tagName","LABEL")
        assert(card1_distance_label) is not None and card1_distance_label.is_visible()
        assert card1_distance_label.inner_text()=="Дистанция:"
        expect(card1_distance_label).to_have_js_property("tagName","LABEL")
        assert(card1_sex_label) is not None and card1_sex_label.is_visible()
        assert card1_sex_label.inner_text()=="Пол:"
        expect(card1_sex_label).to_have_js_property("tagName","LABEL")
        assert(card1_phase_label) is not None and card1_phase_label.is_visible()
        assert card1_phase_label.inner_text()=="Фаза:"
        expect(card1_phase_label).to_have_js_property("tagName","LABEL")
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_datetime_label) is not None and card1_datetime_label.is_visible()
        assert card1_datetime_label.inner_text()=="Местная дата и время заплыва:"
        expect(card1_datetime_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select).to_have_value("")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select).to_have_value("")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select).to_have_value("")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_phase_select) is not None and card1_phase_select.is_visible()
        expect(card1_phase_select).to_have_value("")
        expect(card1_phase_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select).to_have_value("")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_datetime_input) is not None and card1_datetime_input.is_visible()
        expect(card1_datetime_input).to_have_attribute("type","datetime-local")
        expect(card1_datetime_input).to_have_js_property("tagName","INPUT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select).to_have_value("")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        
        assert(card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите сведения о пловцах заплыва"
        expect(card2_title).to_have_js_property("tagName","DIV")
        assert(card2_lane_header) is not None and card2_lane_header.is_visible()
        assert card2_lane_header.inner_text()=="Дорожка"
        expect(card2_lane_header).to_have_js_property("tagName","LABEL")
        assert(card2_swimmer_header) is not None and card2_swimmer_header.is_visible()
        assert card2_swimmer_header.inner_text()=="Пловец"
        expect(card2_swimmer_header).to_have_js_property("tagName","LABEL")
        assert(card2_lane_0_label) is not None and card2_lane_0_label.is_visible()
        assert card2_lane_0_label.inner_text()=="0"
        expect(card2_lane_0_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_1_label) is not None and card2_lane_1_label.is_visible()
        assert card2_lane_1_label.inner_text()=="1"
        expect(card2_lane_1_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_2_label) is not None and card2_lane_2_label.is_visible()
        assert card2_lane_2_label.inner_text()=="2"
        expect(card2_lane_2_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_3_label) is not None and card2_lane_3_label.is_visible()
        assert card2_lane_3_label.inner_text()=="3"
        expect(card2_lane_3_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_4_label) is not None and card2_lane_4_label.is_visible()
        assert card2_lane_4_label.inner_text()=="4"
        expect(card2_lane_4_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_5_label) is not None and card2_lane_5_label.is_visible()
        assert card2_lane_5_label.inner_text()=="5"
        expect(card2_lane_5_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_6_label) is not None and card2_lane_6_label.is_visible()
        assert card2_lane_6_label.inner_text()=="6"
        expect(card2_lane_6_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_7_label) is not None and card2_lane_7_label.is_visible()
        assert card2_lane_7_label.inner_text()=="7"
        expect(card2_lane_7_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_8_label) is not None and card2_lane_8_label.is_visible()
        assert card2_lane_8_label.inner_text()=="8"
        expect(card2_lane_8_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_9_label) is not None and card2_lane_9_label.is_visible()
        assert card2_lane_9_label.inner_text()=="9"
        expect(card2_lane_9_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_0_swimmer_select) is not None and card2_lane_0_swimmer_select.is_visible()
        expect(card2_lane_0_swimmer_select).to_have_value("")
        expect(card2_lane_0_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_1_swimmer_select) is not None and card2_lane_1_swimmer_select.is_visible()
        expect(card2_lane_1_swimmer_select).to_have_value("")
        expect(card2_lane_1_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_2_swimmer_select) is not None and card2_lane_2_swimmer_select.is_visible()
        expect(card2_lane_2_swimmer_select).to_have_value("")
        expect(card2_lane_2_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_3_swimmer_select) is not None and card2_lane_3_swimmer_select.is_visible()
        expect(card2_lane_3_swimmer_select).to_have_value("")
        expect(card2_lane_3_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_4_swimmer_select) is not None and card2_lane_4_swimmer_select.is_visible()
        expect(card2_lane_4_swimmer_select).to_have_value("")
        expect(card2_lane_4_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_5_swimmer_select) is not None and card2_lane_5_swimmer_select.is_visible()
        expect(card2_lane_5_swimmer_select).to_have_value("")
        expect(card2_lane_5_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_6_swimmer_select) is not None and card2_lane_6_swimmer_select.is_visible()
        expect(card2_lane_6_swimmer_select).to_have_value("")
        expect(card2_lane_6_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_7_swimmer_select) is not None and card2_lane_7_swimmer_select.is_visible()
        expect(card2_lane_7_swimmer_select).to_have_value("")
        expect(card2_lane_7_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_8_swimmer_select) is not None and card2_lane_8_swimmer_select.is_visible()
        expect(card2_lane_8_swimmer_select).to_have_value("")
        expect(card2_lane_8_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_9_swimmer_select) is not None and card2_lane_9_swimmer_select.is_visible()
        expect(card2_lane_9_swimmer_select).to_have_value("")
        expect(card2_lane_9_swimmer_select).to_have_js_property("tagName","SELECT")
        
        assert(btn_predict) is not None and btn_predict.is_visible()
        expect(btn_predict).to_have_text("Предсказать")
        expect(btn_predict).to_have_js_property("tagName","BUTTON")
        
        if page.viewport_size['width']<1200:  #Если размер экрана по горизонтали маленький, должна появиться кнопка для сворачивания кнопок меню
            assert header_btn_predict_swim is None or not header_btn_predict_swim.is_visible()
            assert header_btn_predict_discipline is None or not header_btn_predict_discipline.is_visible()
            assert header_btn_main is None or not header_btn_main.is_visible()
            assert header_btn_collapse is not None and header_btn_collapse.is_visible()
        else:
            assert header_btn_collapse is None or not header_btn_collapse.is_visible()
            assert header_btn_main is not None and header_btn_main.is_visible()
            assert header_btn_main.inner_text()=='Главная'
            href = header_btn_main.get_attribute("href")
            assert href=="/"
            assert header_btn_predict_swim is not None and header_btn_predict_swim.is_visible()
            assert header_btn_predict_swim.inner_text()=='Предсказать заплыв'
            href = header_btn_predict_swim.get_attribute("href")
            assert href=="" or href is None
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="discipline"
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка элементов которые должны быть видны (сообщения об ошибках ввода)
        assert card1_style_invalid_feedback.is_visible()
        assert card1_style_invalid_feedback.inner_text()=="Выберите стиль плавания!"
        assert card1_distance_invalid_feedback.is_visible()
        assert card1_distance_invalid_feedback.inner_text()=="Выберите дистанцию!"
        assert card1_sex_invalid_feedback.is_visible()
        assert card1_sex_invalid_feedback.inner_text()=="Выберите пол!"
        assert card1_phase_invalid_feedback.is_visible()
        assert card1_phase_invalid_feedback.inner_text()=="Выберите фазу!"
        assert card1_pool_length_invalid_feedback.is_visible()
        assert card1_pool_length_invalid_feedback.inner_text()=="Выберите длину бассейна!"
        assert card1_datetime_invalid_feedback.is_visible()
        assert card1_datetime_invalid_feedback.inner_text()=="Выберите дату и время заплыва (от 2026 до 2050 года)!"
        assert card1_host_country_invalid_feedback.is_visible()
        assert card1_host_country_invalid_feedback.inner_text()=="Выберите страну заплыва!"
        assert card2_swimmers_invalid_alert.is_visible()
        assert card2_swimmers_invalid_alert.inner_text()=="В заплыве должен быть выбран хотя бы один пловец!"
        
        #Проверка элементов которых не должно существовать (результаты заплыва, тосты с ошибками сети)
        assert toasts_count==0
        assert visible_result_cards_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии по кнопке Предсказания при неправильном заполнении полей
    # (слишком ранняя дата заплыва, дупликаты пловцов), а именно:
    #Стиль плавания - баттерфляй
    #Дистанция - 100м
    #Пол - Мужской
    #Фаза - Отборочные
    #Длина бассейна - 50м
    #Дата и время заплвыва - 31.12.2025 23:59:59
    #Страна проведения - Австралия
    #Пловец на дорожке 0 - LIENDO Josh
    #Пловец на дорожке 1 - LIENDO Josh
    def test_all_elements_present_and_have_required_text_after_predict_click_invalid_input_too_early_date_duplicate_swimmer(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+SWIM_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.set_default_timeout(3000)
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Выбрать необходимые данные
        page.select_option("select#selectStyle",label="Баттерфляй")
        page.select_option("select#selectDistance",label="100м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPhase",label="Отборочные")
        page.select_option("select#selectPoolLength",label="50м")
        page.fill("input[type='datetime-local']", "2025-12-31T23:59:59")
        page.select_option("select#selectHostCountry",label="Австралия")
        page.locator("#selectSwimmer0 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer0 + .ts-wrapper input").fill("LIENDO")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer0 + .ts-wrapper .ts-dropdown .option", has_text="LIENDO Josh").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmer1 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer1 + .ts-wrapper input").fill("LIENDO")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer1 + .ts-wrapper .ts-dropdown .option", has_text="LIENDO Josh").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.get_by_text("Предсказать",exact=True).first.click() #Нажать по кнопке предсказания
        page.wait_for_timeout(600)  # Ждем анимацию
        
        try:
            header_title=page.locator("nav").get_by_text('Система прогноза результатов по плаванию').first
        except:
            header_title=None
        try:
            header_btn_main=page.locator("nav").get_by_text("Главная").first
        except:
            header_btn_main=None
        try:
            header_btn_predict_swim=page.locator("nav").get_by_text("Предсказать заплыв").first
        except:
            header_btn_predict_swim=None
        try:
            header_btn_predict_discipline=page.locator("nav").get_by_text("Предсказать дисциплину").first
        except:
            header_btn_predict_discipline=None
        try:
            header_btn_collapse=page.locator("button.navbar-toggler").first
        except:
            header_btn_collapse=None
        
        try:
            card1_title=page.get_by_text('Введите сведения о заплыве').first
        except:
            card1_title=None
        try:
            card1_style_label=page.get_by_text('Стиль плавания:').first
        except:
            card1_style_label=None
        try:
            card1_distance_label=page.get_by_text('Дистанция:').first
        except:
            card1_distance_label=None
        try:
            card1_sex_label=page.get_by_text('Пол:').first
        except:
            card1_sex_label=None
        try:
            card1_phase_label=page.get_by_text('Фаза:').first
        except:
            card1_phase_label=None
        try:
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_datetime_label=page.get_by_text('Местная дата и время заплыва:').first
        except:
            card1_datetime_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_style_select=page.locator('select').filter(has_text="Выберите стиль").first
        except:
            card1_style_select=None
        try:
            card1_distance_select=page.locator('select').filter(has_text="Выберите дистанцию").first
        except:
            card1_distance_select=None
        try:
            card1_sex_select=page.locator('select').filter(has_text="Выберите пол").first
        except:
            card1_sex_select=None
        try:
            card1_phase_select=page.locator('select').filter(has_text="Выберите фазу заплыва").first
        except:
            card1_phase_select=None
        try:
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_datetime_input=page.locator("input[type='datetime-local']").first
        except:
            card1_datetime_input=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        
        try:
            card2_title=page.get_by_text('Введите сведения о пловцах заплыва').first
        except:
            card2_title=None
        try:
            card2_lane_header=page.get_by_text('Дорожка').first
        except:
            card2_lane_header=None
        try:
            card2_swimmer_header=page.get_by_text('Пловец').first
        except:
            card2_swimmer_header=None
        try:
            card2_lane_0_label=page.get_by_text('0',exact=True).first
        except:
            card2_lane_0_label=None
        try:
            card2_lane_1_label=page.get_by_text('1',exact=True).first
        except:
            card2_lane_1_label=None
        try:
            card2_lane_2_label=page.get_by_text('2',exact=True).first
        except:
            card2_lane_2_label=None
        try:
            card2_lane_3_label=page.get_by_text('3',exact=True).first
        except:
            card2_lane_3_label=None
        try:
            card2_lane_4_label=page.get_by_text('4',exact=True).first
        except:
            card2_lane_4_label=None
        try:
            card2_lane_5_label=page.get_by_text('5',exact=True).first
        except:
            card2_lane_5_label=None
        try:
            card2_lane_6_label=page.get_by_text('6',exact=True).first
        except:
            card2_lane_6_label=None
        try:
            card2_lane_7_label=page.get_by_text('7',exact=True).first
        except:
            card2_lane_7_label=None
        try:
            card2_lane_8_label=page.get_by_text('8',exact=True).first
        except:
            card2_lane_8_label=None
        try:
            card2_lane_9_label=page.get_by_text('9',exact=True).first
        except:
            card2_lane_9_label=None
        try:
            card2_lane_0_swimmer_select=page.locator('select').filter(has_text='Нет пловца').first
        except:
            card2_lane_0_swimmer_select=None
        try:
            card2_lane_1_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(1)
        except:
            card2_lane_1_swimmer_select=None
        try:
            card2_lane_2_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(2)
        except:
            card2_lane_2_swimmer_select=None
        try:
            card2_lane_3_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(3)
        except:
            card2_lane_3_swimmer_select=None
        try:
            card2_lane_4_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(4)
        except:
            card2_lane_4_swimmer_select=None
        try:
            card2_lane_5_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(5)
        except:
            card2_lane_5_swimmer_select=None
        try:
            card2_lane_6_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(6)
        except:
            card2_lane_6_swimmer_select=None
        try:
            card2_lane_7_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(7)
        except:
            card2_lane_7_swimmer_select=None
        try:
            card2_lane_8_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(8)
        except:
            card2_lane_8_swimmer_select=None
        try:
            card2_lane_9_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(9)
        except:
            card2_lane_9_swimmer_select=None
            
        try:
            btn_predict=page.get_by_text("Предсказать",exact=True)
        except:
            btn_predict=None
        
        try:
            card1_style_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите стиль плавания!").first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите дистанцию!").first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите пол!").first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_phase_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите фазу!").first
        except:
            card1_phase_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите длину бассейна!").first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_datetime_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите дату и время заплыва (от 2026 до 2050 года)!").first
        except:
            card1_datetime_invalid_feedback=None
        try:
            card1_host_country_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите страну заплыва!").first
        except:
            card1_host_country_invalid_feedback=None
        try:
            card2_swimmers_invalid_alert=page.locator('div.alert')
        except:
            card2_swimmers_invalid_alert=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_cards_count=page.locator("[id^='swimmer'][id$='Results']").filter(visible=True).count() #Число выходных карточек
        except:
            visible_result_cards_count=0
        
        try:
            toasts_count=page.locator("div.toast").count()
        except:
            toasts_count=0
        
        
        
        
        
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о заплыве"
        expect(card1_title).to_have_js_property("tagName","DIV")
        assert(card1_style_label) is not None and card1_style_label.is_visible()
        assert card1_style_label.inner_text()=="Стиль плавания:"
        expect(card1_style_label).to_have_js_property("tagName","LABEL")
        assert(card1_distance_label) is not None and card1_distance_label.is_visible()
        assert card1_distance_label.inner_text()=="Дистанция:"
        expect(card1_distance_label).to_have_js_property("tagName","LABEL")
        assert(card1_sex_label) is not None and card1_sex_label.is_visible()
        assert card1_sex_label.inner_text()=="Пол:"
        expect(card1_sex_label).to_have_js_property("tagName","LABEL")
        assert(card1_phase_label) is not None and card1_phase_label.is_visible()
        assert card1_phase_label.inner_text()=="Фаза:"
        expect(card1_phase_label).to_have_js_property("tagName","LABEL")
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_datetime_label) is not None and card1_datetime_label.is_visible()
        assert card1_datetime_label.inner_text()=="Местная дата и время заплыва:"
        expect(card1_datetime_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Баттерфляй")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("100м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_phase_select) is not None and card1_phase_select.is_visible()
        expect(card1_phase_select.locator("option:checked")).to_have_text("Отборочные")
        expect(card1_phase_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("50м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_datetime_input) is not None and card1_datetime_input.is_visible()
        expect(card1_datetime_input).to_have_value("2025-12-31T23:59:59")
        expect(card1_datetime_input).to_have_attribute("type","datetime-local")
        expect(card1_datetime_input).to_have_js_property("tagName","INPUT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Австралия")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        
        assert(card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите сведения о пловцах заплыва"
        expect(card2_title).to_have_js_property("tagName","DIV")
        assert(card2_lane_header) is not None and card2_lane_header.is_visible()
        assert card2_lane_header.inner_text()=="Дорожка"
        expect(card2_lane_header).to_have_js_property("tagName","LABEL")
        assert(card2_swimmer_header) is not None and card2_swimmer_header.is_visible()
        assert card2_swimmer_header.inner_text()=="Пловец"
        expect(card2_swimmer_header).to_have_js_property("tagName","LABEL")
        assert(card2_lane_0_label) is not None and card2_lane_0_label.is_visible()
        assert card2_lane_0_label.inner_text()=="0"
        expect(card2_lane_0_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_1_label) is not None and card2_lane_1_label.is_visible()
        assert card2_lane_1_label.inner_text()=="1"
        expect(card2_lane_1_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_2_label) is not None and card2_lane_2_label.is_visible()
        assert card2_lane_2_label.inner_text()=="2"
        expect(card2_lane_2_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_3_label) is not None and card2_lane_3_label.is_visible()
        assert card2_lane_3_label.inner_text()=="3"
        expect(card2_lane_3_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_4_label) is not None and card2_lane_4_label.is_visible()
        assert card2_lane_4_label.inner_text()=="4"
        expect(card2_lane_4_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_5_label) is not None and card2_lane_5_label.is_visible()
        assert card2_lane_5_label.inner_text()=="5"
        expect(card2_lane_5_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_6_label) is not None and card2_lane_6_label.is_visible()
        assert card2_lane_6_label.inner_text()=="6"
        expect(card2_lane_6_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_7_label) is not None and card2_lane_7_label.is_visible()
        assert card2_lane_7_label.inner_text()=="7"
        expect(card2_lane_7_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_8_label) is not None and card2_lane_8_label.is_visible()
        assert card2_lane_8_label.inner_text()=="8"
        expect(card2_lane_8_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_9_label) is not None and card2_lane_9_label.is_visible()
        assert card2_lane_9_label.inner_text()=="9"
        expect(card2_lane_9_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_0_swimmer_select) is not None and card2_lane_0_swimmer_select.is_visible()
        expect(card2_lane_0_swimmer_select.locator("option:checked")).to_have_text("LIENDO Josh")
        expect(card2_lane_0_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_1_swimmer_select) is not None and card2_lane_1_swimmer_select.is_visible()
        expect(card2_lane_1_swimmer_select.locator("option:checked")).to_have_text("LIENDO Josh")
        expect(card2_lane_1_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_2_swimmer_select) is not None and card2_lane_2_swimmer_select.is_visible()
        expect(card2_lane_2_swimmer_select).to_have_value("")
        expect(card2_lane_2_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_3_swimmer_select) is not None and card2_lane_3_swimmer_select.is_visible()
        expect(card2_lane_3_swimmer_select).to_have_value("")
        expect(card2_lane_3_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_4_swimmer_select) is not None and card2_lane_4_swimmer_select.is_visible()
        expect(card2_lane_4_swimmer_select).to_have_value("")
        expect(card2_lane_4_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_5_swimmer_select) is not None and card2_lane_5_swimmer_select.is_visible()
        expect(card2_lane_5_swimmer_select).to_have_value("")
        expect(card2_lane_5_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_6_swimmer_select) is not None and card2_lane_6_swimmer_select.is_visible()
        expect(card2_lane_6_swimmer_select).to_have_value("")
        expect(card2_lane_6_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_7_swimmer_select) is not None and card2_lane_7_swimmer_select.is_visible()
        expect(card2_lane_7_swimmer_select).to_have_value("")
        expect(card2_lane_7_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_8_swimmer_select) is not None and card2_lane_8_swimmer_select.is_visible()
        expect(card2_lane_8_swimmer_select).to_have_value("")
        expect(card2_lane_8_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_9_swimmer_select) is not None and card2_lane_9_swimmer_select.is_visible()
        expect(card2_lane_9_swimmer_select).to_have_value("")
        expect(card2_lane_9_swimmer_select).to_have_js_property("tagName","SELECT")
        
        assert(btn_predict) is not None and btn_predict.is_visible()
        expect(btn_predict).to_have_text("Предсказать")
        expect(btn_predict).to_have_js_property("tagName","BUTTON")
        
        if page.viewport_size['width']<1200:  #Если размер экрана по горизонтали маленький, должна появиться кнопка для сворачивания кнопок меню
            assert header_btn_predict_swim is None or not header_btn_predict_swim.is_visible()
            assert header_btn_predict_discipline is None or not header_btn_predict_discipline.is_visible()
            assert header_btn_main is None or not header_btn_main.is_visible()
            assert header_btn_collapse is not None and header_btn_collapse.is_visible()
        else:
            assert header_btn_collapse is None or not header_btn_collapse.is_visible()
            assert header_btn_main is not None and header_btn_main.is_visible()
            assert header_btn_main.inner_text()=='Главная'
            href = header_btn_main.get_attribute("href")
            assert href=="/"
            assert header_btn_predict_swim is not None and header_btn_predict_swim.is_visible()
            assert header_btn_predict_swim.inner_text()=='Предсказать заплыв'
            href = header_btn_predict_swim.get_attribute("href")
            assert href=="" or href is None
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="discipline"
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        assert not card1_distance_invalid_feedback.is_visible()
        assert not card1_sex_invalid_feedback.is_visible()
        assert not card1_phase_invalid_feedback.is_visible()
        assert not card1_pool_length_invalid_feedback.is_visible()
        assert card1_datetime_invalid_feedback.is_visible()
        assert card1_datetime_invalid_feedback.inner_text()=="Выберите дату и время заплыва (от 2026 до 2050 года)!"
        assert not card1_host_country_invalid_feedback.is_visible()
        assert card2_swimmers_invalid_alert.is_visible()
        assert card2_swimmers_invalid_alert.inner_text()=="Один и тот же пловец не может встречаться на нескольких дорожках!"
        
        #Проверка элементов которых не должно существовать (результаты заплыва, тосты с ошибками сети)
        assert toasts_count==0
        assert visible_result_cards_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии по кнопке Предсказания при неправильном заполнении полей
    # (слишком поздняя дата заплыва, дупликаты пловцов), а именно:
    #Стиль плавания - Комплексный
    #Дистанция - 200м
    #Пол - Женский
    #Фаза - Полуфинал
    #Длина бассейна - 25м
    #Дата и время заплвыва - 01.01.2050 00:00:00
    #Страна проведения - Франция
    #Пловец на дорожке 3 - DUNN Alexandra
    #Пловец на дорожке 4 - DOUGLASS Kate
    #Пловец на дорожке 5 - DOUGLASS Kate
    #Пловец на дорожке 6 - PALLISTER Lani
    def test_all_elements_present_and_have_required_text_after_predict_click_invalid_input_too_late_date_duplicate_swimmer(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+SWIM_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.set_default_timeout(3000)
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Выбрать необходимые данные
        page.select_option("select#selectStyle",label="Комплексный")
        page.select_option("select#selectDistance",label="200м")
        page.select_option("select#selectSex",label="Женский")
        page.select_option("select#selectPhase",label="Полуфинал")
        page.select_option("select#selectPoolLength",label="25м")
        page.fill("input[type='datetime-local']", "2050-01-01T00:00")
        page.select_option("select#selectHostCountry",label="Франция")
        page.locator("#selectSwimmer3 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer3 + .ts-wrapper input").fill("DUNN")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer3 + .ts-wrapper .ts-dropdown .option", has_text="DUNN Alexandra").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(1000) #Подождать пока томселект закроется
        page.locator("#selectSwimmer4 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer4 + .ts-wrapper input").fill("DOUGLASS")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer4 + .ts-wrapper .ts-dropdown .option", has_text="DOUGLASS Kate").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(1000) #Подождать пока томселект закроется
        page.locator("#selectSwimmer5 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer5 + .ts-wrapper input").fill("DOUGLASS")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer5 + .ts-wrapper .ts-dropdown .option", has_text="DOUGLASS Kate").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(1000) #Подождать пока томселект закроется
        page.locator("#selectSwimmer6 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer6 + .ts-wrapper input").fill("PALLISTER")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer6 + .ts-wrapper .ts-dropdown .option", has_text="PALLISTER Lani").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(1000) #Подождать пока томселект закроется
        
        page.get_by_text("Предсказать",exact=True).first.click() #Нажать по кнопке предсказания
        page.wait_for_timeout(600)  # Ждем анимацию
        
        try:
            header_title=page.locator("nav").get_by_text('Система прогноза результатов по плаванию').first
        except:
            header_title=None
        try:
            header_btn_main=page.locator("nav").get_by_text("Главная").first
        except:
            header_btn_main=None
        try:
            header_btn_predict_swim=page.locator("nav").get_by_text("Предсказать заплыв").first
        except:
            header_btn_predict_swim=None
        try:
            header_btn_predict_discipline=page.locator("nav").get_by_text("Предсказать дисциплину").first
        except:
            header_btn_predict_discipline=None
        try:
            header_btn_collapse=page.locator("button.navbar-toggler").first
        except:
            header_btn_collapse=None
        
        try:
            card1_title=page.get_by_text('Введите сведения о заплыве').first
        except:
            card1_title=None
        try:
            card1_style_label=page.get_by_text('Стиль плавания:').first
        except:
            card1_style_label=None
        try:
            card1_distance_label=page.get_by_text('Дистанция:').first
        except:
            card1_distance_label=None
        try:
            card1_sex_label=page.get_by_text('Пол:').first
        except:
            card1_sex_label=None
        try:
            card1_phase_label=page.get_by_text('Фаза:').first
        except:
            card1_phase_label=None
        try:
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_datetime_label=page.get_by_text('Местная дата и время заплыва:').first
        except:
            card1_datetime_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_style_select=page.locator('select').filter(has_text="Выберите стиль").first
        except:
            card1_style_select=None
        try:
            card1_distance_select=page.locator('select').filter(has_text="Выберите дистанцию").first
        except:
            card1_distance_select=None
        try:
            card1_sex_select=page.locator('select').filter(has_text="Выберите пол").first
        except:
            card1_sex_select=None
        try:
            card1_phase_select=page.locator('select').filter(has_text="Выберите фазу заплыва").first
        except:
            card1_phase_select=None
        try:
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_datetime_input=page.locator("input[type='datetime-local']").first
        except:
            card1_datetime_input=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        
        try:
            card2_title=page.get_by_text('Введите сведения о пловцах заплыва').first
        except:
            card2_title=None
        try:
            card2_lane_header=page.get_by_text('Дорожка').first
        except:
            card2_lane_header=None
        try:
            card2_swimmer_header=page.get_by_text('Пловец').first
        except:
            card2_swimmer_header=None
        try:
            card2_lane_0_label=page.get_by_text('0',exact=True).first
        except:
            card2_lane_0_label=None
        try:
            card2_lane_1_label=page.get_by_text('1',exact=True).first
        except:
            card2_lane_1_label=None
        try:
            card2_lane_2_label=page.get_by_text('2',exact=True).first
        except:
            card2_lane_2_label=None
        try:
            card2_lane_3_label=page.get_by_text('3',exact=True).first
        except:
            card2_lane_3_label=None
        try:
            card2_lane_4_label=page.get_by_text('4',exact=True).first
        except:
            card2_lane_4_label=None
        try:
            card2_lane_5_label=page.get_by_text('5',exact=True).first
        except:
            card2_lane_5_label=None
        try:
            card2_lane_6_label=page.get_by_text('6',exact=True).first
        except:
            card2_lane_6_label=None
        try:
            card2_lane_7_label=page.get_by_text('7',exact=True).first
        except:
            card2_lane_7_label=None
        try:
            card2_lane_8_label=page.get_by_text('8',exact=True).first
        except:
            card2_lane_8_label=None
        try:
            card2_lane_9_label=page.get_by_text('9',exact=True).first
        except:
            card2_lane_9_label=None
        try:
            card2_lane_0_swimmer_select=page.locator('select').filter(has_text='Нет пловца').first
        except:
            card2_lane_0_swimmer_select=None
        try:
            card2_lane_1_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(1)
        except:
            card2_lane_1_swimmer_select=None
        try:
            card2_lane_2_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(2)
        except:
            card2_lane_2_swimmer_select=None
        try:
            card2_lane_3_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(3)
        except:
            card2_lane_3_swimmer_select=None
        try:
            card2_lane_4_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(4)
        except:
            card2_lane_4_swimmer_select=None
        try:
            card2_lane_5_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(5)
        except:
            card2_lane_5_swimmer_select=None
        try:
            card2_lane_6_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(6)
        except:
            card2_lane_6_swimmer_select=None
        try:
            card2_lane_7_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(7)
        except:
            card2_lane_7_swimmer_select=None
        try:
            card2_lane_8_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(8)
        except:
            card2_lane_8_swimmer_select=None
        try:
            card2_lane_9_swimmer_select=page.locator('select').filter(has_text='Нет пловца').nth(9)
        except:
            card2_lane_9_swimmer_select=None
            
        try:
            btn_predict=page.get_by_text("Предсказать",exact=True)
        except:
            btn_predict=None
        
        try:
            card1_style_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите стиль плавания!").first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите дистанцию!").first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите пол!").first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_phase_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите фазу!").first
        except:
            card1_phase_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите длину бассейна!").first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_datetime_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите дату и время заплыва (от 2026 до 2050 года)!").first
        except:
            card1_datetime_invalid_feedback=None
        try:
            card1_host_country_invalid_feedback=page.locator('div.invalid-feedback').filter(has_text="Выберите страну заплыва!").first
        except:
            card1_host_country_invalid_feedback=None
        try:
            card2_swimmers_invalid_alert=page.locator('div.alert')
        except:
            card2_swimmers_invalid_alert=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_cards_count=page.locator("[id^='swimmer'][id$='Results']").filter(visible=True).count() #Число выходных карточек
        except:
            visible_result_cards_count=0
        
        try:
            toasts_count=page.locator("div.toast").count()
        except:
            toasts_count=0
        
        
        
        
        
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о заплыве"
        expect(card1_title).to_have_js_property("tagName","DIV")
        assert(card1_style_label) is not None and card1_style_label.is_visible()
        assert card1_style_label.inner_text()=="Стиль плавания:"
        expect(card1_style_label).to_have_js_property("tagName","LABEL")
        assert(card1_distance_label) is not None and card1_distance_label.is_visible()
        assert card1_distance_label.inner_text()=="Дистанция:"
        expect(card1_distance_label).to_have_js_property("tagName","LABEL")
        assert(card1_sex_label) is not None and card1_sex_label.is_visible()
        assert card1_sex_label.inner_text()=="Пол:"
        expect(card1_sex_label).to_have_js_property("tagName","LABEL")
        assert(card1_phase_label) is not None and card1_phase_label.is_visible()
        assert card1_phase_label.inner_text()=="Фаза:"
        expect(card1_phase_label).to_have_js_property("tagName","LABEL")
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_datetime_label) is not None and card1_datetime_label.is_visible()
        assert card1_datetime_label.inner_text()=="Местная дата и время заплыва:"
        expect(card1_datetime_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Комплексный")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("200м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Женский")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_phase_select) is not None and card1_phase_select.is_visible()
        expect(card1_phase_select.locator("option:checked")).to_have_text("Полуфинал")
        expect(card1_phase_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_datetime_input) is not None and card1_datetime_input.is_visible()
        expect(card1_datetime_input).to_have_value("2050-01-01T00:00")
        expect(card1_datetime_input).to_have_attribute("type","datetime-local")
        expect(card1_datetime_input).to_have_js_property("tagName","INPUT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Франция")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        
        assert(card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите сведения о пловцах заплыва"
        expect(card2_title).to_have_js_property("tagName","DIV")
        assert(card2_lane_header) is not None and card2_lane_header.is_visible()
        assert card2_lane_header.inner_text()=="Дорожка"
        expect(card2_lane_header).to_have_js_property("tagName","LABEL")
        assert(card2_swimmer_header) is not None and card2_swimmer_header.is_visible()
        assert card2_swimmer_header.inner_text()=="Пловец"
        expect(card2_swimmer_header).to_have_js_property("tagName","LABEL")
        assert(card2_lane_0_label) is not None and card2_lane_0_label.is_visible()
        assert card2_lane_0_label.inner_text()=="0"
        expect(card2_lane_0_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_1_label) is not None and card2_lane_1_label.is_visible()
        assert card2_lane_1_label.inner_text()=="1"
        expect(card2_lane_1_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_2_label) is not None and card2_lane_2_label.is_visible()
        assert card2_lane_2_label.inner_text()=="2"
        expect(card2_lane_2_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_3_label) is not None and card2_lane_3_label.is_visible()
        assert card2_lane_3_label.inner_text()=="3"
        expect(card2_lane_3_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_4_label) is not None and card2_lane_4_label.is_visible()
        assert card2_lane_4_label.inner_text()=="4"
        expect(card2_lane_4_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_5_label) is not None and card2_lane_5_label.is_visible()
        assert card2_lane_5_label.inner_text()=="5"
        expect(card2_lane_5_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_6_label) is not None and card2_lane_6_label.is_visible()
        assert card2_lane_6_label.inner_text()=="6"
        expect(card2_lane_6_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_7_label) is not None and card2_lane_7_label.is_visible()
        assert card2_lane_7_label.inner_text()=="7"
        expect(card2_lane_7_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_8_label) is not None and card2_lane_8_label.is_visible()
        assert card2_lane_8_label.inner_text()=="8"
        expect(card2_lane_8_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_9_label) is not None and card2_lane_9_label.is_visible()
        assert card2_lane_9_label.inner_text()=="9"
        expect(card2_lane_9_label).to_have_js_property("tagName","LABEL")
        assert(card2_lane_0_swimmer_select) is not None and card2_lane_0_swimmer_select.is_visible()
        expect(card2_lane_0_swimmer_select.locator("option:checked")).to_have_text("Нет пловца")
        expect(card2_lane_0_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_1_swimmer_select) is not None and card2_lane_1_swimmer_select.is_visible()
        expect(card2_lane_1_swimmer_select.locator("option:checked")).to_have_text("Нет пловца")
        expect(card2_lane_1_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_2_swimmer_select) is not None and card2_lane_2_swimmer_select.is_visible()
        expect(card2_lane_2_swimmer_select).to_have_value("")
        expect(card2_lane_2_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_3_swimmer_select) is not None and card2_lane_3_swimmer_select.is_visible()
        expect(card2_lane_3_swimmer_select.locator("option:checked")).to_have_text("DUNN Alexandra")
        expect(card2_lane_3_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_4_swimmer_select) is not None and card2_lane_4_swimmer_select.is_visible()
        expect(card2_lane_4_swimmer_select.locator("option:checked")).to_have_text("DOUGLASS Kate")
        expect(card2_lane_4_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_5_swimmer_select) is not None and card2_lane_5_swimmer_select.is_visible()
        expect(card2_lane_5_swimmer_select.locator("option:checked")).to_have_text("DOUGLASS Kate")
        expect(card2_lane_5_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_6_swimmer_select) is not None and card2_lane_6_swimmer_select.is_visible()
        expect(card2_lane_6_swimmer_select.locator("option:checked")).to_have_text("PALLISTER Lani")
        expect(card2_lane_6_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_7_swimmer_select) is not None and card2_lane_7_swimmer_select.is_visible()
        expect(card2_lane_7_swimmer_select).to_have_value("")
        expect(card2_lane_7_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_8_swimmer_select) is not None and card2_lane_8_swimmer_select.is_visible()
        expect(card2_lane_8_swimmer_select).to_have_value("")
        expect(card2_lane_8_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_9_swimmer_select) is not None and card2_lane_9_swimmer_select.is_visible()
        expect(card2_lane_9_swimmer_select).to_have_value("")
        expect(card2_lane_9_swimmer_select).to_have_js_property("tagName","SELECT")
        
        assert(btn_predict) is not None and btn_predict.is_visible()
        expect(btn_predict).to_have_text("Предсказать")
        expect(btn_predict).to_have_js_property("tagName","BUTTON")
        
        if page.viewport_size['width']<1200:  #Если размер экрана по горизонтали маленький, должна появиться кнопка для сворачивания кнопок меню
            assert header_btn_predict_swim is None or not header_btn_predict_swim.is_visible()
            assert header_btn_predict_discipline is None or not header_btn_predict_discipline.is_visible()
            assert header_btn_main is None or not header_btn_main.is_visible()
            assert header_btn_collapse is not None and header_btn_collapse.is_visible()
        else:
            assert header_btn_collapse is None or not header_btn_collapse.is_visible()
            assert header_btn_main is not None and header_btn_main.is_visible()
            assert header_btn_main.inner_text()=='Главная'
            href = header_btn_main.get_attribute("href")
            assert href=="/"
            assert header_btn_predict_swim is not None and header_btn_predict_swim.is_visible()
            assert header_btn_predict_swim.inner_text()=='Предсказать заплыв'
            href = header_btn_predict_swim.get_attribute("href")
            assert href=="" or href is None
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="discipline"
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        assert not card1_distance_invalid_feedback.is_visible()
        assert not card1_sex_invalid_feedback.is_visible()
        assert not card1_phase_invalid_feedback.is_visible()
        assert not card1_pool_length_invalid_feedback.is_visible()
        assert card1_datetime_invalid_feedback.is_visible()
        assert card1_datetime_invalid_feedback.inner_text()=="Выберите дату и время заплыва (от 2026 до 2050 года)!"
        assert not card1_host_country_invalid_feedback.is_visible()
        assert card2_swimmers_invalid_alert.is_visible()
        assert card2_swimmers_invalid_alert.inner_text()=="Один и тот же пловец не может встречаться на нескольких дорожках!"
        
        #Проверка элементов которых не должно существовать (результаты заплыва, тосты с ошибками сети)
        assert toasts_count==0
        assert visible_result_cards_count==0
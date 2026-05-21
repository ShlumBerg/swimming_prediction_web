import pytest
from playwright.sync_api import sync_playwright,Browser,Page,expect
BASE_URL_DEFAULT="http://217.26.30.216"
SWIM_PAGE_PATH="/swim"
DISCIPLINE_PAGE_PATH="/discipline"

#Настроить размер viewport для playwright (через встроеную в него функцию)
@pytest.fixture(scope="function")
def browser_context_args(browser_context_args,viewport):
    return {
        **browser_context_args,
        "viewport": viewport}


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
def browser_context_args(browser_context_args,viewport):
    return {
        **browser_context_args,
        "viewport": viewport}
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
            toasts_count=page.locator("div.toast").filter(visible=True).count()
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
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при отсутствии интернета и действий на странице
    def test_all_elements_present_and_have_required_text_no_actions_and_no_internet(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+SWIM_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.context.set_offline(True) #Отключить интернет как только страница загрузилась
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
            toasts_count=page.locator("div.toast").filter(visible=True).count()
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
        #Проверка элементов которых не должно существовать (результаты заплыва)
        assert visible_result_cards_count==0
        
        #Проверка что есть ошибки сети
        assert toasts_count>0
    
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
            toasts_count=page.locator("div.toast").filter(visible=True).count()
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
            toasts_count=page.locator("div.toast").filter(visible=True).count()
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
            toasts_count=page.locator("div.toast").filter(visible=True).count()
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
            toasts_count=page.locator("div.toast").filter(visible=True).count()
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
            toasts_count=page.locator("div.toast").filter(visible=True).count()
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
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии по кнопке Предсказания при правильном заполнении полей
    #а именно:
    #Стиль плавания - вольный
    #Дистанция - 50м
    #Пол - Мужской
    #Фаза - Финал
    #Длина бассейна - 50м
    #Дата и время заплвыва - 01.01.2026 00:00:00
    #Страна проведения - Греция
    #Пловец на дорожке 9 - LIENDO Josh
    def test_all_elements_present_and_have_required_text_after_predict_click_valid_input_earliest_possible_date_single_swimmer(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+SWIM_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.set_default_timeout(3000)
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Выбрать необходимые данные
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPhase",label="Финал")
        page.select_option("select#selectPoolLength",label="50м")
        page.fill("input[type='datetime-local']", "2026-01-01T00:00")
        page.select_option("select#selectHostCountry",label="Греция")
        page.locator("#selectSwimmer9 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer9 + .ts-wrapper input").fill("LIENDO")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer9 + .ts-wrapper .ts-dropdown .option", has_text="LIENDO Josh").click()
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
            toasts_count=page.locator("div.toast").filter(visible=True).count()
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
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_phase_select) is not None and card1_phase_select.is_visible()
        expect(card1_phase_select.locator("option:checked")).to_have_text("Финал")
        expect(card1_phase_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("50м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_datetime_input) is not None and card1_datetime_input.is_visible()
        expect(card1_datetime_input).to_have_value("2026-01-01T00:00")
        expect(card1_datetime_input).to_have_attribute("type","datetime-local")
        expect(card1_datetime_input).to_have_js_property("tagName","INPUT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Греция")
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
        expect(card2_lane_9_swimmer_select.locator("option:checked")).to_have_text("LIENDO Josh")
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
        assert not card1_datetime_invalid_feedback.is_visible()
        assert not card1_host_country_invalid_feedback.is_visible()
        assert not card2_swimmers_invalid_alert.is_visible()
        
        #Проверка элементов которых не должно существовать (тосты с ошибками сети)
        assert toasts_count==0
        
        #Проверка что карточек с результатами ровно 1 штука
        assert visible_result_cards_count==1
        
        #Проверяем каждую карточку
        class swimmer_res:
            time:float
            place:int
        results_list=[]
        lanes_list=[9]
        swimmers_list=["LIENDO Josh"]
        for ind, lane in enumerate(lanes_list):
            result_card_title=page.locator(f'div#swimmer{lane}Results div.card-header')
            result_swimmer_header_label=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(1) > div:nth-child(1)')
            result_time_header_label=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(2) > div:nth-child(1)')
            result_place_header_label=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(3) > div:nth-child(1)')
            result_swimmer_val=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(1) > div:nth-child(2)')
            result_time_val=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(2) > div:nth-child(2)')
            result_place_val=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(3) > div:nth-child(2)')
            show_graphs_btn=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(4) > button:nth-child(1)')
            #Проверить что все подписи к результатам видны и соответствуют ожидаемым
            assert result_swimmer_header_label.is_visible() and result_swimmer_header_label.inner_text()=="Пловец:"
            assert result_time_header_label.is_visible() and result_time_header_label.inner_text()=="Время:"
            assert result_place_header_label.is_visible() and result_place_header_label.inner_text()=="Место:"
            #Проверить что все результаты видны и соответствуют ожидаемым
            time_str=result_time_val.inner_text()
            if ':' in time_str:
                parts = time_str.split(':')
                if len(parts)==2:
                    res_time_secs = float(parts[0]) * 60 + float(parts[1])
                elif len(parts)==3:
                    res_time_secs = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
            else:
                res_time_secs = float(time_str)
            
            res_place=int(result_place_val.inner_text())
            assert result_swimmer_val.is_visible() and result_swimmer_val.inner_text()==swimmers_list[ind]
            assert result_time_val.is_visible() and res_time_secs>=10
            assert result_place_val.is_visible() and res_place>0 and res_place<=len(lanes_list)
            
            #Проверить что название карточки видно и соответствует ожидаемому
            assert result_card_title.is_visible() and result_card_title.inner_text()==f"Результаты пловца на дорожке {lane}"
            
            #Проверить что кнопка графиков видна и соответствует ожидаемому
            assert show_graphs_btn.is_visible() and show_graphs_btn.inner_text()=="Графики..."
            
            #Проверить что модалка с графиками видна при нажатии на кнопку и соответствует ожидаемому
            show_graphs_btn.click()
            page.wait_for_timeout(300) #Ждем прогрузки графиков
            graphs_modal=page.locator("div#graphsModal")
            assert graphs_modal.is_visible() #Проверка что видно модалку
            graphs_modal_title=page.locator("div.modal-header")
            assert graphs_modal_title.is_visible() and graphs_modal_title.inner_text()==f"Графики для пловца {swimmers_list[ind]}" #Проверка на видимость и содержание заголовка модалки
            canvas_height_dependency=page.locator("canvas#canvasHeightDependency")
            canvas_height_dependency_label=page.locator("label#canvasHeightDependencyLabel")
            #Проверка на видимость графика зависимости от роста (или на видимость соответствующей надписи о том что графика нет)
            assert canvas_height_dependency.is_visible() and not canvas_height_dependency_label.is_visible() or \
                not canvas_height_dependency.is_visible() and canvas_height_dependency_label.is_visible() and canvas_height_dependency_label.inner_text()=="График зависимости времени от роста пловца отсутствует, так как рост пловца неизвестен!"
            canvas_age_dependency=page.locator("canvas#canvasAgeDependency")
            canvas_age_dependency_label=page.locator("label#canvasAgeDependencyLabel")
            #Проверка на видимость графика зависимости от возраста (или на видимость соответствующей надписи о том что графика нет)
            assert canvas_age_dependency.is_visible() and not canvas_age_dependency_label.is_visible() or \
                not canvas_age_dependency.is_visible() and canvas_age_dependency_label.is_visible() and canvas_age_dependency_label.inner_text()=="График зависимости времени от возраста пловца отсутствует, так как возраст пловца неизвестен!"
            canvas_lane_dependency=page.locator("canvas#canvasLaneDependency")
            #Проверка на видимость графика зависимости от дорожки
            assert canvas_lane_dependency.is_visible()
            graphs_modal_close_btn=page.locator("div.modal-header button.btn-close")
            assert graphs_modal_close_btn.is_visible() #Проверка что кнопка закрытия видна
            
            #Проверить что модалка с графиками не видна при нажатии на кнопку закрытия модалки
            graphs_modal_close_btn.click()
            page.wait_for_timeout(300) #Ждем закрытия модалки
            assert not graphs_modal.is_visible() #Проверка что не видно модалку
            assert not graphs_modal_title.is_visible() #Проверка что не видно заголовок модалки
            assert not canvas_height_dependency.is_visible() and not canvas_height_dependency_label.is_visible() #Проверка что не видно график зависимости от роста и не видно надпись о его отсутствии
            assert not canvas_age_dependency.is_visible() and not canvas_age_dependency_label.is_visible() #Проверка что не видно график зависимости от возраста и не видно надпись о его отсутствии
            assert not canvas_lane_dependency.is_visible()  #Проверка что не видно график зависимости от дорожки
            assert not graphs_modal_close_btn.is_visible() #Проверка что кнопка закрытия модалки не видна
            
            results_list.append(swimmer_res())
            results_list[-1].time=res_time_secs
            results_list[-1].place=res_place
        
        #Проверяем что места уникальны и что результирующее время соответствует результирующему месту
        results_list=sorted(results_list, key=lambda x: x.place)
        for i in range(len(results_list)-1):
            assert results_list[i+1].place> results_list[i].place
            assert results_list[i+1].time>= results_list[i].time
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии по кнопке Предсказания при правильном заполнении полей
    #а именно:
    #Стиль плавания - на спине
    #Дистанция - 1500м
    #Пол - Женский
    #Фаза - Отборочные
    #Длина бассейна - 25м
    #Дата и время заплвыва - 31.12.2049 23:59:59
    #Страна проведения - Россия
    #Пловец на дорожке 0 - SUZUKI Satomi
    #Пловец на дорожке 1 - CASEY Hannah
    #Пловец на дорожке 2 - WASICK Katarzyna
    #Пловец на дорожке 3 - SMOLIGA Olivia
    #Пловец на дорожке 4 - COLLINS Ava
    #Пловец на дорожке 5 - BARBER Molly
    #Пловец на дорожке 6 - NORMAN Gemma
    #Пловец на дорожке 7 - WOOD Abbie
    #Пловец на дорожке 8 - IRANGI Nina
    #Пловец на дорожке 9 - CHONG Xin Lin
    def test_all_elements_present_and_have_required_text_after_predict_click_valid_input_earliest_possible_date_10_swimmers(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+SWIM_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.set_default_timeout(3000)
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Выбрать необходимые данные
        page.select_option("select#selectStyle",label="На спине")
        page.select_option("select#selectDistance",label="1500м")
        page.select_option("select#selectSex",label="Женский")
        page.select_option("select#selectPhase",label="Отборочные")
        page.select_option("select#selectPoolLength",label="25м")
        page.fill("input[type='datetime-local']", "2049-12-31T23:59:59")
        page.select_option("select#selectHostCountry",label="Россия")
        
        page.locator("#selectSwimmer0 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer0 + .ts-wrapper input").fill("SUZUKI")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer0 + .ts-wrapper .ts-dropdown .option", has_text="SUZUKI Satomi").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer1 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer1 + .ts-wrapper input").fill("CASEY")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer1 + .ts-wrapper .ts-dropdown .option", has_text="CASEY Hannah").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer2 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer2 + .ts-wrapper input").fill("WASICK")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer2 + .ts-wrapper .ts-dropdown .option", has_text="WASICK Katarzyna").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer3 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer3 + .ts-wrapper input").fill("SMOLIGA")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer3 + .ts-wrapper .ts-dropdown .option", has_text="SMOLIGA Olivia").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer4 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer4 + .ts-wrapper input").fill("collins")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer4 + .ts-wrapper .ts-dropdown .option", has_text="COLLINS Ava").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer5 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer5 + .ts-wrapper input").fill("BARBER")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer5 + .ts-wrapper .ts-dropdown .option", has_text="BARBER Molly").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer6 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer6 + .ts-wrapper input").fill("NORMAN")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer6 + .ts-wrapper .ts-dropdown .option", has_text="NORMAN Gemma").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer7 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer7 + .ts-wrapper input").fill("WOOD")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer7 + .ts-wrapper .ts-dropdown .option", has_text="WOOD Abbie").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer8 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer8 + .ts-wrapper input").fill("IRANGI")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer8 + .ts-wrapper .ts-dropdown .option", has_text="IRANGI Nina").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer9 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer9 + .ts-wrapper input").fill("CHONG")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer9 + .ts-wrapper .ts-dropdown .option", has_text="CHONG Xin Lin").click()
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
            toasts_count=page.locator("div.toast").filter(visible=True).count()
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
        expect(card1_style_select.locator("option:checked")).to_have_text("На спине")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("1500м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Женский")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_phase_select) is not None and card1_phase_select.is_visible()
        expect(card1_phase_select.locator("option:checked")).to_have_text("Отборочные")
        expect(card1_phase_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_datetime_input) is not None and card1_datetime_input.is_visible()
        expect(card1_datetime_input).to_have_value("2049-12-31T23:59:59")
        expect(card1_datetime_input).to_have_attribute("type","datetime-local")
        expect(card1_datetime_input).to_have_js_property("tagName","INPUT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Россия")
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
        expect(card2_lane_0_swimmer_select.locator("option:checked")).to_have_text("SUZUKI Satomi")
        expect(card2_lane_0_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_1_swimmer_select) is not None and card2_lane_1_swimmer_select.is_visible()
        expect(card2_lane_1_swimmer_select.locator("option:checked")).to_have_text("CASEY Hannah")
        expect(card2_lane_1_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_2_swimmer_select) is not None and card2_lane_2_swimmer_select.is_visible()
        expect(card2_lane_2_swimmer_select.locator("option:checked")).to_have_text("WASICK Katarzyna")
        expect(card2_lane_2_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_3_swimmer_select) is not None and card2_lane_3_swimmer_select.is_visible()
        expect(card2_lane_3_swimmer_select.locator("option:checked")).to_have_text("SMOLIGA Olivia")
        expect(card2_lane_3_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_4_swimmer_select) is not None and card2_lane_4_swimmer_select.is_visible()
        expect(card2_lane_4_swimmer_select.locator("option:checked")).to_have_text("COLLINS Ava")
        expect(card2_lane_4_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_5_swimmer_select) is not None and card2_lane_5_swimmer_select.is_visible()
        expect(card2_lane_5_swimmer_select.locator("option:checked")).to_have_text("BARBER Molly")
        expect(card2_lane_5_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_6_swimmer_select) is not None and card2_lane_6_swimmer_select.is_visible()
        expect(card2_lane_6_swimmer_select.locator("option:checked")).to_have_text("NORMAN Gemma")
        expect(card2_lane_6_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_7_swimmer_select) is not None and card2_lane_7_swimmer_select.is_visible()
        expect(card2_lane_7_swimmer_select.locator("option:checked")).to_have_text("WOOD Abbie")
        expect(card2_lane_7_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_8_swimmer_select) is not None and card2_lane_8_swimmer_select.is_visible()
        expect(card2_lane_8_swimmer_select.locator("option:checked")).to_have_text("IRANGI Nina")
        expect(card2_lane_8_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_9_swimmer_select) is not None and card2_lane_9_swimmer_select.is_visible()
        expect(card2_lane_9_swimmer_select.locator("option:checked")).to_have_text("CHONG Xin Lin")
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
        assert not card1_datetime_invalid_feedback.is_visible()
        assert not card1_host_country_invalid_feedback.is_visible()
        assert not card2_swimmers_invalid_alert.is_visible()
        
        #Проверка элементов которых не должно существовать (тосты с ошибками сети)
        assert toasts_count==0
        
        #Проверка что карточек с результатами ровно 10 штук
        assert visible_result_cards_count==10
        
        #Проверяем каждую карточку
        class swimmer_res:
            time:float
            place:int
        results_list=[]
        lanes_list=[0,1,2,3,4,5,6,7,8,9]
        swimmers_list=["SUZUKI Satomi","CASEY Hannah","WASICK Katarzyna","SMOLIGA Olivia","COLLINS Ava",
                        "BARBER Molly","NORMAN Gemma","WOOD Abbie","IRANGI Nina","CHONG Xin Lin"]
        for ind, lane in enumerate(lanes_list):
            result_card_title=page.locator(f'div#swimmer{lane}Results div.card-header')
            result_swimmer_header_label=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(1) > div:nth-child(1)')
            result_time_header_label=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(2) > div:nth-child(1)')
            result_place_header_label=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(3) > div:nth-child(1)')
            result_swimmer_val=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(1) > div:nth-child(2)')
            result_time_val=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(2) > div:nth-child(2)')
            result_place_val=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(3) > div:nth-child(2)')
            show_graphs_btn=page.locator(f'div#swimmer{lane}Results div.card-body div#swimmerDataTable > div:nth-child(4) > button:nth-child(1)')
            #Проверить что все подписи к результатам видны и соответствуют ожидаемым
            assert result_swimmer_header_label.is_visible() and result_swimmer_header_label.inner_text()=="Пловец:"
            assert result_time_header_label.is_visible() and result_time_header_label.inner_text()=="Время:"
            assert result_place_header_label.is_visible() and result_place_header_label.inner_text()=="Место:"
            #Проверить что все результаты видны и соответствуют ожидаемым
            time_str = result_time_val.inner_text()
            if ':' in time_str:
                parts = time_str.split(':')
                if len(parts)==2:
                    res_time_secs = float(parts[0]) * 60 + float(parts[1])
                elif len(parts)==3:
                    res_time_secs = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
            else:
                res_time_secs = float(time_str)
            
            res_place=int(result_place_val.inner_text())
            assert result_swimmer_val.is_visible() and result_swimmer_val.inner_text()==swimmers_list[ind]
            assert result_time_val.is_visible() and res_time_secs>=10
            assert result_place_val.is_visible() and res_place>0 and res_place<=len(lanes_list)
            
            #Проверить что название карточки видно и соответствует ожидаемому
            assert result_card_title.is_visible() and result_card_title.inner_text()==f"Результаты пловца на дорожке {lane}"
            
            #Проверить что кнопка графиков видна и соответствует ожидаемому
            assert show_graphs_btn.is_visible() and show_graphs_btn.inner_text()=="Графики..."
            
            #Проверить что модалка с графиками видна при нажатии на кнопку и соответствует ожидаемому
            show_graphs_btn.click()
            page.wait_for_timeout(300) #Ждем прогрузки графиков
            graphs_modal=page.locator("div#graphsModal")
            assert graphs_modal.is_visible() #Проверка что видно модалку
            graphs_modal_title=page.locator("div.modal-header")
            assert graphs_modal_title.is_visible() and graphs_modal_title.inner_text()==f"Графики для пловца {swimmers_list[ind]}" #Проверка на видимость и содержание заголовка модалки
            canvas_height_dependency=page.locator("canvas#canvasHeightDependency")
            canvas_height_dependency_label=page.locator("label#canvasHeightDependencyLabel")
            #Проверка на видимость графика зависимости от роста (или на видимость соответствующей надписи о том что графика нет)
            assert canvas_height_dependency.is_visible() and not canvas_height_dependency_label.is_visible() or \
                not canvas_height_dependency.is_visible() and canvas_height_dependency_label.is_visible() and canvas_height_dependency_label.inner_text()=="График зависимости времени от роста пловца отсутствует, так как рост пловца неизвестен!"
            canvas_age_dependency=page.locator("canvas#canvasAgeDependency")
            canvas_age_dependency_label=page.locator("label#canvasAgeDependencyLabel")
            #Проверка на видимость графика зависимости от возраста (или на видимость соответствующей надписи о том что графика нет)
            assert canvas_age_dependency.is_visible() and not canvas_age_dependency_label.is_visible() or \
                not canvas_age_dependency.is_visible() and canvas_age_dependency_label.is_visible() and canvas_age_dependency_label.inner_text()=="График зависимости времени от возраста пловца отсутствует, так как возраст пловца неизвестен!"
            canvas_lane_dependency=page.locator("canvas#canvasLaneDependency")
            #Проверка на видимость графика зависимости от дорожки
            assert canvas_lane_dependency.is_visible()
            graphs_modal_close_btn=page.locator("div.modal-header button.btn-close")
            assert graphs_modal_close_btn.is_visible() #Проверка что кнопка закрытия видна
            
            #Проверить что модалка с графиками не видна при нажатии на кнопку закрытия модалки
            graphs_modal_close_btn.click()
            page.wait_for_timeout(300) #Ждем закрытия модалки
            assert not graphs_modal.is_visible() #Проверка что не видно модалку
            assert not graphs_modal_title.is_visible() #Проверка что не видно заголовок модалки
            assert not canvas_height_dependency.is_visible() and not canvas_height_dependency_label.is_visible() #Проверка что не видно график зависимости от роста и не видно надпись о его отсутствии
            assert not canvas_age_dependency.is_visible() and not canvas_age_dependency_label.is_visible() #Проверка что не видно график зависимости от возраста и не видно надпись о его отсутствии
            assert not canvas_lane_dependency.is_visible()  #Проверка что не видно график зависимости от дорожки
            assert not graphs_modal_close_btn.is_visible() #Проверка что кнопка закрытия модалки не видна
            
            results_list.append(swimmer_res())
            results_list[-1].time=res_time_secs
            results_list[-1].place=res_place
        
        #Проверяем что места уникальны и что результирующее время соответствует результирующему месту
        results_list=sorted(results_list, key=lambda x: x.place)
        for i in range(len(results_list)-1):
            assert results_list[i+1].place> results_list[i].place
            assert results_list[i+1].time>= results_list[i].time
            
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии по кнопке Предсказания при правильном заполнении полей
    #а именно:
    #Стиль плавания - на спине
    #Дистанция - 1500м
    #Пол - Женский
    #Фаза - Отборочные
    #Длина бассейна - 25м
    #Дата и время заплвыва - 31.12.2049 23:59:59
    #Страна проведения - Россия
    #Пловец на дорожке 0 - SUZUKI Satomi
    #Пловец на дорожке 1 - CASEY Hannah
    #Пловец на дорожке 2 - WASICK Katarzyna
    #Пловец на дорожке 3 - SMOLIGA Olivia
    #Пловец на дорожке 4 - COLLINS Ava
    #Пловец на дорожке 5 - BARBER Molly
    #Пловец на дорожке 6 - NORMAN Gemma
    #Пловец на дорожке 7 - WOOD Abbie
    #Пловец на дорожке 8 - IRANGI Nina
    #Пловец на дорожке 9 - CHONG Xin Lin
    #При этом во время нажатия кнопки предсказания Интернет отсутствует.
    def test_all_elements_present_and_have_required_text_after_predict_click_valid_input_earliest_possible_date_10_swimmers_and_no_internet(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+SWIM_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.set_default_timeout(3000)
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Выбрать необходимые данные
        page.select_option("select#selectStyle",label="На спине")
        page.select_option("select#selectDistance",label="1500м")
        page.select_option("select#selectSex",label="Женский")
        page.select_option("select#selectPhase",label="Отборочные")
        page.select_option("select#selectPoolLength",label="25м")
        page.fill("input[type='datetime-local']", "2049-12-31T23:59:59")
        page.select_option("select#selectHostCountry",label="Россия")
        
        page.locator("#selectSwimmer0 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer0 + .ts-wrapper input").fill("SUZUKI")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer0 + .ts-wrapper .ts-dropdown .option", has_text="SUZUKI Satomi").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer1 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer1 + .ts-wrapper input").fill("CASEY")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer1 + .ts-wrapper .ts-dropdown .option", has_text="CASEY Hannah").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer2 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer2 + .ts-wrapper input").fill("WASICK")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer2 + .ts-wrapper .ts-dropdown .option", has_text="WASICK Katarzyna").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer3 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer3 + .ts-wrapper input").fill("SMOLIGA")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer3 + .ts-wrapper .ts-dropdown .option", has_text="SMOLIGA Olivia").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer4 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer4 + .ts-wrapper input").fill("collins")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer4 + .ts-wrapper .ts-dropdown .option", has_text="COLLINS Ava").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer5 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer5 + .ts-wrapper input").fill("BARBER")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer5 + .ts-wrapper .ts-dropdown .option", has_text="BARBER Molly").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer6 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer6 + .ts-wrapper input").fill("NORMAN")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer6 + .ts-wrapper .ts-dropdown .option", has_text="NORMAN Gemma").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer7 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer7 + .ts-wrapper input").fill("WOOD")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer7 + .ts-wrapper .ts-dropdown .option", has_text="WOOD Abbie").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer8 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer8 + .ts-wrapper input").fill("IRANGI")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer8 + .ts-wrapper .ts-dropdown .option", has_text="IRANGI Nina").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmer9 + .ts-wrapper input").focus()
        page.locator("#selectSwimmer9 + .ts-wrapper input").fill("CHONG")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmer9 + .ts-wrapper .ts-dropdown .option", has_text="CHONG Xin Lin").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.context.set_offline(True) #Отключить интернет
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
            toasts_count=page.locator("div.toast").filter(visible=True).count()
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
        expect(card1_style_select.locator("option:checked")).to_have_text("На спине")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("1500м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Женский")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_phase_select) is not None and card1_phase_select.is_visible()
        expect(card1_phase_select.locator("option:checked")).to_have_text("Отборочные")
        expect(card1_phase_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_datetime_input) is not None and card1_datetime_input.is_visible()
        expect(card1_datetime_input).to_have_value("2049-12-31T23:59:59")
        expect(card1_datetime_input).to_have_attribute("type","datetime-local")
        expect(card1_datetime_input).to_have_js_property("tagName","INPUT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Россия")
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
        expect(card2_lane_0_swimmer_select.locator("option:checked")).to_have_text("SUZUKI Satomi")
        expect(card2_lane_0_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_1_swimmer_select) is not None and card2_lane_1_swimmer_select.is_visible()
        expect(card2_lane_1_swimmer_select.locator("option:checked")).to_have_text("CASEY Hannah")
        expect(card2_lane_1_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_2_swimmer_select) is not None and card2_lane_2_swimmer_select.is_visible()
        expect(card2_lane_2_swimmer_select.locator("option:checked")).to_have_text("WASICK Katarzyna")
        expect(card2_lane_2_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_3_swimmer_select) is not None and card2_lane_3_swimmer_select.is_visible()
        expect(card2_lane_3_swimmer_select.locator("option:checked")).to_have_text("SMOLIGA Olivia")
        expect(card2_lane_3_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_4_swimmer_select) is not None and card2_lane_4_swimmer_select.is_visible()
        expect(card2_lane_4_swimmer_select.locator("option:checked")).to_have_text("COLLINS Ava")
        expect(card2_lane_4_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_5_swimmer_select) is not None and card2_lane_5_swimmer_select.is_visible()
        expect(card2_lane_5_swimmer_select.locator("option:checked")).to_have_text("BARBER Molly")
        expect(card2_lane_5_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_6_swimmer_select) is not None and card2_lane_6_swimmer_select.is_visible()
        expect(card2_lane_6_swimmer_select.locator("option:checked")).to_have_text("NORMAN Gemma")
        expect(card2_lane_6_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_7_swimmer_select) is not None and card2_lane_7_swimmer_select.is_visible()
        expect(card2_lane_7_swimmer_select.locator("option:checked")).to_have_text("WOOD Abbie")
        expect(card2_lane_7_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_8_swimmer_select) is not None and card2_lane_8_swimmer_select.is_visible()
        expect(card2_lane_8_swimmer_select.locator("option:checked")).to_have_text("IRANGI Nina")
        expect(card2_lane_8_swimmer_select).to_have_js_property("tagName","SELECT")
        assert(card2_lane_9_swimmer_select) is not None and card2_lane_9_swimmer_select.is_visible()
        expect(card2_lane_9_swimmer_select.locator("option:checked")).to_have_text("CHONG Xin Lin")
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
        assert not card1_datetime_invalid_feedback.is_visible()
        assert not card1_host_country_invalid_feedback.is_visible()
        assert not card2_swimmers_invalid_alert.is_visible()
        
        #Проверка что существуют тосты с ошибками сети
        assert toasts_count>0
        
        #Проверка что карточек с результатами нет
        assert visible_result_cards_count==0
        
#Настроить размер viewport для playwright (через встроеную в него функцию)
@pytest.fixture(scope="function")
def browser_context_args(browser_context_args,viewport):
    return {
        **browser_context_args,
        "viewport": viewport}
@pytest.mark.parametrize("viewport",[
    pytest.param({"width":393,"height":852},id="xs"), #extra small (iphone 14 iOS 18.6 vertical)
    pytest.param({"width":712,"height":1138},id="sm"), #small (galaxy tab s9 android 14 vetrical)
    pytest.param({"width":820,"height":1180},id="md"), #medium (iPad 10 iPadOS 18.6 vertical)
    pytest.param({"width":1024,"height":600},id="lg"), #large (Nest Hub horizontal)
    pytest.param({"width":1280,"height":800},id="xl"), #extra large (Nest Hub Max horizontal)
    pytest.param({"width":1920,"height":1080},id="xxl"), #extra extra large (1080p television horizontal)
])
class TestDisciplinePredPage:
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при отсутствии действий на странице
    def test_all_elements_present_and_have_required_text_no_actions(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Выберите стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("Выберите дистанцию")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Выберите пол")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("Выберите длину бассейна")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Выберите страну")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is None or not card2_title.is_visible()
        assert card2_input_swims_count_label is None or not card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count is None or not card2_input_swims_count.is_visible()
        assert (card2_apply_btn) is None or not card2_apply_btn.is_visible()
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        assert not card1_distance_invalid_feedback.is_visible()
        assert not card1_sex_invalid_feedback.is_visible()
        assert not card1_pool_length_invalid_feedback.is_visible()
        assert not card2_phase_swim_count_invalid_feedback.is_visible()
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
    
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при отсутствии действий на странице и интернета
    def test_all_elements_present_and_have_required_text_no_actions_and_no_internet(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.context.set_offline(True) #Отключить интернет как только страница загрузилась
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Выберите стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("Выберите дистанцию")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Выберите пол")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("Выберите длину бассейна")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Выберите страну")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is None or not card2_title.is_visible()
        assert card2_input_swims_count_label is None or not card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count is None or not card2_input_swims_count.is_visible()
        assert (card2_apply_btn) is None or not card2_apply_btn.is_visible()
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        assert not card1_distance_invalid_feedback.is_visible()
        assert not card1_sex_invalid_feedback.is_visible()
        assert not card1_pool_length_invalid_feedback.is_visible()
        assert not card2_phase_swim_count_invalid_feedback.is_visible()
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что существуют тосты с ошибками сети
        assert toasts_count>0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при разворачивании меню в шапке на маленьких экранах
    def test_all_elements_present_and_have_required_text_after_expand_header_menu(self,base_url,page:Page,viewport):
        if page.viewport_size['width']>=1200: #Если размер страницы большой - работать с меню нельзя!
            return
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Выберите стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("Выберите дистанцию")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Выберите пол")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("Выберите длину бассейна")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Выберите страну")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is None or not card2_title.is_visible()
        assert card2_input_swims_count_label is None or not card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count is None or not card2_input_swims_count.is_visible()
        assert (card2_apply_btn) is None or not card2_apply_btn.is_visible()
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
        
        
        
        #Проверка элементов которые зависят от размеров экрана
        assert header_btn_collapse is not None and header_btn_collapse.is_visible()
        assert header_btn_main is not None and header_btn_main.is_visible()
        assert header_btn_main.inner_text()=='Главная'
        href = header_btn_main.get_attribute("href")
        assert href=="/"
        assert header_btn_predict_swim is not None and header_btn_predict_swim.is_visible()
        assert header_btn_predict_swim.inner_text()=='Предсказать заплыв'
        href = header_btn_predict_swim.get_attribute("href")
        assert href=="swim"
        assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
        assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
        href = header_btn_predict_discipline.get_attribute("href")
        assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        assert not card1_distance_invalid_feedback.is_visible()
        assert not card1_sex_invalid_feedback.is_visible()
        assert not card1_pool_length_invalid_feedback.is_visible()
        assert not card2_phase_swim_count_invalid_feedback.is_visible()
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при разворачивании меню в шапке на маленьких экранах
    def test_all_elements_present_and_have_required_text_after_expand_collapse_header_menu(self,base_url,page:Page,viewport):
        if page.viewport_size['width']>=1200: #Если размер страницы большой - работать с меню нельзя!
            return
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Выберите стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("Выберите дистанцию")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Выберите пол")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("Выберите длину бассейна")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Выберите страну")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is None or not card2_title.is_visible()
        assert card2_input_swims_count_label is None or not card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count is None or not card2_input_swims_count.is_visible()
        assert (card2_apply_btn) is None or not card2_apply_btn.is_visible()
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
        
        
        #Проверка элементов которые зависят от размеров экрана
        assert header_btn_collapse is not None and header_btn_collapse.is_visible()
        assert header_btn_main is None or not header_btn_main.is_visible()
        assert header_btn_predict_swim is None or not header_btn_predict_swim.is_visible()
        assert header_btn_predict_discipline is None or not header_btn_predict_discipline.is_visible()
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        assert not card1_distance_invalid_feedback.is_visible()
        assert not card1_sex_invalid_feedback.is_visible()
        assert not card1_pool_length_invalid_feedback.is_visible()
        assert not card2_phase_swim_count_invalid_feedback.is_visible()
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" без заполнения полей в карточке 1
    def test_all_elements_present_and_have_required_text_after_apply_click_no_input_on_card1(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Нажать на кнопку "Применить"
        page.locator("button#buttonApplyDisciplineData").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Выберите стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("Выберите дистанцию")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Выберите пол")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("Выберите длину бассейна")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Выберите страну")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is None or not card2_title.is_visible()
        assert card2_input_swims_count_label is None or not card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count is None or not card2_input_swims_count.is_visible()
        assert (card2_apply_btn) is None or not card2_apply_btn.is_visible()
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert card1_style_invalid_feedback.is_visible()
        assert card1_style_invalid_feedback.inner_text()=="Выберите стиль плавания!"
        assert card1_distance_invalid_feedback.is_visible()
        assert card1_distance_invalid_feedback.inner_text()=="Выберите дистанцию!"
        assert card1_sex_invalid_feedback.is_visible()
        assert card1_sex_invalid_feedback.inner_text()=="Выберите пол!"
        assert card1_pool_length_invalid_feedback.is_visible()
        assert card1_pool_length_invalid_feedback.inner_text()=="Выберите длину бассейна!"
        assert not card2_phase_swim_count_invalid_feedback.is_visible()
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
    
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" без заполнения поля в карточке 2
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - вольный стиль
    #Дистанция - 50м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Испания
    #Полуфинала нет
    #Отборочных нет
    def test_all_elements_present_and_have_required_text_after_apply_click_no_input_on_card2_phases_finals(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Испания")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Испания")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе финала"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе финала:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()==""
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert card2_phase_swim_count_invalid_feedback.is_visible()
        assert card2_phase_swim_count_invalid_feedback.inner_text()=="Введите целое число от 1 до 30!"
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" без заполнения поля в карточке 2
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - вольный стиль
    #Дистанция - 50м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Испания
    #Полуфинала нет
    #Отборочные есть
    def test_all_elements_present_and_have_required_text_after_apply_click_no_input_on_card2_phases_finals_heats(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Испания")
        page.check("input#checkHasHeats")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Испания")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе отборочных"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе отборочных:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()==""
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert card2_phase_swim_count_invalid_feedback.is_visible()
        assert card2_phase_swim_count_invalid_feedback.inner_text()=="Введите целое число от 2 до 30!"
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" при заполнения поля в карточке 2 дробным числом
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - вольный стиль
    #Дистанция - 50м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Испания
    #Полуфинала нет
    #Отборочных нет
    #Ввод в карточке 2:
    #2.5
    def test_all_elements_present_and_have_required_text_after_apply_click_float_input_on_card2_phases_finals(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Испания")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Ввод дробного числа во 2 карточке
        page.locator("input#inputPhaseSwimCount").first.fill("2.5")
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Испания")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе финала"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе финала:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()=="2.5"
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert card2_phase_swim_count_invalid_feedback.is_visible()
        assert card2_phase_swim_count_invalid_feedback.inner_text()=="Введите целое число от 1 до 30!"
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" при заполнения поля в карточке 2 дробным числом
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - вольный стиль
    #Дистанция - 50м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Испания
    #Полуфинал есть
    #Отборочные есть
    #Ввод в карточке 2:
    #2.5
    def test_all_elements_present_and_have_required_text_after_apply_click_float_input_on_card2_phases_finals_semifinals_heats(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Испания")
        page.check("input#checkHasHeats")
        page.check("input#checkHasSemifinals")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Ввод дробного числа во 2 карточке
        page.locator("input#inputPhaseSwimCount").first.fill("2.5")
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Испания")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе отборочных"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе отборочных:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()=="2.5"
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert card2_phase_swim_count_invalid_feedback.is_visible()
        assert card2_phase_swim_count_invalid_feedback.inner_text()=="Введите целое число от 2 до 30!"
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" при заполнения поля в карточке 2 строкой с буквами
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - вольный стиль
    #Дистанция - 50м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Испания
    #Полуфинала нет
    #Отборочных нет
    #Ввод в карточке 2:
    #a2bc
    def test_all_elements_present_and_have_required_text_after_apply_click_string_input_on_card2_phases_finals(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Испания")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Ввод строки во 2 карточке
        input_locator = page.locator("input#inputPhaseSwimCount").first
        input_locator.evaluate("""
    el => {
        el.type = 'text';
        el.value = 'a2bc';
    }
""")
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Испания")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе финала"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе финала:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()=="a2bc"
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert card2_phase_swim_count_invalid_feedback.is_visible()
        assert card2_phase_swim_count_invalid_feedback.inner_text()=="Введите целое число от 1 до 30!"
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" при заполнения поля в карточке 2 строкой с буквами
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - вольный стиль
    #Дистанция - 50м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Испания
    #Полуфинал есть
    #Отборочные есть
    #Ввод в карточке 2:
    #a2bc
    def test_all_elements_present_and_have_required_text_after_apply_click_string_input_on_card2_phases_finals_semifinals_heats(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Испания")
        page.check("input#checkHasHeats")
        page.check("input#checkHasSemifinals")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Ввод строки во 2 карточке
        input_locator = page.locator("input#inputPhaseSwimCount").first
        input_locator.evaluate("""
    el => {
        el.type = 'text';
        el.value = 'a2bc';
    }
""")
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Испания")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе отборочных"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе отборочных:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()=="a2bc"
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert card2_phase_swim_count_invalid_feedback.is_visible()
        assert card2_phase_swim_count_invalid_feedback.inner_text()=="Введите целое число от 2 до 30!"
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" при заполнения поля в карточке 2 отрицательным числом
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - вольный стиль
    #Дистанция - 50м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Испания
    #Полуфинала нет
    #Отборочных нет
    #Ввод в карточке 2:
    #-1
    def test_all_elements_present_and_have_required_text_after_apply_click_negative_number_input_on_card2_phases_finals(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Испания")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Ввод отрицательного числа во 2 карточке
        page.locator("input#inputPhaseSwimCount").first.fill("-1")
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Испания")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе финала"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе финала:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()=="-1"
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert card2_phase_swim_count_invalid_feedback.is_visible()
        assert card2_phase_swim_count_invalid_feedback.inner_text()=="Введите целое число от 1 до 30!"
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" при заполнения поля в карточке 2 отрицательным числом
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - вольный стиль
    #Дистанция - 50м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Испания
    #Полуфинал есть
    #Отборочные есть
    #Ввод в карточке 2:
    #-1
    def test_all_elements_present_and_have_required_text_after_apply_click_negative_number_input_on_card2_phases_finals_semifinals_heats(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Испания")
        page.check("input#checkHasHeats")
        page.check("input#checkHasSemifinals")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Ввод отрицательного числа во 2 карточке
        page.locator("input#inputPhaseSwimCount").first.fill("-1")
        
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Испания")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе отборочных"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе отборочных:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()=="-1"
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert card2_phase_swim_count_invalid_feedback.is_visible()
        assert card2_phase_swim_count_invalid_feedback.inner_text()=="Введите целое число от 2 до 30!"
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" при заполнения поля в карточке 2 слишком малым числом
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - вольный стиль
    #Дистанция - 50м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Испания
    #Полуфинала нет
    #Отборочных нет
    #Ввод в карточке 2:
    #0
    def test_all_elements_present_and_have_required_text_after_apply_click_too_small_number_input_on_card2_phases_finals(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Испания")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Ввод слишком малого числа во 2 карточке
        page.locator("input#inputPhaseSwimCount").first.fill("0")
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Испания")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе финала"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе финала:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()=="0"
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert card2_phase_swim_count_invalid_feedback.is_visible()
        assert card2_phase_swim_count_invalid_feedback.inner_text()=="Введите целое число от 1 до 30!"
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" при заполнения поля в карточке 2 слишком малым числом
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - вольный стиль
    #Дистанция - 50м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Испания
    #Полуфинал есть
    #Отборочные есть
    #Ввод в карточке 2:
    #1
    def test_all_elements_present_and_have_required_text_after_apply_click_too_small_number_input_on_card2_phases_finals_semifinals_heats(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Испания")
        page.check("input#checkHasHeats")
        page.check("input#checkHasSemifinals")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Ввод слишком малого числа во 2 карточке
        page.locator("input#inputPhaseSwimCount").first.fill("1")
        
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Испания")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе отборочных"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе отборочных:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()=="1"
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert card2_phase_swim_count_invalid_feedback.is_visible()
        assert card2_phase_swim_count_invalid_feedback.inner_text()=="Введите целое число от 2 до 30!"
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" при заполнения поля в карточке 2 слишком большим числом
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - вольный стиль
    #Дистанция - 50м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Испания
    #Полуфинала нет
    #Отборочных нет
    #Ввод в карточке 2:
    #31
    def test_all_elements_present_and_have_required_text_after_apply_click_too_big_number_input_on_card2_phases_finals(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Испания")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Ввод слишком большого числа во 2 карточке
        page.locator("input#inputPhaseSwimCount").first.fill("31")
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Испания")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе финала"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе финала:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()=="31"
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert card2_phase_swim_count_invalid_feedback.is_visible()
        assert card2_phase_swim_count_invalid_feedback.inner_text()=="Введите целое число от 1 до 30!"
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" при заполнения поля в карточке 2 слишком большим числом
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - вольный стиль
    #Дистанция - 50м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Испания
    #Полуфинал есть
    #Отборочные есть
    #Ввод в карточке 2:
    #31
    def test_all_elements_present_and_have_required_text_after_apply_click_too_big_number_input_on_card2_phases_finals_semifinals_heats(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Вольный стиль")
        page.select_option("select#selectDistance",label="50м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Испания")
        page.check("input#checkHasHeats")
        page.check("input#checkHasSemifinals")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Ввод слишком большого числа во 2 карточке
        page.locator("input#inputPhaseSwimCount").first.fill("31")
        
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Вольный стиль")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("50м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Испания")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе отборочных"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе отборочных:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()=="31"
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        
        assert (card3_title) is None or not card3_title.is_visible()
        
        assert (predict_discipline_btn) is None or not predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert card2_phase_swim_count_invalid_feedback.is_visible()
        assert card2_phase_swim_count_invalid_feedback.inner_text()=="Введите целое число от 2 до 30!"
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" при заполнении карточки 3 без пловцов во всех заплывах
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - Брасс
    #Дистанция - 100м
    #Пол - женский
    #Длина бассейна - 50м
    #Страна проведения - Венгрия
    #Полуфинал есть
    #Отборочных нет
    #Карточки 2 нет (всегда 2 полуфинала):
    #Ввод в карточке 3:
    #Дата и время 1 заплыва фазы полуфинала: 01.01.2026 00:00
    #Дата и время 2 заплыва фазы полуфинала: 01.01.2026 00:00
    #Дата и время 1 заплыва фазы финала: 01.01.2026 00:15
    def test_all_elements_present_and_have_required_text_after_predict_click_no_swimmers_on_card3_phases_finals_semifinals(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Брасс")
        page.select_option("select#selectDistance",label="100м")
        page.select_option("select#selectSex",label="Женский")
        page.select_option("select#selectPoolLength",label="50м")
        page.select_option("select#selectHostCountry",label="Венгрия")
        page.check("input#checkHasSemifinals")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Развернуть все элементы аккордеона в 3 карточке
        accordeonButtons=page.locator("div#swimInputAccordeon .accordion-button")
        for i in accordeonButtons.all():
            i.click()
        #Заполнить дату и время для всех заплывов в 3 карточке
        page.locator("input#inputDatetimeSwimInputSemifinalsSwim0").fill("2026-01-01T00:00")
        page.locator("input#inputDatetimeSwimInputSemifinalsSwim1").fill("2026-01-01T00:00")
        page.locator("input#inputDatetimeSwimInputFinalsSwim0").fill("2026-01-01T00:15")
        #Нажать на кнопку прогноза
        page.locator("button#buttonPredict").click()
        
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Брасс")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("100м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Женский")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("50м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Венгрия")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is None or not card2_title.is_visible()
        assert card2_input_swims_count_label is None or not card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count is None or not card2_input_swims_count.is_visible()
        assert (card2_apply_btn) is None or not card2_apply_btn.is_visible()
        
        assert (card3_title) is not None and card3_title.is_visible()
        
        assert (predict_discipline_btn) is not None and predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert not card2_phase_swim_count_invalid_feedback.is_visible()
        assert card3_swim_input_invalid_feedback.is_visible()
        assert card3_swim_input_invalid_feedback.inner_html()=="В заплыве 1 фазы полуфинала отсутствуют пловцы!"
        
        
        #Проверка что не существуют тосты с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
        #Проверка вводного аккордеона из карточки 3 со сведениями о заплывах
        class Swim:
            def __init__(self,datetime,phase,swim_number_in_phase):
                self.datetime:str=datetime
                self.swimmers_arr:list=[None]*10
                self.phase=phase
                self.swim_number_in_phase=swim_number_in_phase
        
        swims_array=[]
        swims_array.append(Swim("2026-01-01T00:00","Semifinals",1))
        swims_array.append(Swim("2026-01-01T00:00","Semifinals",2))
        swims_array.append(Swim("2026-01-01T00:15","Finals",1))
        from_phase_to_str={"Semifinals":"полуфинала","Finals":"финала","Heats":"отборочных"}
        first_phase="Semifinals"
        for swim in swims_array:
            btn_accordion=page.get_by_text(f"Заплыв {swim.swim_number_in_phase} фазы {from_phase_to_str[swim.phase]}")
            assert btn_accordion is not None and btn_accordion.is_visible()
            assert btn_accordion.inner_text()==f"Заплыв {swim.swim_number_in_phase} фазы {from_phase_to_str[swim.phase]}"
            expect(btn_accordion).to_have_js_property("tagName","BUTTON")
            swim_datetime_input=page.locator(f"input#inputDatetimeSwimInput{swim.phase}Swim{swim.swim_number_in_phase-1}")
            assert swim_datetime_input is not None and swim_datetime_input.is_visible()
            assert swim_datetime_input.input_value()==swim.datetime
            if swim.phase==first_phase:
                for lane in range(10):
                    swimmer_select=page.locator(f"select#selectSwimmer{swim.phase}{swim.swim_number_in_phase-1}Lane{lane}")
                    swimmer_select
                    assert(swimmer_select) is not None and swimmer_select.is_visible()
                    expect(swimmer_select.locator("option:checked")).to_have_text(swim.swimmers_arr[lane] if swim.swimmers_arr[lane] is not None else "Нет пловца")
                    expect(swimmer_select).to_have_js_property("tagName","SELECT")
                    
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" 
    # при корректном заполнении карточки 3 но при нажатии на кнопку прогноза без интернета
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - На спине
    #Дистанция - 200м
    #Пол - мужской
    #Длина бассейна - 25м
    #Страна проведения - Турция
    #Полуфинала нет
    #Отборочных нет
    #В карточке 2 выбрано число финалов:
    #1
    #Ввод в карточке 3:
    #Дата и время 1 заплыва фазы финала: 31.12.2049 23:59:59
    #Пловец на дорожке 3: LIENDO Josh
    #Пловец на дорожке 4: ALEXY Jack
    #Пловец на дорожке 5: JETT Gabriel
    def test_all_elements_present_and_have_required_text_after_predict_click_valid_input_no_internet_on_card3_phases_finals(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="На спине")
        page.select_option("select#selectDistance",label="200м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="25м")
        page.select_option("select#selectHostCountry",label="Турция")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Выбрать число заплывов (1) в финале
        page.locator("input#inputPhaseSwimCount").first.fill("1")
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
        #Развернуть все элементы аккордеона в 3 карточке
        accordeonButtons=page.locator("div#swimInputAccordeon .accordion-button")
        for i in accordeonButtons.all():
            i.click()
        #Заполнить дату и время для всех заплывов в 3 карточке
        page.locator("input#inputDatetimeSwimInputFinalsSwim0").fill("2049-12-31T23:59:59")
        page.context.set_offline(True) #Выключить интернет
        
        #Выбрать пловцов
        page.locator("#selectSwimmerFinals0Lane3 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerFinals0Lane3 + .ts-wrapper input").fill("LIENDO")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerFinals0Lane3 + .ts-wrapper .ts-dropdown .option", has_text="LIENDO Josh").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerFinals0Lane4 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerFinals0Lane4 + .ts-wrapper input").fill("ALEXY")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerFinals0Lane4 + .ts-wrapper .ts-dropdown .option", has_text="ALEXY Jack").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerFinals0Lane5 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerFinals0Lane5 + .ts-wrapper input").fill("JETT")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerFinals0Lane5 + .ts-wrapper .ts-dropdown .option", has_text="JETT Gabriel").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        #Нажать на кнопку прогноза
        page.locator("button#buttonPredict").click()
        
        page.wait_for_timeout(1000) #Подождать анимацию
        
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("На спине")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("200м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("25м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Турция")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).not_to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).not_to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе финала"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе финала:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()=='1'
        assert card2_input_swims_count.is_disabled()
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        assert card2_apply_btn.is_disabled()
        
        assert (card3_title) is not None and card3_title.is_visible()
        
        assert (predict_discipline_btn) is not None and predict_discipline_btn.is_visible()
        
        assert results_accordion is None or not results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert not card2_phase_swim_count_invalid_feedback.is_visible()
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        
        #Проверка что существуют тосты с ошибками сети
        assert toasts_count>0
        
        #Проверка что результатов заплывов 0
        assert visible_result_swims_count==0
        
        #Проверка что результатов пловцов в заплывах 0
        assert visible_result_swimmers_count==0
        
        #Проверка вводного аккордеона из карточки 3 со сведениями о заплывах
        class Swim:
            def __init__(self,datetime,phase,swim_number_in_phase):
                self.datetime:str=datetime
                self.swimmers_arr:list=[None]*10
                self.phase=phase
                self.swim_number_in_phase=swim_number_in_phase
        
        swims_array=[]
        swims_array.append(Swim("2049-12-31T23:59:59","Finals",1))
        swims_array[0].swimmers_arr[3]="LIENDO Josh"
        swims_array[0].swimmers_arr[4]="ALEXY Jack"
        swims_array[0].swimmers_arr[5]="JETT Gabriel"
        from_phase_to_str={"Semifinals":"полуфинала","Finals":"финала","Heats":"отборочных"}
        first_phase="Finals"
        for swim in swims_array:
            btn_accordion=page.get_by_text(f"Заплыв {swim.swim_number_in_phase} фазы {from_phase_to_str[swim.phase]}")
            assert btn_accordion is not None and btn_accordion.is_visible()
            assert btn_accordion.inner_text()==f"Заплыв {swim.swim_number_in_phase} фазы {from_phase_to_str[swim.phase]}"
            expect(btn_accordion).to_have_js_property("tagName","BUTTON")
            swim_datetime_input=page.locator(f"input#inputDatetimeSwimInput{swim.phase}Swim{swim.swim_number_in_phase-1}")
            assert swim_datetime_input is not None and swim_datetime_input.is_visible()
            assert swim_datetime_input.input_value()==swim.datetime
            if swim.phase==first_phase:
                for lane in range(10):
                    swimmer_select=page.locator(f"select#selectSwimmer{swim.phase}{swim.swim_number_in_phase-1}Lane{lane}")
                    swimmer_select
                    assert(swimmer_select) is not None and swimmer_select.is_visible()
                    expect(swimmer_select.locator("option:checked")).to_have_text(swim.swimmers_arr[lane] if swim.swimmers_arr[lane] is not None else "Нет пловца")
                    expect(swimmer_select).to_have_js_property("tagName","SELECT")
                    
    #Проверить что все нужные элементы прогрузились (а ненужные не видны или не существуют) при нажатии на кнопку "применить" 
    # при корректном заполнении карточки 3
    #Перед этим в карточке 1 был следующий ввод:
    #Стиль плавания - Комплексный
    #Дистанция - 400м
    #Пол - Мужской
    #Длина бассейна - 50м
    #Страна проведения - Мексика
    #Полуфинал есть
    #Отборочные есть
    #В карточке 2 выбрано число отборочных:
    #3
    #Ввод в карточке 3:
    #Дата и время 1 заплыва фазы отборочных: 01.01.2026 01:01:01
    #Пловец на дорожке 0: LIENDO Josh
    #Пловец на дорожке 1: HOBSON Luke
    #Пловец на дорожке 2: SCHOTT Mitchell
    #Пловец на дорожке 3: ALEXY Jack
    #Пловец на дорожке 4: LITCHFIELD Max
    #Пловец на дорожке 5: KOS Hubert
    #Пловец на дорожке 6: GUILIANO Chris
    #Пловец на дорожке 7: KHARUN Ilya
    #Пловец на дорожке 8: GIULIANI Maximillian
    #Пловец на дорожке 9: STANTON Michael C
    #Дата и время 2 заплыва фазы отборочных: 01.01.2026 01:01:01
    #Пловец на дорожке 0: GUTIERREZ Santiago
    #Пловец на дорожке 1: CECCON Thomas
    #Пловец на дорожке 2: STOKOWSKI Kacper
    #Пловец на дорожке 3: RICHARDS Matthew
    #Пловец на дорожке 4: TAYLOR Lamar
    #Пловец на дорожке 5: TRIBUNTSOV Ralf
    #Пловец на дорожке 6: GAZIEV Ruslan
    #Пловец на дорожке 7: CORBEAU Caspar
    #Пловец на дорожке 8: MACDONALD Connor
    #Пловец на дорожке 9: FONSECA Simon
    #Дата и время 3 заплыва фазы отборочных: 01.01.2026 01:01:01
    #Пловец на дорожке 0: SMITH Kieran
    #Пловец на дорожке 1: KNOX Finlay
    #Пловец на дорожке 2: GRAY Cameron
    #Пловец на дорожке 3: DINU Patrick Sebastian
    #Пловец на дорожке 4: MORA Lorenzo
    #Пловец на дорожке 5: LEPINE Alexandre
    #Пловец на дорожке 6: PEATY Adam
    #Пловец на дорожке 7: CHIRINOS Franco
    #Пловец на дорожке 8: SHORT Samuel
    #Пловец на дорожке 9: JETT Gabriel
    #Дата и время 1 заплыва фазы полуфинала: 01.01.2026 01:16:01
    #Дата и время 2 заплыва фазы полуфинала: 01.01.2026 01:16:01
    #Дата и время 1 заплыва фазы финала: 01.01.2026 01:31:01
    def test_all_elements_present_and_have_required_text_after_predict_click_valid_input_on_card3_phases_finals_semifinals_heats(self,base_url,page:Page,viewport):
        url=base_url if base_url else BASE_URL_DEFAULT
        url=url+DISCIPLINE_PAGE_PATH
        page.goto(url) #Перейти по ссылке
        page.context.set_default_timeout(5000)
        page.wait_for_load_state("networkidle") #Дождаться полной загрузки страницы
        #Ввод сведений о дисциплине
        page.select_option("select#selectStyle",label="Комплексный")
        page.select_option("select#selectDistance",label="400м")
        page.select_option("select#selectSex",label="Мужской")
        page.select_option("select#selectPoolLength",label="50м")
        page.select_option("select#selectHostCountry",label="Мексика")
        page.check("input#checkHasSemifinals")
        page.check("input#checkHasHeats")
        #Нажать на кнопку "Применить" в 1 карточке
        page.locator("button#buttonApplyDisciplineData").first.click()
        #Выбрать число заплывов (3) в отборочных
        page.locator("input#inputPhaseSwimCount").first.fill("3")
        #Нажать на кнопку "Применить" во 2 карточке
        page.locator("button#buttonApplyPhaseSwimCount").first.click()
        #Развернуть все элементы аккордеона в 3 карточке
        accordeonButtons=page.locator("div#swimInputAccordeon .accordion-button")
        for i in accordeonButtons.all():
            i.click()
        #Заполнить дату и время для всех заплывов в 3 карточке
        page.locator("input#inputDatetimeSwimInputHeatsSwim0").fill("2026-01-01T01:01:01")
        page.locator("input#inputDatetimeSwimInputHeatsSwim1").fill("2026-01-01T01:01:01")
        page.locator("input#inputDatetimeSwimInputHeatsSwim2").fill("2026-01-01T01:01:01")
        page.locator("input#inputDatetimeSwimInputSemifinalsSwim0").fill("2026-01-01T01:16:01")
        page.locator("input#inputDatetimeSwimInputSemifinalsSwim1").fill("2026-01-01T01:16:01")
        page.locator("input#inputDatetimeSwimInputFinalsSwim0").fill("2026-01-01T01:31:01")
        
        #Выбрать пловцов
        page.locator("#selectSwimmerHeats0Lane0 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats0Lane0 + .ts-wrapper input").fill("LIENDO")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats0Lane0 + .ts-wrapper .ts-dropdown .option", has_text="LIENDO Josh").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats0Lane1 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats0Lane1 + .ts-wrapper input").fill("HOBSON")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats0Lane1 + .ts-wrapper .ts-dropdown .option", has_text="HOBSON Luke").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats0Lane2 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats0Lane2 + .ts-wrapper input").fill("SCHOTT")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats0Lane2 + .ts-wrapper .ts-dropdown .option", has_text="SCHOTT Mitchell").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats0Lane3 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats0Lane3 + .ts-wrapper input").fill("ALEXY")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats0Lane3 + .ts-wrapper .ts-dropdown .option", has_text="ALEXY Jack").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats0Lane4 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats0Lane4 + .ts-wrapper input").fill("LITCHFIELD")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats0Lane4 + .ts-wrapper .ts-dropdown .option", has_text="LITCHFIELD Max").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats0Lane5 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats0Lane5 + .ts-wrapper input").fill("KOS")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats0Lane5 + .ts-wrapper .ts-dropdown .option", has_text="KOS Hubert").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats0Lane6 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats0Lane6 + .ts-wrapper input").fill("GUILIANO")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats0Lane6 + .ts-wrapper .ts-dropdown .option", has_text="GUILIANO Chris").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats0Lane7 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats0Lane7 + .ts-wrapper input").fill("KHARUN")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats0Lane7 + .ts-wrapper .ts-dropdown .option", has_text="KHARUN Ilya").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats0Lane8 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats0Lane8 + .ts-wrapper input").fill("GIULIANI")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats0Lane8 + .ts-wrapper .ts-dropdown .option", has_text="GIULIANI Maximillian").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats0Lane9 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats0Lane9 + .ts-wrapper input").fill("STANTON")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats0Lane9 + .ts-wrapper .ts-dropdown .option", has_text="STANTON Michael C").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmerHeats1Lane0 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats1Lane0 + .ts-wrapper input").fill("GUTIERREZ")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats1Lane0 + .ts-wrapper .ts-dropdown .option", has_text="GUTIERREZ Santiago").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats1Lane1 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats1Lane1 + .ts-wrapper input").fill("CECCON")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats1Lane1 + .ts-wrapper .ts-dropdown .option", has_text="CECCON Thomas").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats1Lane2 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats1Lane2 + .ts-wrapper input").fill("STOKOWSKI")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats1Lane2 + .ts-wrapper .ts-dropdown .option", has_text="STOKOWSKI Kacper").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats1Lane3 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats1Lane3 + .ts-wrapper input").fill("RICHARDS")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats1Lane3 + .ts-wrapper .ts-dropdown .option", has_text="RICHARDS Matthew").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats1Lane4 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats1Lane4 + .ts-wrapper input").fill("TAYLOR")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats1Lane4 + .ts-wrapper .ts-dropdown .option", has_text="TAYLOR Lamar").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats1Lane5 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats1Lane5 + .ts-wrapper input").fill("TRIBUNTSOV")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats1Lane5 + .ts-wrapper .ts-dropdown .option", has_text="TRIBUNTSOV Ralf").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats1Lane6 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats1Lane6 + .ts-wrapper input").fill("GAZIEV")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats1Lane6 + .ts-wrapper .ts-dropdown .option", has_text="GAZIEV Ruslan").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats1Lane7 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats1Lane7 + .ts-wrapper input").fill("CORBEAU")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats1Lane7 + .ts-wrapper .ts-dropdown .option", has_text="CORBEAU Caspar").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats1Lane8 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats1Lane8 + .ts-wrapper input").fill("MACDONALD")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats1Lane8 + .ts-wrapper .ts-dropdown .option", has_text="MACDONALD Connor").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats1Lane9 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats1Lane9 + .ts-wrapper input").fill("FONSECA")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats1Lane9 + .ts-wrapper .ts-dropdown .option", has_text="FONSECA Simon").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        page.locator("#selectSwimmerHeats2Lane0 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats2Lane0 + .ts-wrapper input").fill("SMITH")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats2Lane0 + .ts-wrapper .ts-dropdown .option", has_text="SMITH Kieran").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats2Lane1 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats2Lane1 + .ts-wrapper input").fill("KNOX")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats2Lane1 + .ts-wrapper .ts-dropdown .option", has_text="KNOX Finlay").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats2Lane2 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats2Lane2 + .ts-wrapper input").fill("GRAY")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats2Lane2 + .ts-wrapper .ts-dropdown .option", has_text="GRAY Cameron").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats2Lane3 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats2Lane3 + .ts-wrapper input").fill("DINU")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats2Lane3 + .ts-wrapper .ts-dropdown .option", has_text="DINU Patrick Sebastian").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats2Lane4 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats2Lane4 + .ts-wrapper input").fill("MORA")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats2Lane4 + .ts-wrapper .ts-dropdown .option", has_text="MORA Lorenzo").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats2Lane5 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats2Lane5 + .ts-wrapper input").fill("LEPINE")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats2Lane5 + .ts-wrapper .ts-dropdown .option", has_text="LEPINE Alexandre").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats2Lane6 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats2Lane6 + .ts-wrapper input").fill("PEATY")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats2Lane6 + .ts-wrapper .ts-dropdown .option", has_text="PEATY Adam").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats2Lane7 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats2Lane7 + .ts-wrapper input").fill("CHIRINOS")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats2Lane7 + .ts-wrapper .ts-dropdown .option", has_text="CHIRINOS Franco").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats2Lane8 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats2Lane8 + .ts-wrapper input").fill("SHORT")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats2Lane8 + .ts-wrapper .ts-dropdown .option", has_text="SHORT Samuel").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        page.locator("#selectSwimmerHeats2Lane9 + .ts-wrapper input").focus()
        page.locator("#selectSwimmerHeats2Lane9 + .ts-wrapper input").fill("JETT")
        page.wait_for_timeout(500) #Ожидание фильтра
        page.locator("#selectSwimmerHeats2Lane9 + .ts-wrapper .ts-dropdown .option", has_text="JETT Gabriel").click()
        page.keyboard.press("Escape")  # закрыть томселект
        page.wait_for_timeout(400) #Подождать пока томселект закроется
        
        #Нажать на кнопку прогноза
        page.locator("button#buttonPredict").click()
        page.wait_for_timeout(2000) #Подождать результатов
        
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
            card1_title=page.get_by_text('Введите сведения о дисциплине').first
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
            card1_pool_length_label=page.get_by_text('Длина бассейна:').first
        except:
            card1_pool_length_label=None
        try:
            card1_host_country_label=page.get_by_text('Страна проведения:').first
        except:
            card1_host_country_label=None
        try:
            card1_has_semifinals_label=page.get_by_text('Есть ли в дисциплине полуфинал:').first
        except:
            card1_has_semifinals_label=None
        try:
            card1_has_heats_label=page.get_by_text('Есть ли в дисциплине отборочные:').first
        except:
            card1_has_heats_label=None
        
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
            card1_pool_length_select=page.locator('select').filter(has_text="Выберите длину бассейна").first
        except:
            card1_pool_length_select=None
        try:
            card1_host_country_select=page.locator('select').filter(has_text="Выберите страну").first
        except:
            card1_host_country_select=None
        try:
            card1_has_semifinals_checkbox=page.locator('input#checkHasSemifinals').first
        except:
            card1_has_semifinals_checkbox=None
        try:
            card1_has_heats_checkbox=page.locator('input#checkHasHeats').first
        except:
            card1_has_heats_checkbox=None
        try:
            card1_style_invalid_feedback=page.locator('div#styleInvalidFeedback').first
        except:
            card1_style_invalid_feedback=None
        try:
            card1_distance_invalid_feedback=page.locator('div#distanceInvalidFeedback').first
        except:
            card1_distance_invalid_feedback=None
        try:
            card1_sex_invalid_feedback=page.locator('div#sexInvalidFeedback').first
        except:
            card1_sex_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_pool_length_invalid_feedback=page.locator('div#poolLengthInvalidFeedback').first
        except:
            card1_pool_length_invalid_feedback=None
        try:
            card1_apply_btn=page.locator('button#buttonApplyDisciplineData').first
        except:
            card1_apply_btn=None
        
        try:
            card2_title=page.get_by_text('Введите число заплывов в фазе').first
        except:
            card2_title=None
        try:
            card2_input_swims_count_label=page.get_by_text('Введите число заплывов в фазе').nth(1)
        except:
            card2_input_swims_count_label=None
        try:
            card2_input_swims_count=page.locator('input#inputPhaseSwimCount').first
        except:
            card2_input_swims_count=None
        try:
            card2_apply_btn=page.locator('button#buttonApplyPhaseSwimCount').first
        except:
            card2_apply_btn=None
        try:
            card2_phase_swim_count_invalid_feedback=page.locator('div#phaseSwimCountInvalidFeedback').first
        except:
            card2_phase_swim_count_invalid_feedback=None
        
        
        try:
            card3_title=page.get_by_text('Введите сведения о заплывах').first
        except:
            card3_title=None
        try:
            card3_swim_input_invalid_feedback=page.locator('div#swimInputInvalidFeedback').first
        except:
            card3_swim_input_invalid_feedback=None
        
        
        try:
            predict_discipline_btn=page.locator('button#buttonPredict').first
        except:
            predict_discipline_btn=None
        
        try:
            graphs_modal=page.locator('#graphsModal').first
        except:
            graphs_modal=None
        
        #Раскрыть аккордеон с результатами
        results_accordeon_buttons_count=page.locator('div#resultsAccordion .accordion-button').count()
        for i in range(results_accordeon_buttons_count):
            page.locator('div#resultsAccordion .accordion-button').nth(i).click()
            page.wait_for_timeout(600) #Подождать раскрытия аккордеона
        
        try:
            visible_result_swims_count=page.locator("div#resultsAccordion > div").filter(visible=True).count() #Число выходных результатов заплывов
        except:
            visible_result_swims_count=0
            
        try:
            visible_result_swimmers_count=page.locator("div#resultsAccordion div.row").filter(visible=True).count() #Число выходных результатов пловцов во всех результирующих заплывах
        except:
            visible_result_swimmers_count=0
        
        try:
            results_accordion=page.locator("div#resultsAccordion").filter(visible=True).first
        except:
            results_accordion=None
        
        try:
            toasts_count=page.locator("div.toast").filter(visible=True).count()
        except:
            toasts_count=0
            
        #Проверка элементов которые не зависят от размера экрана
        assert header_title is not None and header_title.is_visible()
        assert header_title.inner_text()=="Система прогноза результатов по плаванию"
        expect(header_title).to_have_js_property("tagName","A")
        assert(card1_title) is not None and card1_title.is_visible()
        assert card1_title.inner_text()=="Введите сведения о дисциплине"
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
        assert(card1_pool_length_label) is not None and card1_pool_length_label.is_visible()
        assert card1_pool_length_label.inner_text()=="Длина бассейна:"
        expect(card1_pool_length_label).to_have_js_property("tagName","LABEL")
        assert(card1_host_country_label) is not None and card1_host_country_label.is_visible()
        assert card1_host_country_label.inner_text()=="Страна проведения:"
        expect(card1_host_country_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_semifinals_label) is not None and card1_has_semifinals_label.is_visible()
        assert card1_has_semifinals_label.inner_text()=="Есть ли в дисциплине полуфинал:"
        expect(card1_has_semifinals_label).to_have_js_property("tagName","LABEL")
        assert(card1_has_heats_label) is not None and card1_has_heats_label.is_visible()
        assert card1_has_heats_label.inner_text()=="Есть ли в дисциплине отборочные:"
        expect(card1_has_heats_label).to_have_js_property("tagName","LABEL")
        assert(card1_style_select) is not None and card1_style_select.is_visible()
        expect(card1_style_select.locator("option:checked")).to_have_text("Комплексный")
        expect(card1_style_select).to_have_js_property("tagName","SELECT")
        assert(card1_style_select).is_disabled()
        assert(card1_distance_select) is not None and card1_distance_select.is_visible()
        expect(card1_distance_select.locator("option:checked")).to_have_text("400м")
        expect(card1_distance_select).to_have_js_property("tagName","SELECT")
        assert(card1_distance_select).is_disabled()
        assert(card1_sex_select) is not None and card1_sex_select.is_visible()
        expect(card1_sex_select.locator("option:checked")).to_have_text("Мужской")
        expect(card1_sex_select).to_have_js_property("tagName","SELECT")
        assert(card1_sex_select).is_disabled()
        assert(card1_pool_length_select) is not None and card1_pool_length_select.is_visible()
        expect(card1_pool_length_select.locator("option:checked")).to_have_text("50м")
        expect(card1_pool_length_select).to_have_js_property("tagName","SELECT")
        assert(card1_pool_length_select).is_disabled()
        assert(card1_host_country_select) is not None and card1_host_country_select.is_visible()
        expect(card1_host_country_select.locator("option:checked")).to_have_text("Мексика")
        expect(card1_host_country_select).to_have_js_property("tagName","SELECT")
        assert(card1_host_country_select).is_disabled()
        assert(card1_has_heats_checkbox) is not None and card1_has_heats_checkbox.is_visible()
        expect(card1_has_heats_checkbox).to_be_checked()
        expect(card1_has_heats_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_heats_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_heats_checkbox).is_disabled()
        assert(card1_has_semifinals_checkbox) is not None and card1_has_semifinals_checkbox.is_visible()
        expect(card1_has_semifinals_checkbox).to_be_checked()
        expect(card1_has_semifinals_checkbox).to_have_js_property("tagName","INPUT")
        expect(card1_has_semifinals_checkbox).to_have_attribute("type","checkbox")
        assert(card1_has_semifinals_checkbox).is_disabled()
        assert(card1_apply_btn) is not None and card1_apply_btn.is_visible()
        assert card1_apply_btn.inner_text()=="Применить"
        
        assert (card2_title) is not None and card2_title.is_visible()
        assert card2_title.inner_text()=="Введите число заплывов в фазе отборочных"
        assert card2_input_swims_count_label is not None and card2_input_swims_count_label.is_visible()
        assert card2_input_swims_count_label.inner_text()=="Введите число заплывов в фазе отборочных:"
        assert card2_input_swims_count is not None and card2_input_swims_count.is_visible()
        assert card2_input_swims_count.input_value()=='3'
        assert card2_input_swims_count.is_disabled()
        assert (card2_apply_btn) is not None and card2_apply_btn.is_visible()
        assert card2_apply_btn.inner_text()=="Применить"
        assert card2_apply_btn.is_disabled()
        
        assert (card3_title) is not None and card3_title.is_visible()
        
        assert (predict_discipline_btn) is not None and predict_discipline_btn.is_visible()
        
        assert results_accordion is not None and results_accordion.is_visible()
        
        
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
            assert href=="swim"
            assert header_btn_predict_discipline is not None and header_btn_predict_discipline.is_visible()
            assert header_btn_predict_discipline.inner_text()=='Предсказать дисциплину'
            href = header_btn_predict_discipline.get_attribute("href")
            assert href=="" or href is None
        
        #Проверка элементов которых не должно быть видно (модальные окна)
        assert not graphs_modal.is_visible()
        
        #Проверка сообщений об ошибках ввода
        assert not card1_style_invalid_feedback.is_visible()
        
        assert not card1_distance_invalid_feedback.is_visible()
        
        assert not card1_sex_invalid_feedback.is_visible()
        
        assert not card1_pool_length_invalid_feedback.is_visible()
        
        assert not card2_phase_swim_count_invalid_feedback.is_visible()
        assert not card3_swim_input_invalid_feedback.is_visible()
        
        
        
        #Проверка что не существует тостов с ошибками сети
        assert toasts_count==0
        
        #Проверка что результатов заплывов 6
        assert visible_result_swims_count==6
        
        #Проверка что результатов пловцов в заплывах 30+16+8=54
        assert visible_result_swimmers_count==54
        
        #Проверка вводного аккордеона из карточки 3 со сведениями о заплывах
        class Swim:
            def __init__(self,datetime,phase,swim_number_in_phase):
                self.datetime:str=datetime
                self.swimmers_arr:list=[None]*10
                self.phase=phase
                self.swim_number_in_phase=swim_number_in_phase
        
        swims_array=[]
        swims_array.append(Swim("2026-01-01T01:01:01","Heats",1))
        swims_array[0].swimmers_arr[0]="LIENDO Josh"
        swims_array[0].swimmers_arr[1]="HOBSON Luke"
        swims_array[0].swimmers_arr[2]="SCHOTT Mitchell"
        swims_array[0].swimmers_arr[3]="ALEXY Jack"
        swims_array[0].swimmers_arr[4]="LITCHFIELD Max"
        swims_array[0].swimmers_arr[5]="KOS Hubert"
        swims_array[0].swimmers_arr[6]="GUILIANO Chris"
        swims_array[0].swimmers_arr[7]="KHARUN Ilya"
        swims_array[0].swimmers_arr[8]="GIULIANI Maximillian"
        swims_array[0].swimmers_arr[9]="STANTON Michael C"
        swims_array.append(Swim("2026-01-01T01:01:01","Heats",2))
        swims_array[-1].swimmers_arr[0]="GUTIERREZ Santiago"
        swims_array[-1].swimmers_arr[1]="CECCON Thomas"
        swims_array[-1].swimmers_arr[2]="STOKOWSKI Kacper"
        swims_array[-1].swimmers_arr[3]="RICHARDS Matthew"
        swims_array[-1].swimmers_arr[4]="TAYLOR Lamar"
        swims_array[-1].swimmers_arr[5]="TRIBUNTSOV Ralf"
        swims_array[-1].swimmers_arr[6]="GAZIEV Ruslan"
        swims_array[-1].swimmers_arr[7]="CORBEAU Caspar"
        swims_array[-1].swimmers_arr[8]="MACDONALD Connor"
        swims_array[-1].swimmers_arr[9]="FONSECA Simon"
        swims_array.append(Swim("2026-01-01T01:01:01","Heats",3))
        swims_array[-1].swimmers_arr[0]="SMITH Kieran"
        swims_array[-1].swimmers_arr[1]="KNOX Finlay"
        swims_array[-1].swimmers_arr[2]="GRAY Cameron"
        swims_array[-1].swimmers_arr[3]="DINU Patrick Sebastian"
        swims_array[-1].swimmers_arr[4]="MORA Lorenzo"
        swims_array[-1].swimmers_arr[5]="LEPINE Alexandre"
        swims_array[-1].swimmers_arr[6]="PEATY Adam"
        swims_array[-1].swimmers_arr[7]="CHIRINOS Franco"
        swims_array[-1].swimmers_arr[8]="SHORT Samuel"
        swims_array[-1].swimmers_arr[9]="JETT Gabriel"
        swims_array.append(Swim("2026-01-01T01:16:01","Semifinals",1))
        swims_array.append(Swim("2026-01-01T01:16:01","Semifinals",2))
        swims_array.append(Swim("2026-01-01T01:31:01","Finals",1))
        from_phase_to_str={"Semifinals":"полуфинала","Finals":"финала","Heats":"отборочных"}
        first_phase="Heats"
        for swim in swims_array:
            btn_accordion=page.locator('#resultsAccordion').get_by_text(f"Заплыв {swim.swim_number_in_phase} фазы {from_phase_to_str[swim.phase]}")
            assert btn_accordion is not None and btn_accordion.is_visible()
            assert btn_accordion.inner_text()==f"Заплыв {swim.swim_number_in_phase} фазы {from_phase_to_str[swim.phase]}"
            expect(btn_accordion).to_have_js_property("tagName","BUTTON")
            swim_datetime_input=page.locator(f"input#inputDatetimeSwimInput{swim.phase}Swim{swim.swim_number_in_phase-1}")
            assert swim_datetime_input is not None and swim_datetime_input.is_visible()
            assert swim_datetime_input.input_value()==swim.datetime
            if swim.phase==first_phase:
                for lane in range(10):
                    swimmer_select=page.locator(f"select#selectSwimmer{swim.phase}{swim.swim_number_in_phase-1}Lane{lane}")
                    swimmer_select
                    assert(swimmer_select) is not None and swimmer_select.is_visible()
                    expect(swimmer_select.locator("option:checked")).to_have_text(swim.swimmers_arr[lane] if swim.swimmers_arr[lane] is not None else "Нет пловца")
                    expect(swimmer_select).to_have_js_property("tagName","SELECT")
                    
        #Проверка результатов
        cur_phase="Heats"
        cur_swims_arr=swims_array[:3]
        class swimmerResult:
            def __init__(self,name,phase_place,swim_place,result_time,lane):
                self.name:str=name
                self.phase_place:int=phase_place
                self.swim_place:int=swim_place
                self.result_time:float=result_time
                self.lane=lane
        
        while cur_phase!="":
            
            #Собираем результаты пловцов
            swimmers_results_in_cur_phase=[]
            for ind,swim in enumerate(cur_swims_arr):
                cur_swim_accordeon_button=page.locator(f'button[data-bs-target="#resultsAccordionEntry{swim.phase}{swim.swim_number_in_phase-1}"]')
                assert cur_swim_accordeon_button.is_visible()
                assert cur_swim_accordeon_button.inner_text()==f"Заплыв {swim.swim_number_in_phase} фазы {from_phase_to_str[swim.phase]}"
                swimmer_rows=page.locator(f'#resultsAccordionEntry{swim.phase}{swim.swim_number_in_phase-1} > div > div.row')
                swimmers_results_in_swim=[]
                for swimmer_row in swimmer_rows.all():
                    assert swimmer_row.locator('> div').first.locator('> div').first.is_visible() and swimmer_row.locator('> div').first.locator('> div').first.inner_text()=="Дорожка:"
                    assert swimmer_row.locator('> div').nth(1).locator('> div').first.is_visible() and swimmer_row.locator('> div').nth(1).locator('> div').first.inner_text()=="Пловец:"
                    assert swimmer_row.locator('> div').nth(2).locator('> div').first.is_visible() and swimmer_row.locator('> div').nth(2).locator('> div').first.inner_text()=="Время:"
                    assert swimmer_row.locator('> div').nth(3).locator('> div').first.is_visible() and swimmer_row.locator('> div').nth(3).locator('> div').first.inner_text()=="Место (заплыв):"
                    assert swimmer_row.locator('> div').nth(4).locator('> div').first.is_visible() and swimmer_row.locator('> div').nth(4).locator('> div').first.inner_text()=="Место (фаза):"
                    assert swimmer_row.locator('> div').nth(5).locator('> button').first.is_visible() and swimmer_row.locator('> div').nth(5).locator('> button').first.inner_text()=="Графики..."
                    lane=int(swimmer_row.locator('> div').first.locator('> div').nth(1).inner_text())
                    name=swimmer_row.locator('> div').nth(1).locator('> div').nth(1).inner_text()
                    time_str=swimmer_row.locator('> div').nth(2).locator('> div').nth(1).inner_text()
                    if ':' in time_str:
                        parts = time_str.split(':')
                        if len(parts)==2:
                            time = float(parts[0]) * 60 + float(parts[1])
                        elif len(parts)==3:
                            time = float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
                    else:
                        time = float(time_str)
                    swim_place=int(swimmer_row.locator('> div').nth(3).locator('> div').nth(1).inner_text())
                    phase_place=int(swimmer_row.locator('> div').nth(4).locator('> div').nth(1).inner_text())
                    swimmers_results_in_swim.append(swimmerResult(name,phase_place,swim_place,time,lane))
                    show_graphs_btn=swimmer_row.locator('> div').nth(5).locator('> button').first
                    #Проверить имя на соответствие
                    assert name==cur_swims_arr[ind].swimmers_arr[lane]
                    
                    #Проверить что модалка с графиками видна при нажатии на кнопку и соответствует ожидаемому
                    show_graphs_btn.click()
                    page.wait_for_timeout(300) #Ждем прогрузки графиков
                    graphs_modal=page.locator("div#graphsModal")
                    assert graphs_modal.is_visible() #Проверка что видно модалку
                    graphs_modal_title=page.locator("div.modal-header")
                    assert graphs_modal_title.is_visible() and graphs_modal_title.inner_text()==f"Графики для пловца {name} в заплыве {swim.swim_number_in_phase} фазы {from_phase_to_str[swim.phase]}" #Проверка на видимость и содержание заголовка модалки
                    canvas_height_dependency=page.locator("canvas#canvasHeightDependency")
                    canvas_height_dependency_label=page.locator("label#canvasHeightDependencyLabel")
                    #Проверка на видимость графика зависимости от роста (или на видимость соответствующей надписи о том что графика нет)
                    assert canvas_height_dependency.is_visible() and not canvas_height_dependency_label.is_visible() or \
                        not canvas_height_dependency.is_visible() and canvas_height_dependency_label.is_visible() and canvas_height_dependency_label.inner_text()=="График зависимости времени от роста пловца отсутствует, так как рост пловца неизвестен!"
                    canvas_age_dependency=page.locator("canvas#canvasAgeDependency")
                    canvas_age_dependency_label=page.locator("label#canvasAgeDependencyLabel")
                    #Проверка на видимость графика зависимости от возраста (или на видимость соответствующей надписи о том что графика нет)
                    assert canvas_age_dependency.is_visible() and not canvas_age_dependency_label.is_visible() or \
                        not canvas_age_dependency.is_visible() and canvas_age_dependency_label.is_visible() and canvas_age_dependency_label.inner_text()=="График зависимости времени от возраста пловца отсутствует, так как возраст пловца неизвестен!"
                    canvas_lane_dependency=page.locator("canvas#canvasLaneDependency")
                    #Проверка на видимость графика зависимости от дорожки
                    assert canvas_lane_dependency.is_visible()
                    graphs_modal_close_btn=page.locator("div.modal-header button.btn-close")
                    assert graphs_modal_close_btn.is_visible() #Проверка что кнопка закрытия видна
                    
                    #Проверить что модалка с графиками не видна при нажатии на кнопку закрытия модалки
                    graphs_modal_close_btn.click()
                    page.wait_for_timeout(300) #Ждем закрытия модалки
                    assert not graphs_modal.is_visible() #Проверка что не видно модалку
                    assert not graphs_modal_title.is_visible() #Проверка что не видно заголовок модалки
                    assert not canvas_height_dependency.is_visible() and not canvas_height_dependency_label.is_visible() #Проверка что не видно график зависимости от роста и не видно надпись о его отсутствии
                    assert not canvas_age_dependency.is_visible() and not canvas_age_dependency_label.is_visible() #Проверка что не видно график зависимости от возраста и не видно надпись о его отсутствии
                    assert not canvas_lane_dependency.is_visible()  #Проверка что не видно график зависимости от дорожки
                    assert not graphs_modal_close_btn.is_visible() #Проверка что кнопка закрытия модалки не видна
                swimmers_results_in_swim=sorted(swimmers_results_in_swim, key=lambda x:x.phase_place)
                #Проверить что места пловцов соответствуют времени и последовательны и начинаются с 1, проверить что место в заплыве уникально
                assert swimmers_results_in_swim[0].swim_place==1
                for i in range(len(swimmers_results_in_swim)-1):
                    assert swimmers_results_in_swim[i+1].swim_place==swimmers_results_in_swim[i].swim_place+1
                    assert swimmers_results_in_swim[i+1].result_time>=swimmers_results_in_swim[i].result_time
                #Проверить что дорожки уникальны в рамках заплыва
                lanes_set=set()
                for i in range(len(swimmers_results_in_swim)):
                    lanes_set.add(swimmers_results_in_swim[i].lane)
                assert len(lanes_set)==len(swimmers_results_in_swim)
                
                swimmers_results_in_cur_phase+=swimmers_results_in_swim
            swimmers_results_in_cur_phase=sorted(swimmers_results_in_cur_phase,key=lambda x:x.phase_place)
            min_phase_place=1
            min_swim_place=1
            min_res_time=10
            #Проверить что все времена больше минимальных значений
            for swimmer_res in swimmers_results_in_cur_phase:
                assert swimmer_res.phase_place>=min_phase_place
                assert swimmer_res.swim_place>=min_swim_place
                assert swimmer_res.result_time>=min_res_time
                
            #Проверить что места в фазе последовательны, начинаются с 1 и время отсортировано вместе с ними
            assert swimmers_results_in_cur_phase[0].phase_place==1
            for ind in range(len(swimmers_results_in_cur_phase)-1):
                assert swimmers_results_in_cur_phase[ind+1].result_time>=swimmers_results_in_cur_phase[ind].result_time
                assert swimmers_results_in_cur_phase[ind+1].phase_place==swimmers_results_in_cur_phase[ind].phase_place+1
            #Проверить что дорожки находятся внутри допустимого диапазона (>=0 и <=9)
            for ind in range(len(swimmers_results_in_cur_phase)-1):
                assert swimmers_results_in_cur_phase[ind+1].lane>=0
                assert swimmers_results_in_cur_phase[ind+1].lane<=9
            from_place_in_phase_to_lane_ind=(4, 5, 3, 6, 2, 7, 1, 8, 0, 9)
            if cur_phase=="Heats":
                cur_phase="Semifinals"
                new_swims_array=[swim for swim in swims_array if swim.phase == "Semifinals"]
                for ind,swimmer in enumerate(swimmers_results_in_cur_phase):
                    if ind>15: #Уже набрали 16 пловцов
                        break
                    seeding_in_swim=ind//2
                    new_lane=from_place_in_phase_to_lane_ind[seeding_in_swim]
                    swim_ind=(ind+1)%2
                    new_swims_array[swim_ind].swimmers_arr[new_lane]=swimmer.name
            elif cur_phase=="Semifinals":
                cur_phase="Finals"
                new_swims_array=[swim for swim in swims_array if swim.phase == "Finals"]
                for ind,swimmer in enumerate(swimmers_results_in_cur_phase):
                    if ind>7: #Уже набрали 8 пловцов
                        break
                    seeding_in_swim=ind
                    new_lane=from_place_in_phase_to_lane_ind[seeding_in_swim]
                    new_swims_array[0].swimmers_arr[new_lane]=swimmer.name
            elif cur_phase=="Finals":
                cur_phase=""
                new_swims_array=[]
            cur_swims_arr=new_swims_array
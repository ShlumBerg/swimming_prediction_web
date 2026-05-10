from PyQt6.QtCore import QObject, pyqtSignal, QThread
import requests, csv, os, sqlite3, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import pandas as pd
import numpy as np




class Competition:
    def __init__(self,id):
        self.id=id
        pass

class Discipline:
    def __init__(self,discipline_id,competition_name,host_country_code,host_city,region_name,pool_configuration):
        self.id=discipline_id
        self.competition_name=competition_name
        self.host_country_code=host_country_code
        self.host_city=host_city
        self.region_name=region_name
        self.pool_configuration=pool_configuration
        pass


#
#ThreadParseCompetitions
#
class ThreadParseCompetitions(QThread):
    status_signal=pyqtSignal(str)
    error_signal=pyqtSignal(str)
    competitions_list_signal=pyqtSignal(list)  #Сигнал, передающий список id соревнований
    
    def __init__(self, ):
        super().__init__()
        self.is_running=True
    
    def run(self):
        tourn_list=[]
        try:
            #Получаем число элементов
            response=requests.get("https://api.worldaquatics.com/fina/competitions",params={"page_size":1,
                                            "venueDateFrom":"1900-01-01T00:00:00+00:00",
                                            "disciplines":"SW",
                                            #"group":"FINA"
                                            },timeout=15)
            n_elems=0
            if response.status_code!=200:
                raise ConnectionError(f"Ошибка при подключении к https://api.worldaquatics.com/fina/competitions. {response.status_code}")
            n_elems=response.json()['pageInfo']['numEntries']
            
            n_passed_elems=0
            cur_page=-1
            while n_passed_elems<n_elems and self.is_running:
                n_passed_elems+=10
                cur_page+=1
                response=requests.get("https://api.worldaquatics.com/fina/competitions",params={"page_size":100,
                                            "venueDateFrom":"1900-01-01T00:00:00+00:00",
                                            "disciplines":"SW",
                                            #"group":"FINA",
                                            
                                            "sort":"dateFrom,desc",
                                            "page":cur_page},timeout=15)
                if response.status_code!=200:
                    self.error_signal.emit(f"Ошибка при подключении к https://api.worldaquatics.com/fina/competitions: {response.status_code}")
                else:
                    tourn_as_resp=response.json()['content']
                    for tourn in tourn_as_resp:
                        tourn_list.append(Competition(tourn['id']))
        except Exception as e:
            self.error_signal.emit(f"Произошла ошибка: {e}")
        
        
        if self.is_running:
            self.competitions_list_signal.emit(tourn_list)
            
        
    def stop(self):
        self.is_running=False
        self.wait()
        

#
#ThreadParseCompetition
#
class ThreadParseCompetition(QThread):
    status_signal=pyqtSignal(str)
    error_signal=pyqtSignal(str)
    disciplines_list_signal=pyqtSignal(list)  #Сигнал, передающий список id дисциплин
    
    def __init__(self, competitions_list):
        super().__init__()
        self.competitions_list=competitions_list
        self.is_running=True
        
    def run(self):
        disciplines_list=[]
        ind=1
        for comp in self.competitions_list:
            competition_id=comp.id
            try:
                if not self.is_running:
                    break
                self.status_signal.emit(f"Идет парсинг {ind} соревнования из {len(self.competitions_list)}"); ind+=1
                response=requests.get(f"https://api.worldaquatics.com/fina/competitions/{competition_id}/events",timeout=15)
                if response.status_code!=200:
                    raise Exception(f"Ошибка при подключении к https://api.worldaquatics.com/fina/competitions/{competition_id}: {response.status_code}")
                else:
                    tourn_json_obj=response.json()
                    sports_list=tourn_json_obj["Sports"]
                    city=tourn_json_obj.get("City",None)
                    host_country_code=tourn_json_obj.get("CountryCode",None)
                    pool_length=tourn_json_obj.get("PoolConfiguration",None)
                    region_name=tourn_json_obj.get("RegionName",None)
                    tourn_name=tourn_json_obj.get("OfficialName",None)
                    for i in sports_list:
                        if i["Code"]=="SW":
                            for j in i["DisciplineList"]:
                                disciplines_list.append(Discipline(j["Id"],tourn_name,host_country_code,city,region_name,pool_length))
            except Exception as e:
                self.error_signal.emit(f"Произошла ошибка: {e}")
        if self.is_running:
            self.disciplines_list_signal.emit(disciplines_list)
            
        
    def stop(self):
        self.is_running=False
        self.wait()
        

#
#ThreadParseDiscipline
#
class ThreadParseDiscipline(QThread):
    status_signal=pyqtSignal(str)
    error_signal=pyqtSignal(str)
    parsing_over_signal=pyqtSignal(bool)  #Сигнал, передающий, что парсинг закончился
    
    def __init__(self, disciplines_list:Discipline,folder):
        super().__init__()
        self.disciplines_list=disciplines_list
        self.is_running=True
        self.folder=folder
        self.raw_csv_path=os.path.join(folder,"raw_dataset.txt")
        self.fieldnames=["competition_name","host_country_code","host_city","host_region",
                         "pool_configuration","discipline_name","phase_name",
                         "race_number_in_phase", "races_in_phase","race_date_local", "race_time_local",
                         "swimmer_country_code","swimmer_full_name","swimmer_age_at_swim_start","swimmer_id","swimmer_lane",
                         "swimmer_date_of_birth","swimmer_weight","swimmer_height","result_time","heat_rank"]
        self.swimmers_cache={}
        self.swimmers_cache_lock=Lock()
        self.csv_file_lock=Lock()
        with open(self.raw_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
        self.db_path = os.path.join(folder,'swimmers_db.sqlite')
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS swimmers (
                    id           TEXT PRIMARY KEY,
                    full_name TEXT,
                    dob          TEXT,
                    height       REAL,
                    sex          INTEGER,
                    country_code TEXT
            )
        """)
        

    def get_swimmer_dob_weight_height(self,swimmer_id,discipline_name):
        if swimmer_id==None:
            return None,None,None
        with self.swimmers_cache_lock:
            if swimmer_id in self.swimmers_cache:
                return self.swimmers_cache[swimmer_id]
        
        response_swimmer=requests.get(f"https://api.worldaquatics.com/fina/athletes/{swimmer_id}/bio",timeout=15) #Получить сведения о пловце
        if response_swimmer.status_code!=200:
            with self.swimmers_cache_lock:
                self.swimmers_cache[swimmer_id]=None,None,None
            return None,None,None
        else:
            swimmer_data=response_swimmer.json()[0].get("CoreData",None)
            swimmer_dob=None
            swimmer_weight=None
            swimmer_height=None
            swimmer_country_code=None
            swimmer_sex=1
            swimmer_given_name=""
            swimmer_family_name=""
            if discipline_name.split()[0]=='Men\'s':
                swimmer_sex=0
            if swimmer_data!=None:
                swimmer_dob=swimmer_data.get("DateOfBirth",None)
                swimmer_weight=swimmer_data.get("Weight",None)
                swimmer_height=swimmer_data.get("Height",None)
                swimmer_country_code=swimmer_data.get("CountryCode",None)
                swimmer_given_name=swimmer_data.get("PreferredGivenName","")
                swimmer_family_name=swimmer_data.get("PreferredFamilyName","")
            #Сохраняем в кэш
            with self.swimmers_cache_lock:
                self.swimmers_cache[swimmer_id]=swimmer_dob,swimmer_weight,swimmer_height
            swimmer_dob_1=None
            #Сохранить в sqlite файл
            try:
                if swimmer_dob is not None:
                    swimmer_dob_1=swimmer_dob.split("T")[0]
                with sqlite3.connect(self.db_path) as conn:
                    conn.execute("""
                        INSERT OR IGNORE INTO swimmers (id, full_name, dob, height, sex, country_code)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (swimmer_id,swimmer_family_name+" "+swimmer_given_name, swimmer_dob_1, swimmer_height, swimmer_sex, swimmer_country_code))
            except Exception as e:
                self.error_signal.emit(f"Ошибка записи в БД для пловца {swimmer_id}: {e}")
            
            
            #Возвращаем дату рождения и пол
            return swimmer_dob,swimmer_weight,swimmer_height
    
    def _parse_and_save(self,discipline):
        discipline_id=discipline.id
        competition_name=discipline.competition_name
        host_country_code=discipline.host_country_code
        host_city=discipline.host_city
        region_name=discipline.region_name
        pool_configuration=discipline.pool_configuration
        if not self.is_running:
            return
        try:
            response=requests.get(f"https://api.worldaquatics.com/fina/events/{discipline_id}",timeout=15)
            if response.status_code!=200:
                raise Exception(f"Ошибка при подключении к https://api.worldaquatics.com/fina/events/{discipline_id}: {response.status_code}")
            json_obj=response.json()
            disc_name=json_obj["DisciplineName"]
            rows=[]
            if "Relay" in disc_name:  #Эстафеты пропускаем
                return
            else:
                phases_stages_count={}
                for swim in json_obj["Heats"]:
                    if not self.is_running:
                        return
                    swim_date=swim.get("Date",None)
                    swim_time=swim.get("Time",None)
                    phase=swim.get("PhaseName",None)
                    
                    swim_number_in_phase=swim.get("UnitCode",None)
                    disc_name
                    pool_configuration
                    if "IsSummary" in swim and swim["IsSummary"]: #Не отдельный заплыв, а агрегация нескольких заплывов - пропускаем
                        continue
                    if phase in phases_stages_count:
                        phases_stages_count[phase]+=1
                    else:
                        phases_stages_count[phase]=1
                    for swimmer in swim["Results"]:
                        if not self.is_running:
                            return
                        try:
                            lane=swimmer.get("Lane",None)
                            result_time=swimmer.get("Time",None)
                            full_name=swimmer.get("FullName",None)
                            swimmer_country=swimmer.get("NAT",None)
                            swimmer_age=swimmer.get("AthleteResultAge",None)
                            swimmer_id=swimmer.get("PersonId",None)
                            heat_rank=swimmer.get("HeatRank",None)
                            swimmer_dob,swimmer_weight,swimmer_height=self.get_swimmer_dob_weight_height(swimmer_id,disc_name)
                            #Добавляем ряд
                            row={"competition_name":competition_name,"host_country_code":host_country_code,"host_city":host_city,"host_region":region_name,
                                    "pool_configuration":pool_configuration,"discipline_name":disc_name, "phase_name":phase, "race_number_in_phase":swim_number_in_phase,
                                    "race_date_local":swim_date,"race_time_local":swim_time,"swimmer_country_code":swimmer_country, "swimmer_full_name":full_name,
                                    "swimmer_age_at_swim_start":swimmer_age,"swimmer_id":swimmer_id,"swimmer_lane":lane,"swimmer_date_of_birth":swimmer_dob,
                                    "swimmer_weight":swimmer_weight,"swimmer_height":swimmer_height,
                                    "result_time":result_time,"heat_rank":heat_rank}
                            rows.append(row)
                        except Exception as ex:
                            self.error_signal.emit(f"Произошла ошибка при сохранении сведений заплыва пловца с id {swimmer_id}! Ошибка: {ex}")
            for i in range(len(rows)):
                rows[i]["races_in_phase"]=phases_stages_count[rows[i]["phase_name"]]
            with self.csv_file_lock:
                    with open(self.raw_csv_path, "a", newline="", encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                        writer.writerows(rows)
        except Exception as e:
            self.error_signal.emit(f"Произошла ошибка: {e}")

    def run(self):
            ind=0
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures={executor.submit(self._parse_and_save,discipline)
                for discipline in self.disciplines_list}
                for future in as_completed(futures):
                    if not self.is_running:
                        break
                    ind+=1
                    self.status_signal.emit(f"Было пропаршено {ind} дисциплин из {len(self.disciplines_list)} найденных")
            
            if self.is_running:
                self.parsing_over_signal.emit(True)
                
        
    def stop(self):
        self.is_running=False
        self.wait()





#
#Главная модель (QObject)
#
class ScrappingModuleModel(QObject):
    error_signal    = pyqtSignal(str)
    status_signal   = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.folder=""
        self.races_count=0
        
        self.thread_parse_competitions=None
        self.thread_parse_competition=None
        self.thread_parse_discipline=None
        

    def start_scrapping(self, folder: str):
        '''Запуск процесса парсинга'''
        self.folder=folder
        self.status_signal.emit("Идет поиск соренований...")
        
        self.thread_parse_competitions=ThreadParseCompetitions()
        self.thread_parse_competitions.finished.connect(lambda: setattr(self, "thread_parse_competitions", None))
        
        self.thread_parse_competitions.error_signal.connect(self.error_signal.emit)
        self.thread_parse_competitions.status_signal.connect(self.status_signal.emit)
        self.thread_parse_competitions.competitions_list_signal.connect(self._on_competitions_list_formed)
        
        self.thread_parse_competitions.start()
        
    def _on_competitions_list_formed(self, competitions:list):
        '''Нашли турниры, ищем соревнования по дисциплинам'''
        self.status_signal.emit(f"Было найдено {len(competitions)} соревнований")
        self.status_signal.emit("Идет поиск дисциплин в рамках соревнований...")
        
        self.thread_parse_competition=ThreadParseCompetition(competitions)
        self.thread_parse_competition.finished.connect(lambda: setattr(self, "thread_parse_competition", None))
        
        self.thread_parse_competition.error_signal.connect(self.error_signal.emit)
        self.thread_parse_competition.status_signal.connect(self.status_signal.emit)
        self.thread_parse_competition.disciplines_list_signal.connect(self._on_disciplines_found)
        
        self.thread_parse_competition.start()
        
    def _on_disciplines_found(self,disciplines:list):
        '''Нашли дисциплины'''
        self.status_signal.emit(f"Было найдено {len(disciplines)} дисциплин в рамках соревнований")
        self.status_signal.emit("Начинается формирование датасета...")
        
        self.thread_parse_discipline=ThreadParseDiscipline(disciplines,self.folder)
        self.thread_parse_discipline.finished.connect(lambda: setattr(self, "thread_parse_discipline", None))
        
        self.thread_parse_discipline.error_signal.connect(self.error_signal.emit)
        self.thread_parse_discipline.status_signal.connect(self.status_signal.emit)
        self.thread_parse_discipline.parsing_over_signal.connect(self._on_parsing_over)
        
        self.thread_parse_discipline.start()
        
    def _on_parsing_over(self):
        '''Парсинг закончился'''
        self.finished_signal.emit(True)
        
    def cancel_scrapping(self):
        '''Остановка всех потоков'''
        threads = [
        self.thread_parse_competitions,
        self.thread_parse_competition,
        self.thread_parse_discipline
        ]
        for thread in threads:
            try:
                if thread and thread.isRunning():
                    thread.stop()
            except RuntimeError: #Поток и так уже удален
                pass
        self.finished_signal.emit(False)

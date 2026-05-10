from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from numpy.lib.stride_tricks import sliding_window_view
import numpy as np




#Класс для нормализации входных признаков и переделки их в формат, подходящий на вход к BiLSTM
class SequenceStandardScalerForBiLSTM(BaseEstimator, TransformerMixin):
    def __init__(self,
                 window_size=5,                           #Размер окна для последовательности
                 ):
        self.window_size = window_size                
        self.is_train_data_transformed=False             #Флаг, показывает, были ли преобразованы тренировочные данные через transform
        
    #Вернуть только те колонки датафрейма, которые не являются строками или объектами
    def _get_required_columns_from_dataset(self, X):
        return X.select_dtypes(include='number').columns.tolist()

    def fit(self, X, y=None):
        #Обучаем StandardScaler для признаков на тренировочном датасете
        self.feature_cols = self._get_required_columns_from_dataset(X)
        self.scaler_ = StandardScaler().fit(X[self.feature_cols])     
        self.is_train_data_transformed = False

        return self

    def transform(self, X):
        if not self.is_train_data_transformed:  #На train данных
            X_scaled = X.copy()
        
            #Получить углы дня года и времени в секундах дня - для сортировки записей в хронологическом порядке
            X_scaled['_doy_angle'] = np.arctan2(X['race_doy_sin'], X['race_doy_cos']) % (2 * np.pi)
            X_scaled['_time_angle'] = np.arctan2(X['race_time_seconds_sin'], X['race_time_seconds_cos']) % (2 * np.pi)
            
            #Преобразуем значения внутри датафрейма согласно StandardScaler
            X_scaled[self.feature_cols] = self.scaler_.transform(X[self.feature_cols])
            
            X_scaled['_original_idx'] = np.arange(len(X))
            
            #Сортируем датафрейм сначала по ИД пловца, затем по году заплыва, затем по углу дня года, затем по углу времени дня
            X_scaled = X_scaled.sort_values(by=['swimmer_id', 'race_year', '_doy_angle', '_time_angle'])
            
            #Есть проблема, что не у всех строк в датасете было время (оно было импутировано для некоторых значений).
            #Однако дата есть у всех строк. В целом же погрешность времени в течении дня не должно сильно влиять на производительность модели
            
            
            #Выходной 3D массив на вход к модели
            sequences = np.zeros((len(X), self.window_size, len(self.feature_cols)), dtype=np.float32)
            
            #Получаем последовательности для обучения BiLSTM и сохраняем 
            self.swimmer_history = {}            
            for swimmer_id, group in X_scaled.groupby('swimmer_id', sort=False):
                X_for_1_swimmer = group[self.feature_cols].values.astype(np.float32)                      #Отсортированный массив результатов одного пловца
                paddings=np.full((self.window_size-1, len(self.feature_cols)), -999.0, dtype=np.float32)  #(windows_size-1,n_features)
                swimmer_history_sequence=np.vstack([paddings,X_for_1_swimmer])                             #(len(X_for_1_swimmer)+windows_size-1,n_features) 
                original_indices = group['_original_idx'].values                              
                
                windows = sliding_window_view(swimmer_history_sequence, window_shape=self.window_size, axis=0) #(len(X_for_1_swimmer),n_features,windows_size)
                
                #Переставить местами два измерения массива, так как BiLSTM ожидает массив размерности (batch,timesteps,n_features)
                windows = np.swapaxes(windows, 1, 2) #(len(X_for_1_swimmer),windows_size,n_features)
                
                #Присваиваем результирующие последовательности для обучения BiLSTM внутрь выходного 3Д массива
                sequences[original_indices] = windows 
                
                self.swimmer_history[swimmer_id] = X_for_1_swimmer[-(self.window_size - 1):]      #Сохраняем последние записи пловца в историю
                
            self.is_train_data_transformed=True
            return sequences
        else:   #На test/validation данных
            X_scaled = X.copy()
        
            #Получить углы дня года и времени в секундах дня - для сортировки записей в хронологическом порядке
            X_scaled['_doy_angle'] = np.arctan2(X['race_doy_sin'], X['race_doy_cos']) % (2 * np.pi)
            X_scaled['_time_angle'] = np.arctan2(X['race_time_seconds_sin'], X['race_time_seconds_cos']) % (2 * np.pi)
            
            #Преобразуем значения внутри датафрейма согласно StandardScaler
            X_scaled[self.feature_cols] = self.scaler_.transform(X[self.feature_cols])
            
            X_scaled['_original_idx'] = np.arange(len(X)) 
            
            #Сортируем датафрейм сначала по ИД пловца, затем по году заплыва, затем по углу дня года, затем по углу времени дня
            X_scaled = X_scaled.sort_values(by=['swimmer_id', 'race_year', '_doy_angle', '_time_angle'])
                                   
            #Выходной 3D массив на вход к модели
            sequences = np.zeros((len(X), self.window_size, len(self.feature_cols)), dtype=np.float32)
            
            #Получаем последовательности для обучения BiLSTM и сохраняем             
            for swimmer_id, group in X_scaled.groupby('swimmer_id', sort=False):
                X_for_1_swimmer = group[self.feature_cols].values.astype(np.float32)                      #Отсортированный массив результатов одного пловца
                
                #Пытаемся получить историю пловца
                history = self.swimmer_history.get(
                    swimmer_id,
                    np.zeros((0, len(self.feature_cols)), dtype=np.float32)
                )
                
                padding_size=max(0,self.window_size-1-len(history))  #Размер паддинга слева значениями -999
                
                #Строим массив последовательностей
                swimmer_sequences=None
                if padding_size>0:
                    paddings=np.full((padding_size, len(self.feature_cols)), -999.0, dtype=np.float32)   #(padding_size,n_features)
                    swimmer_sequences=np.vstack([paddings,history,X_for_1_swimmer])                     #(len(X_for_1_swimmer)+windows_size-1,n_features)
                else:
                    swimmer_sequences=np.vstack([history,X_for_1_swimmer])                     #(len(X_for_1_swimmer)+windows_size-1,n_features)
                original_indices = group['_original_idx'].values                              
                
                windows = sliding_window_view(swimmer_sequences, window_shape=self.window_size, axis=0) #(len(X_for_1_swimmer),n_features,windows_size)
                
                #Переставить местами два измерения массива, так как BiLSTM ожидает массив размерности (batch,timesteps,n_features)
                windows = np.swapaxes(windows, 1, 2) #(len(X_for_1_swimmer),windows_size,n_features)
                
                #Присваиваем результирующие последовательности для обучения BiLSTM внутрь выходного 3Д массива
                sequences[original_indices] = windows               
                
            return sequences
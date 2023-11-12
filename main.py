from enum import Enum
from fastapi import FastAPI, HTTPException, Query, Path, Body
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime


app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"



class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog'),
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

# 1. Реализация пути "/"
@app.get('/')
def root():
    """
    Корневой маршрут, который приветствует пользователя.
    """
    return {"message": "Welcome to the Dog Information Service"}

# 2. Реализация пути "/post"
@app.post('/post', response_model=Timestamp)
def create_post(dog_id: int):
    """
    Создает новую запись о времени для собаки с заданным идентификатором.
    :param dog_id: Идентификатор собаки, для которой создается запись времени.
    :return: Объект Timestamp с идентификатором и временной меткой.
    """
    timestamp = int(datetime.timestamp(datetime.now()))
    post = Timestamp(id=dog_id, timestamp=timestamp)
    post_db.append(post)
    return post


# 3. Реализация пути "/dog" для создания собаки
@app.post('/dog', response_model=Dog)
def create_dog(dog: Dog):
    """
    Создает новую запись о собаке.
    :param dog: Данные о новой собаке.
    :return: Объект Dog с идентификатором, присвоенным при создании.
    """
    new_dog_id = max(dogs_db.keys()) + 1
    dogs_db[new_dog_id] = dog
    return dog
    
# 4. Реализация пути "/dog" для получения списка собак
@app.get('/dog')
def get_dogs(kind: DogType = Query(None, description='Порода собаки',required=False)):
    """
    Получает список всех собак в базе данных или списка собак определенного типа.
    :param kind: Тип собаки (опциональный параметр).
    :return: Список собак (с объектами Dog).
    """
    if kind:
        filtered_dogs = [dog for dog in dogs_db.values() if dog.kind == kind]
        return filtered_dogs
    else:
        return list(dogs_db.values())


# 5. Реализация пути "/dog/{pk}" для получения собаки по ID
@app.get('/dog/{pk}', response_model=Dog)
def get_dog_by_pk(pk: int):
    """
    Получает информацию о собаке по её идентификатору.
    :param dog_id: Идентификатор собаки.
    :return: Объект Dog с данными о собаке или сообщение об ошибке, если собака не найдена.
    """

    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dogs_db[pk]


# 6. Реализация пути "/dog/{pk}" для обновления собаки по ID
@app.patch('/dog/{pk}', response_model=Dog)
def update_dog(pk: int, updated_dog: Dog):
    """
    Обновляет информацию о собаке с заданным идентификатором.
    :param dog_id: Идентификатор собаки, которую необходимо обновить.
    :param updated_dog: Обновленные данные о собаке.
    :return: Обновленный объект Dog или сообщение об ошибке, если собака не найдена.
    """
   
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="Dog not found")
    
   
    current_dog = dogs_db[pk]
    updated_data = updated_dog.dict(exclude_unset=True)
    updated_dog = current_dog.copy(update=updated_data)
    dogs_db[pk] = updated_dog
    return updated_dog

    
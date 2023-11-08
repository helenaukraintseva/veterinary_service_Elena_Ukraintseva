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
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def read_root():
    """
    Корневой маршрут, который приветствует пользователя.
    """
    return {"message": "Welcome to the Dog Information Service"}


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

@app.post('/dogs', response_model=Dog)
def create_dog(dog: Dog):
    """
    Создает новую запись о собаке.
    :param dog: Данные о новой собаке.
    :return: Объект Dog с идентификатором, присвоенным при создании.
    """
    new_dog_id = max(dogs_db.keys()) + 1
    dogs_db[new_dog_id] = dog
    return dog

@app.get('/dogs', response_model=list[Dog])
def get_dogs():
    """
    Получает список всех собак в базе данных.
    :return: Список собак (с объектами Dog).
    """
    return list(dogs_db.values())

@app.get('/dogs/{dog_id}', response_model=Dog)
def get_dog_by_id(dog_id: int):
    """
    Получает информацию о собаке по её идентификатору.
    :param dog_id: Идентификатор собаки.
    :return: Объект Dog с данными о собаке или сообщение об ошибке, если собака не найдена.
    """
    if dog_id in dogs_db:
        return dogs_db[dog_id]
    return {"error": "Dog not found"}

@app.get('/dogs/type/{dog_type}', response_model=list[Dog])
def get_dogs_by_type(dog_type: DogType):
    """
    Получает список собак определенного типа.
    :param dog_type: Тип собаки (DogType).
    :return: Список собак данного типа (с объектами Dog).
    """
    matching_dogs = [dog for dog in dogs_db.values() if dog.kind == dog_type]
    return matching_dogs

@app.put('/dogs/{dog_id}', response_model=Dog)
def update_dog_by_id(dog_id: int, updated_dog: Dog):
    """
    Обновляет информацию о собаке с заданным идентификатором.
    :param dog_id: Идентификатор собаки, которую необходимо обновить.
    :param updated_dog: Обновленные данные о собаке.
    :return: Обновленный объект Dog или сообщение об ошибке, если собака не найдена.
    """
    if dog_id in dogs_db:
        dogs_db[dog_id] = updated_dog
        return updated_dog
    return {"error": "Dog not found"}
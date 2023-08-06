# PyModelManager
PyModelManager это Python библиотека для взаимодействия с ModelManager API.

## Установка

```bash
$ pip install PyModelManager
```

## Пример использования

```python
from modelmanager import ModelManager

# Сначала создаем экземпляр ModelManager
mm = ModelManager(base_url='http://{hostname}/api', login='{login}', password='{password}')

# Получим список проектов
projects = mm.get_projects()

# Получим все существующие версии моделей всех проектов
models = [project.get_models() for project in projects]

# Выводим в stdout все модели
for model in models:
    print(model)

# Получим реестр признаков
registry = mm.get_feature_registry()

# Получим список всех признаков
features = registry.get_features()

# Выводим в stdout все признаки
for feature in features:
    print('Feature: %s, %s' % (feature.name, feature.description))
    
# Созданим в реестре новый признак
feature = registry.create_feature('birthday', "Дата рождения в формате 'yyyy-mm-dd'")
```

## Документация

TBD
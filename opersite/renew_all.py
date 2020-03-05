from renew_baseorders import renew_baseorders_worker
from renew_baseworkplan import renew_baseworkplan_worker
from renew_basedocumentations import renew_basedocumentations_worker
from renew_basedocumentations_fact import renew_basedocumentations_fact_worker

if __name__ == "__main__":
    print('Обновление служебных записок')
    renew_baseorders_worker()

    print('Обновление дат Плана Производства')
    renew_baseworkplan_worker()

    print('Обновление дат документации по планам')
    renew_basedocumentations_worker()

    print('Обновление дат документации по фактам')
    renew_basedocumentations_fact_worker()
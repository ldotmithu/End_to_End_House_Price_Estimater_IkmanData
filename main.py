from house_project.Pipeline.Stages_of_pipeline import (DataIngestionPipeline,DataValidationPipeline,
                                                       DataTransformPipeline,ModelTrainerPipeline,ModelEvaluationPipeline)
from house_project import logging

try:
    logging.info(">>>>>>>Data Ingestion>>>>>>>")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.Main()
    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
except Exception as e:
    #logging.exception(e)
    raise e 


try:
    logging.info(">>>>>>>Data Validation>>>>>>>")
    data_validaion = DataValidationPipeline()
    data_validaion.Main()
    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
except Exception as e:
    #logging.exception(e)
    raise e 


try:
    logging.info(">>>>>>>Data Transform>>>>>>>")
    data_transform = DataTransformPipeline()
    data_transform.Main()
    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
except Exception as e:
    #logging.exception(e)
    raise e 

try:
    logging.info(">>>>>>>Model Tranier >>>>>>>")
    model_trainer = ModelTrainerPipeline()
    model_trainer.Main()
    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
except Exception as e:
    #logging.exception(e)
    raise e 

try:
    logging.info(">>>>>>>Model Tranier >>>>>>>")
    model_evaluation = ModelEvaluationPipeline()
    model_evaluation.Main()
    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
except Exception as e:
    #logging.exception(e)
    raise e 
import pickle 
import pandas as pd
import logging

logging.basicConfig(level=logging.ERROR, filemode='w', filename='error_log.log', format='%(asctime)s - %(levelname)s - %(message)s')


def predictor(predict_data):
    normailzed = pd.json_normalize(predict_data)
    model_arr = pickle.load(open('car_insurance_model.pkl', 'rb'))

    prediction_model = model_arr[0]
    occupation_le = model_arr[1]
    car_use_le = model_arr[2]
    car_type_le = model_arr[3]
    revoked_le = model_arr[4]

    try:
        normailzed['OCCUPATION'] = occupation_le.transform(normailzed['OCCUPATION'])
        normailzed['CAR_USE'] = car_use_le.transform(normailzed['CAR_USE'])
        normailzed['CAR_TYPE'] = car_type_le.transform(normailzed['CAR_TYPE'])
        normailzed['REVOKED'] = revoked_le.transform(normailzed['REVOKED'])
    except AttributeError:
        logging.error("The above Encoder either don't have the property which used or there is a spelling error in calling that property.")
        return 2
    except NameError:
        logging.error("The variable or the function called is not either defined or there in spell error in calling the function.")
        return 2
    except KeyError:
        logging.error("The key used to access the data in dataframe is either not present in the dataset or it is spelled incorrectly.")
        return 2
    
    try:
        result = prediction_model.predict(normailzed)
    except AttributeError:
        logging.error("The model either don't have the attribute predict or is mispelled.")
        return 2
    
    return result[0]
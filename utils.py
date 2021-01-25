# dependencies
import numpy  as np
import pandas as pd
from   sklearn.impute          import SimpleImputer
from   sklearn.preprocessing   import OneHotEncoder, StandardScaler
from   sklearn.model_selection import GridSearchCV
from   sklearn.ensemble        import RandomForestClassifier
from   sklearn.tree            import DecisionTreeClassifier
from   sklearn.metrics         import make_scorer, f1_score

# funciones
# fe variables numericas
def feature_engineer_numeric(dataframe, columnas_numericas):
    df = dataframe.copy()
    # imputación
    imputador_numeric   = SimpleImputer(missing_values = np.nan, strategy = 'mean').fit(df[columnas_numericas])
    df_imputed = imputador_numeric.transform(df[columnas_numericas])    
    # estandarización
    estandarizador = StandardScaler().fit(df_imputed)
    df_standarizado = estandarizador.transform(df_imputed)
    # add names
    df_nombres = pd.DataFrame(df_standarizado, columns = columnas_numericas).reset_index(drop = True)
    df_salida  = pd.concat([df_nombres, dataframe.drop(columns = columnas_numericas)], axis = 1)
    #
    return df_salida
# fe variables categoricas
def feature_engineer_categoric(dataframe, columnas_categoricas):
    df = dataframe.copy()
    # imputacion
    imputador_categoric = SimpleImputer(missing_values = None, strategy = 'most_frequent').fit(df[columnas_categoricas])
    df_imputed = imputador_categoric.transform(df[columnas_categoricas])
    # ohe
    encoder = OneHotEncoder(handle_unknown = 'ignore', sparse = False).fit(df_imputed)
    df_ohe = encoder.transform(df_imputed)
    # add names
    columnas_nombres = encoder.get_feature_names()
    df_nombres = pd.DataFrame(df_ohe, columns = columnas_nombres).reset_index(drop = True)
    # gather results
    df_salida = pd.concat([dataframe.drop(columns = columnas_categoricas), df_nombres], axis = 1)
    #
    return df_salida
# junto ambas
def feature_engineer(dataframe, columnas_numericas, columnas_categoricas):
    df_numeric   = feature_engineer_numeric(dataframe,    columnas_numericas)
    df_categoric = feature_engineer_categoric(df_numeric, columnas_categoricas)
    # salida
    return df_categoric
# preparación de la variable objetivo
def ohe_objetivo(dataframe):
    df = dataframe.copy()
    # 
    encoder = OneHotEncoder(handle_unknown = 'error', sparse = False).fit(df)
    df_ohe  = encoder.transform(df)
    # format
    columnas_nombres = encoder.get_feature_names()
    df_nombres       = pd.DataFrame(df_ohe, columns = columnas_nombres).reset_index(drop = True)
    # salida
    return df_nombres, encoder


# feature engineer for new examples, with any number of missing values
# numeric
def feature_engineer_numeric_new_data(dataframe_parcial, dataframe_completo, columnas_numericas):
    df_completo = dataframe_completo.copy()
    df_parcial = dataframe_parcial.copy()
    ##  transformations
    # imputacion
    imputador_numeric = SimpleImputer(missing_values = np.nan, strategy = 'mean').fit(df_completo[columnas_numericas])
    df_imputed        = imputador_numeric.transform(df_parcial[columnas_numericas])
    # estandarizado
    estandarizador  = StandardScaler().fit(df_completo[columnas_numericas])
    df_standarizado = estandarizador.transform(df_imputed)
    # add names
    df_nombres = pd.DataFrame(df_standarizado, columns = columnas_numericas).reset_index(drop = True)
    df_salida  = pd.concat([df_nombres, df_parcial.drop(columns = columnas_numericas)], axis = 1)
    # 
    return df_salida
# ingenieria de variables para las variables categoricas de los ejemplos nuevos
def feature_engineer_categoric_new_data(dataframe_parcial, dataframe_completo, columnas_categoricas):
    df_completo = dataframe_completo.copy()
    df_parcial  = dataframe_parcial.copy()
    # imputacion
    imputador_categoric = SimpleImputer(missing_values = '', strategy = 'most_frequent').fit(df_completo[columnas_categoricas])
    df_imputed = imputador_categoric.transform(df_parcial[columnas_categoricas])
    # ohe
    encoder = OneHotEncoder(handle_unknown = 'ignore', sparse = False).fit(df_completo[columnas_categoricas])
    df_ohe = encoder.transform(df_imputed)
    # add names
    columnas_nombres = encoder.get_feature_names()
    df_nombres = pd.DataFrame(df_ohe, columns = columnas_nombres).reset_index(drop = True)
    # gather results
    df_salida = pd.concat([dataframe_parcial.drop(columns = columnas_categoricas), df_nombres], axis = 1)
    #
    return df_salida
# junto ambos pasos
def feature_engineer_new_data(dataframe_parcial, dataframe_completo, columnas_numericas, columnas_categoricas):
    df_completo = dataframe_completo.copy()
    df_parcial  = dataframe_parcial.copy()
    # magic
    df_numeric   = feature_engineer_numeric_new_data(df_parcial,   df_completo, columnas_numericas)
    df_categoric = feature_engineer_categoric_new_data(df_numeric, df_completo, columnas_categoricas)
    # 
    df_salida = df_categoric
    return df_salida


# prediction of new samples
# function to fill empty values in user examples
def complete_df(df_example):
    # helper df
    df_empty = pd.DataFrame([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, '', '', '', '']], columns = columnas_predictoras)
    # llenado
    df_salida = pd.concat([df_empty.drop(columns = df_ejemplo_raw.columns), df_ejemplo_raw], axis = 1)
    # 
    return df_salida
#  prediction function
# function to predict in human terms
def predict_phone(ejemplo, dataframe_entrenamiento, columnas_numericas, columnas_categoricas, modelo, encoder_objetivo, dataframe_completo):
    # transformación para la prediccion
    df_ejemplo_transformed = feature_engineer_new_data(ejemplo, dataframe_entrenamiento, columnas_numericas, columnas_categoricas)
    # predicción
    prediccion_cruda = modelo.predict(df_ejemplo_transformed)
    # formato más familiar
    prediction_human = encoder_objetivo.inverse_transform(prediccion_cruda)
    # agrupo todo en un dataframe
    df_salida = pd.DataFrame({'producto_nombre': prediction_human[0]}).merge(dataframe_completo, on = 'producto_nombre', how = 'inner')
    # 
    return df_salida
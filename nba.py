import numpy as np
import pandas as pd


def read_csv(filename):
    return pd.read_csv(filename, ';')


def new_patient(n):
    return np.random.randint(0, 2, n)


def dis_prob(new_patient, disease_probability, symptom_data):
    patient_disease_probs = np.ones(len(disease_probability))
    for i in range(len(disease_probability)):
        patient_disease_probs[i] *= disease_probability[i]
        for j in range(len(new_patient)):
            if new_patient[j] == 1:
                patient_disease_probs[i] *= symptom_data.iloc[j, i + 1]
                # print(symptom_data.iloc[j, i+1])
    return patient_disease_probs


if __name__ == '__main__':
    symptom_data = read_csv('symptom.csv')
    disease_data = read_csv('disease.csv')
    disease_probability = list(map(lambda x: x / disease_data['количество пациентов'][len(disease_data) - 1],
                                   disease_data['количество пациентов'][0:-1]))
    # print(disease_probability)
    new_patient = new_patient(symptom_data.shape[0])
    print(dis_prob(new_patient, disease_probability, symptom_data))
    print(np.argmax(dis_prob(new_patient, disease_probability, symptom_data)))
    print(disease_data.disease[np.argmax(dis_prob(new_patient, disease_probability, symptom_data))])
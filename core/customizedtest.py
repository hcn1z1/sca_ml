from .test import  full_ranks, rank , load_model , load_ascad, AES_Sbox
import numpy as np
from collections import Counter

class Evolution:
    def __init__(self,model,ascad_dataset,start_index:int,amount:int) -> None:
        print(model,ascad_dataset,start_index,amount)
        self.model = load_model(model)
        self.start_index = start_index
        self.amount = amount
        self.real_key = 0
        self.prediction = None
        self.x = []
        self.y = []
        self.expected_keys = []
        (X_profiling, Y_profiling), (self.X_attack, Y_attack), (Metadata_profiling, self.Metadata_attack) = load_ascad(ascad_dataset, load_metadata=True)

    def getPrediction(self):
        self.X_attack = self.X_attack[self.start_index:self.start_index+self.amount]
        self.Metadata_attack = self.Metadata_attack[self.start_index:self.start_index+self.amount]
        input_data = self.X_attack
        self.prediction = self.model.predict(input_data)
        self.real_key = self.Metadata_attack[0]["key"][2]
        return self.prediction
    
    def getRanks(self):
        max_trace_idx = min(self.start_index + self.amount, self.X_attack.shape[0])
        ranks = full_ranks(self.prediction, self.X_attack, self.Metadata_attack, 0, max_trace_idx, 10, 2 , 0)
        self.x = [ranks[i][0] for i in range(0, ranks.shape[0])]
        self.y = [ranks[i][1] for i in range(0, ranks.shape[0])]
        return self.x,self.y

    def start_custom_calculation(self):
        key_bytes_proba = []
        expected_keys = []
        for i in range(0,len(self.prediction) - 10,10):
            predictions = self.prediction[i:i+10]
            metadata = self.Metadata_attack[i:i+10]
            expected_key,key_bytes_proba = self.calculate_max(i,predictions,metadata,key_bytes_proba)
            expected_keys.append(expected_key) # [int]
        self.expected_keys = expected_keys # this line was added so the timer doesn't stop after adding only the first element to expected_keys

    def calculate_max(self,step,predictions,metadata,probabilities):
        if len(probabilities) == 0:
            probabilities = np.zeros(256)
        for p in range(0,len(predictions)):
            plain_text = metadata[p]['plaintext'][2]
            real_key = metadata[p]['key'][2]
            for i in range(0,256):
                proba = predictions[p][AES_Sbox[plain_text ^ i]]
                if proba != 0:
                    probabilities[i] += np.log(proba)
                else:
                    min_proba_predictions = predictions[p][np.array(predictions[p]) != 0]
                    min_proba = min(min_proba_predictions)
                    probabilities[i] += np.log(min_proba**2)
        return np.argmax(probabilities),probabilities

    def find_max_and_second_max(self):
        count = Counter(self.expected_keys)
        most_common_elements = count.most_common(2)
        max1 = most_common_elements[0][0] if len(most_common_elements) > 0 else None
        max2 = most_common_elements[1][0] if len(most_common_elements) > 1 else None
        return max1, max2
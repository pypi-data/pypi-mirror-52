import pickle
from Crypto.Cipher import AES
import requests
import random
import string
import base64
from sklearn.metrics import confusion_matrix, f1_score, precision_recall_fscore_support, accuracy_score, auc
from sklearn.metrics import precision_recall_curve, roc_curve, recall_score, precision_score, roc_auc_score
from sklearn.metrics import r2_score, mean_absolute_error, median_absolute_error,  mean_squared_error
import pandas as pd
import tabulate
import base64


def generate_auth_token(api_key):
    return {'key': api_key}


def list_all_models(token, host="beta.preflet.com", port='5000', print_=True):
    import json
    filter = json.dumps({'model': 0})
    if host == "localhost" or host == "127.0.0.1":
        url = "http://" + host + ":" + port + \
            "/api/v1/get/models?filter=" + filter
    else:
        url = "https://" + host + \
            "/api/v1/get/models?filter=" + filter
    r = requests.get(url)
    data = r.json()
    if not data['result']:
        raise Exception(data['data'])
    data = data["data"]
    header = ["Name", "Train Type", "Predicting", "Algorithm"]
    rows = [[x["id"], x["train_type"], x["predict"], x["algorithm"]]
            for x in data]
    if print_:
        print(tabulate.tabulate(rows, header))
    return data


def get_model(id, token, host="beta.preflet.com", port='5000'):
    if host == "localhost" or host == "127.0.0.1":
        url = "http://" + host + ":" + port + \
            "/api/v1/get_model/{}?api_key=".format(
                id) + token['key']
    else:
        url = "https://" + host + \
            "/api/v1/get_model/{}?api_key=".format(
                id) + token['key']
    r = requests.get(url)
    data = r.json()

    if data["result"] and data["data"]:
        model = base64.b64decode(data["data"]["model"])
        decrypted_model = pickle.loads(model)
        return decrypted_model, data["data"]
    return None, None


class Model:
    def __init__(self,
                 id,
                 model,
                 metadata={},
                 metrics={},
                 predict_var_mapping=None,
                 train_type='Classification',
                 feature_importance=None
                 ):
        self.id = id
        self.model = self.prepare_model(model)
        self.metrics = metrics
        self.metadata = metadata
        self.predict = self.get_predict_var()
        self.input_features = list(metadata.keys())
        if self.predict in self.input_features:
            self.input_features.remove(self.predict)
        self.predict_var_mapping = predict_var_mapping
        self.train_type = train_type
        self.algorithm = model.__class__.__name__
        self.feature_importance = feature_importance

    def prepare_model(self, model):
        pickled_model = pickle.dumps(model)

        key = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=32))
        iv = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=16))

        aes = AES.new(key.encode(), AES.MODE_CFB, iv.encode())
        encrypted_model = aes.encrypt(pickled_model)

        enc_data = {"id": self.id, "key": key, "iv": iv}

        self._enc_data = enc_data
        return base64.b64encode(encrypted_model).decode('UTF-8')

    def upload(self, auth_token, host="beta.preflet.com", port='5000'):
        if host == "localhost" or host == "127.0.0.1":
            url = "http://" + host + ":" + port + \
                "/api/v1/host_model?api_key=" + auth_token['key']
        else:
            url = "https://" + host + \
                "/api/v1/host_model?api_key=" + auth_token['key']
        if self.train_type == "Multi-Class":
            self.train_type = "Classification"
        r = requests.request('POST', url, json=self.__dict__)
        print(r.content)
        return self._upload_handler(r)

    def calculate_metrics(self, y_true, y_pred):
        if self.train_type == "Classification":
            metrics = self.measure_error_class(y_true, y_pred)
            self.metrics = metrics
            return metrics
        if self.train_type == "Regression":
            metrics = self.measure_error_reg(y_true, y_pred)
            self.metrics = metrics
            return metrics
        if self.train_type == "Multi-Class":
            metrics = self.measure_error_multiclass(y_true, y_pred)
            self.metrics = metrics
            return metrics

    def _upload_handler(self, r):
        res = r.json()
        if res["result"]:
            print("Upload Succesful.")
        else:
            raise Exception(res["data"])

    def measure_error_reg(self, y_true, y_pred):
        r2 = r2_score(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        mmdse = median_absolute_error(y_true, y_pred)

        matx = {
            'R Squared': round(r2, 2),
            'Mean Squared Error': round(mse, 2),
            'Root Mean Squared Error': round(rmse, 2),
            'Mean Absolute Error': round(mae, 2),
            'Median Squared Error': round(mse, 2)
        }
        return matx

    def measure_error_multiclass(self, y_true, y_pred):

        precision, recall, fscore, _ = precision_recall_fscore_support(
            y_true, y_pred, average='macro')
        f1_micro = f1_score(y_true, y_pred, average="micro")
        accuracy = accuracy_score(y_true, y_pred)
        error_rate = 1 - accuracy

        matx = {
            'Precision': round(precision, 2),
            'Recall': round(recall, 2),
            'Fscore': round(fscore, 2),
            'F1_micro': round(f1_micro, 2),
            'Accuracy': round(accuracy, 2),
            'ErrorRate': round(error_rate, 2),
        }

        return matx

    def measure_error_class(self, y_true, y_pred):
        precision, recall, fscore, _ = precision_recall_fscore_support(
            y_true, y_pred, average='weighted')
        accuracy = accuracy_score(y_true, y_pred)
        error_rate = 1 - accuracy
        fpr, tpr, th = roc_curve(y_true, y_pred)
        pr, rc, thr = precision_recall_curve(y_true, y_pred)
        roc_auc = auc(fpr, tpr)
        pr_auc = auc(rc, pr)
        cm = confusion_matrix(y_true, y_pred)
        tp = cm[0][0]  # TrueNegative
        fp = cm[0][1]  # FalseNegative
        fn = cm[1][0]  # FalsePositive
        tn = cm[1][1]  # TruePositive

        matx = {
            'Precision': round(precision, 2),
            'Recall': round(recall, 2),
            'Fscore': round(fscore, 2),
            'Accuracy': round(accuracy, 2),
            'ErrorRate': round(error_rate, 2),
            'ROC AUC': round(roc_auc, 2),
            'PR AUC': round(pr_auc, 2),
            'TrueNegative': round(tp, 2),
            'FalseNegative': round(fp, 2),
            'FalsePositive': round(fn, 2),
            'TruePositive': round(tn, 2)
        }

        return matx

    def get_predict_var(self):
        for key, value in self.metadata.items():
            if 'predict' in value and value['predict']:
                del self.metadata[key]['predict']
                return key

    def extract_metadata(self, x_train, y_train):
        if type(x_train) == pd.core.frame.DataFrame and type(y_train) == pd.core.series.Series:
            self.input_features = list(x_train.columns)
            self.predict = y_train.name
        else:
            print("Not a pandas DataFrame but a {}; fill metadata manually".format(
                type(y_train)))
            return
        metadata = {}
        number = ['int64', 'float64']
        for column in x_train.columns:
            if x_train[column].dtype in number:
                metadata[column] = {"type": "number"}
            if x_train[column].dtype == "object":
                enums = list(set(x_train[column].values.tolist()))
                metadata[column] = {"type": "category", "enum": enums}
        if y_train.dtype in number:
            metadata[self.predict] = {"type": "number"}
        if y_train.dtype == "object":
            enums = list(set(y_train.data.tolist()))
            metadata[self.predict] = {"type": "category", "enum": enums}
        self.metadata = metadata
        return metadata

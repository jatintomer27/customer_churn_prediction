"""
Data Transformation component responsible for preprocessing and transforming raw data
into a suitable format for model training and evaluation.
"""

import os
import pickle
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from customer_churn_prediction import logger
from customer_churn_prediction.entity.config_entity import DataTransformationConfig


class DataTransformation:
    """
    Handles preprocessing and transformation of data for model training.
    """
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def filter_dataset(self):
        """
        Filter the dataset columns based on the schema.
        """
        target_column = self.config.target_column.name
        relevant_columns = list(self.config.schema.keys())
        relevant_columns.append(target_column)
        data = pd.read_csv(self.config.local_data_file)
        final_data = data[relevant_columns]
        final_data.to_csv(self.config.filtered_data_file,index=False)
        logger.info(f"Selected only relevant columns based on the schema and stored in {self.config.filtered_data_file}")

    def drop_duplicates(self):
        """
        Check for the duplicate values in the dataset and remove if exist.
        """
        data = pd.read_csv(self.config.filtered_data_file)
        no_of_duplicates = data.duplicated().sum()
        if no_of_duplicates:
            data.drop_duplicates(inplace=True)
            logger.info(f"Remove the {no_of_duplicates} rows and final data stored in {self.config.filtered_data_file}")
        data.to_csv(self.config.filtered_data_file,index=False)

    def check_multicolinearity(self):
        """
        Check for check_multicolinearity in the dataset.
        """
        pass

    def categorical_column_encoder(self,encoding):
        """
        Encode the categorical columns based on the encoding type.
        """
        try:
            data = pd.read_csv(self.config.filtered_data_file)
            columns = self.config.schema.items()
            categorical_features = list(filter(lambda col: col[1] in ['str','object'],columns))
            logger.info(f"categorical_features {categorical_features}")
            encoders = {}
            for column, d_type in categorical_features:
                if encoding == 'label_encoding':
                    label_encoder = LabelEncoder()
                    data[column] = label_encoder.fit_transform(data[column])
                    encoders[column] = label_encoder

            if self.config.target_column.type in  ['str','object']:
                column = self.config.target_column.name
                label_encoder = LabelEncoder()
                data[column] = label_encoder.fit_transform(data[column])
                encoders[column] = label_encoder
            data.to_csv(self.config.encoded_data_file,index=False)
            with open(self.config.encoder_file,'wb') as f:
                pickle.dump(encoders,f)
        except Exception:
            logger.exception(f"Exception occured while encoding the categorical variables")
            raise
        
    def train_test_splitting(self):
        """
        Splits the preprocessed dataset into training and test sets 
        and saves them as CSV files.
        """
        data = pd.read_csv(self.config.encoded_data_file)
        train, test = train_test_split(
            data,
            test_size=self.config.params.test_size,
            random_state=self.config.params.random_state
        )
        train.to_csv(os.path.join(self.config.root_dir,"train.csv"),index=False)
        test.to_csv(os.path.join(self.config.root_dir,"test.csv"),index=False)
        logger.info("Splitted data into training and test set")
        logger.info(f"training data shape: {train.shape}")
        logger.info(f"test data shape: {test.shape}")

    def handle_inbalanced_data(self):
        """
        Handle class imbalance in the training dataset using SMOTE.
        """
        train_data = pd.read_csv(os.path.join(self.config.root_dir,"train.csv"))
        x_train = train_data.drop(columns=[self.config.target_column.name])
        y_train = train_data[self.config.target_column.name]
        smote = SMOTE(random_state=23)
        x_train_res, y_train_res = smote.fit_resample(x_train,y_train)
        train_resampled = pd.concat([x_train_res,y_train_res],axis=1)
        train_resampled.to_csv(os.path.join(self.config.root_dir,"train.csv"),index=False)
        logger.info("Applied SMOTE and saved resampled training data")

    def is_inbalanced(self, y, threshould=0.7):
        """
        Check whether the target variable is imbalanced based on a given threshold.
        """
        class_counts = y.value_counts(normalize=True)
        minimum_class_ratio = class_counts.min()
        return minimum_class_ratio < threshould
    
    def manage_inbalanced_data(self):
        """
        Check for class imbalance in the training data and apply SMOTE if necessary.
        """
        train_data = pd.read_csv(os.path.join(self.config.root_dir,"train.csv"))
        y_train = train_data[self.config.target_column.name]
        if self.is_inbalanced(y_train, self.config.params.data_transformation.smote_threshold):
            self.handle_inbalanced_data()
        else:
            logger.info("Data is already balanced")
            
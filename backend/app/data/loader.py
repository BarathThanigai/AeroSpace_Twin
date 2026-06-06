import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class GPSSpoofingDatasetLoader:
    """Load and process GPS Spoofing Detection dataset."""

    def __init__(self, dataset_path: Optional[str] = None):
        self.dataset_path = dataset_path
        self.data = None
        self.features = None
        self.labels = None

    def load_dataset(self, filepath: str) -> pd.DataFrame:
        """Load GPS spoofing dataset from CSV."""
        try:
            self.data = pd.read_csv(filepath)
            logger.info(f"Loaded dataset from {filepath}")
            logger.info(f"Dataset shape: {self.data.shape}")
            logger.info(f"Columns: {list(self.data.columns)}")
            return self.data
        except FileNotFoundError:
            logger.error(f"Dataset file not found: {filepath}")
            raise
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise

    def extract_features(self, feature_columns: Optional[list] = None) -> np.ndarray:
        """Extract features from dataset."""
        if self.data is None:
            raise ValueError("Dataset not loaded. Call load_dataset() first.")

        if feature_columns:
            self.features = self.data[feature_columns].values
        else:
            # Use all numeric columns except label column
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
            if "label" in numeric_cols:
                numeric_cols.remove("label")
            if "Class" in numeric_cols:
                numeric_cols.remove("Class")

            self.features = self.data[numeric_cols].values

        logger.info(f"Extracted features shape: {self.features.shape}")
        return self.features

    def extract_labels(self, label_column: str = "Class") -> np.ndarray:
        """Extract labels from dataset."""
        if self.data is None:
            raise ValueError("Dataset not loaded. Call load_dataset() first.")

        if label_column not in self.data.columns:
            # Try alternative label columns
            possible_labels = [col for col in self.data.columns if "label" in col.lower() or "class" in col.lower()]
            if possible_labels:
                label_column = possible_labels[0]
            else:
                logger.warning(f"Label column '{label_column}' not found")
                return None

        self.labels = self.data[label_column].values
        logger.info(f"Extracted labels: {np.unique(self.labels)}")
        return self.labels

    def get_normal_samples(self) -> np.ndarray:
        """Get only normal (non-spoofed) samples."""
        if self.data is None or self.labels is None:
            raise ValueError("Dataset or labels not loaded")

        # Assuming 0 or 'Normal' represents normal samples
        normal_mask = (self.labels == 0) | (self.labels == "Normal")
        normal_data = self.data[normal_mask]

        logger.info(f"Extracted {len(normal_data)} normal samples")
        return normal_data

    def preprocess(self) -> np.ndarray:
        """Preprocess dataset (handle missing values, normalization)."""
        if self.data is None:
            raise ValueError("Dataset not loaded")

        # Handle missing values
        self.data = self.data.fillna(self.data.mean())

        # Remove any remaining NaN
        self.data = self.data.dropna()

        logger.info(f"Preprocessed dataset shape: {self.data.shape}")
        return self.data


# Example usage
if __name__ == "__main__":
    # This would be used if GPS spoofing dataset becomes available
    loader = GPSSpoofingDatasetLoader()
    # loader.load_dataset("path/to/gps_spoofing_dataset.csv")
    # features = loader.extract_features()
    # labels = loader.extract_labels()
    print("GPS Spoofing Dataset Loader initialized")

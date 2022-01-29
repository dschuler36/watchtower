from sqlalchemy.orm import Session
from app.core.db_crud import get_agg_as_pdf
import pandas as pd
from pyod.models.knn import KNN


def knn_scan(dataset: str, db: Session):
    outlier_fraction = 0.1
    clf_name = 'KNN'

    agg_data = get_agg_as_pdf(db, dataset)
    # Take most recent record to test against
    x_test = pd.concat([agg_data.tail(1)])
    # Remove that record from training set
    x_train = agg_data[:-1]
    clf = KNN(contamination=outlier_fraction)
    clf.fit(x_train)

    # it is possible to get the prediction confidence as well
    y_test_pred, y_test_pred_confidence = clf.predict(x_test, return_confidence=True)
    print(y_test_pred)
    print(y_test_pred_confidence)

    if y_test_pred[0] == 0:
        return {f"not outlier. confidence: {y_test_pred_confidence}"}
    else:
        return {f"outlier. conficence: {y_test_pred_confidence}"}

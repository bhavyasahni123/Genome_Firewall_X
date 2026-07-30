from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    balanced_accuracy_score,
    matthews_corrcoef,
    cohen_kappa_score,
    confusion_matrix,
    log_loss,
    brier_score_loss,
)


def compute_metrics(
    y_true,
    y_pred,
    y_prob,
):

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
    ).ravel()

    specificity = tn / (tn + fp) if (tn + fp) else 0

    sensitivity = recall_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    return {

        "Accuracy":
            accuracy_score(y_true, y_pred),

        "Precision":
            precision_score(
                y_true,
                y_pred,
                zero_division=0,
            ),

        "Recall":
            sensitivity,

        "F1":
            f1_score(
                y_true,
                y_pred,
                zero_division=0,
            ),

        "ROC_AUC":
            roc_auc_score(
                y_true,
                y_prob,
            ),

        "Balanced_Accuracy":
            balanced_accuracy_score(
                y_true,
                y_pred,
            ),

        "Specificity":
            specificity,

        "Sensitivity":
            sensitivity,

        "MCC":
            matthews_corrcoef(
                y_true,
                y_pred,
            ),

        "Cohen_Kappa":
            cohen_kappa_score(
                y_true,
                y_pred,
            ),

        "LogLoss":
            log_loss(
                y_true,
                y_prob,
            ),

        "BrierScore":
            brier_score_loss(
                y_true,
                y_prob,
            ),

    }
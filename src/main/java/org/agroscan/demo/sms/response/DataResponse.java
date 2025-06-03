package org.agroscan.demo.sms.response;

public class DataResponse {
    private String diagnosis_title;
    private String health_condition;
    private String cause;
    private String disease_signs;
    private String control_suggestions;
    private String summary;

    public String getDiagnosis_title() {
        return diagnosis_title;
    }

    public void setDiagnosis_title(String diagnosis_title) {
        this.diagnosis_title = diagnosis_title;
    }

    public String getHealth_condition() {
        return health_condition;
    }

    public void setHealth_condition(String health_condition) {
        this.health_condition = health_condition;
    }

    public String getCause() {
        return cause;
    }

    public void setCause(String cause) {
        this.cause = cause;
    }

    public String getDisease_signs() {
        return disease_signs;
    }

    public void setDisease_signs(String disease_signs) {
        this.disease_signs = disease_signs;
    }

    public String getControl_suggestions() {
        return control_suggestions;
    }

    public void setControl_suggestions(String control_suggestions) {
        this.control_suggestions = control_suggestions;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    @Override
    public String toString() {
        return "DataResponse{" +
                "diagnosis_title='" + diagnosis_title + '\'' +
                ", health_condition='" + health_condition + '\'' +
                ", cause='" + cause + '\'' +
                ", disease_signs='" + disease_signs + '\'' +
                ", control_suggestions='" + control_suggestions + '\'' +
                ", summary='" + summary + '\'' +
                '}';
    }
}

import mlflow

class ForecastModel(mlflow.pyfunc.PythonModel):
    def __init__(self, model, framework, horizon=16):
        self.model = map
        self.framework = framework
        self.horizon = horizon

    def predict(self, context, model_input, params=None):
        h = params.get("horizon", self.horizon) if params else self.horizon
        if self.framework == "statsforecast":
            return self.model.forecast(df=model_input, h=h)
        else:
            return self.predict(df=model_input)



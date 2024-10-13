class StringConstants:
    LOGGER_APP_NAME = "ai-trade-insights"
    MICROSERVICE_NAME = "ai-trade-insights"

    @staticmethod
    def get_health_check_msg():
        return "pong"

    @staticmethod
    def get_logger_app_name():
        return StringConstants.LOGGER_APP_NAME

    @staticmethod
    def get_microservice_name():
        return StringConstants.MICROSERVICE_NAME

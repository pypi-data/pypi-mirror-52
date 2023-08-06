class RequestLoggerConfig:
    # constants
    DB_STORE = True
    REQUEST_LOGGER_DATA_STORE_URL = 'https://us-central1-ingaia-request-logger.cloudfunctions.net/save_request_log'

    # queue configuration
    REQUEST_LOG_QUEUE_NAME = 'requests-log-queue'
    REQUEST_LOG_QUEUE_URI = '/save-requests-log'

    @classmethod
    def enable_database_store(cls):
        cls.DB_STORE = True

    @classmethod
    def disable_database_store(cls):
        cls.DB_STORE = False


config = RequestLoggerConfig()

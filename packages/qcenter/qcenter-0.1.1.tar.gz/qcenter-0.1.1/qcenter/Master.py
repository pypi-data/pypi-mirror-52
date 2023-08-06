class Master:

    import configparser
    import requests
    import json
    import time
    import os
    import logging
    import logging.config


    cnf_fl = os.path.join(os.environ['Q_HOME'], 'config/qcenter.ini')

    log_fl = os.path.join(os.environ['Q_HOME'], 'config/logger.json')

    print(cnf_fl)
    print(log_fl)

    cnf_data = configparser.ConfigParser()
    cnf_data.read(cnf_fl)

    print(cnf_data['DRIVER']['HOST'])




    def setup_logging():

        """Setup logging configuration

        """
        if os.path.exists(log_fl):
            with open(log_fl, 'rt') as f:
                config = json.load(f)
                config['handlers']['file_handler']['filename'] = os.path.join(os.environ['Q_HOME'], 'logs/driver.log')
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=logging.INFO)

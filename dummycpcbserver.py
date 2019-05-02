from flask import Flask, request, jsonify
import json
app = Flask(__name__)


@app.route('/hello', methods = ['GET'])
def hello():
    if request.method == 'GET':
        app.logger.info('Dektos connection to CPCB successful')
        return """Dektos connection to CPCB successful"""


@app.route('/industry/<industryId>/station/<stationId>/data', methods = ['GET', 'POST'])
def uploadStationData(industryId, stationId):
    if request.method == 'GET':
        app.logger.warn('Please try POST method')
        return """Please try POST method"""
    
    elif request.method == 'POST':
        res = request.get_json(silent=True)
        app.logger.info('IndustryId: {}, StationId : {} '.format(industryId, stationId))
        app.logger.info(res)
        return jsonify(res)


if __name__ == '__main__':
    import logging
    from modbusInterface import configuration as CONF
    logName = CONF.LOG_PATH + 'CPCB_API.log'
    logFormatStr = '[%(asctime)s] %(levelname)s - %(message)s'
    logging.basicConfig(format = logFormatStr, filename = CONF.LOG_PATH +'dummyServerGlobal.log', level=logging.DEBUG)
    formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler(logName)
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)
    app.logger.addHandler(streamHandler)
    app.logger.info("Log restarted....")
    
    app.run(port='5000', debug=False)
    
    
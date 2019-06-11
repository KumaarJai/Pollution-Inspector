from flask import Flask, request
from flask import Response
import json
app = Flask(__name__)


def getSuccessResponse():
    return str(json.dumps({ "msg" : "success", "status" : 1 }))

@app.route('/hello', methods = ['GET'])
def hello():
    if request.method == 'GET':
        app.logger.info('Dektos connection to CPCB successful')
        return Response("""Dektos connection to CPCB successful""",200)


@app.route('/industry/<industryId>/station/<stationId>/data', methods = ['GET', 'POST'])
def uploadStationData(industryId, stationId):
    try:
        if request.method == 'GET':
            app.logger.warn('Please try POST method')
            return Response("""Bad Request: Please try POST method""", 400)
        
        elif request.method == 'POST':
            res = request.get_json(silent=True)
            app.logger.info('IndustryId: {}, StationId : {} '.format(industryId, stationId))
            app.logger.info(res)
            app.logger.info(getSuccessResponse())
            return Response(getSuccessResponse(), 200, content_type="application/json")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    
    from modbusInterface import dektosExternalPackageInstaller as DEKTOS_INSTALLER
    DEKTOS_INSTALLER.installPackage('Flask')
    
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
    app.logger.info("Dummy CPCB server Log restarted....")
    
    app.run(port='5000', debug=False)
    
    
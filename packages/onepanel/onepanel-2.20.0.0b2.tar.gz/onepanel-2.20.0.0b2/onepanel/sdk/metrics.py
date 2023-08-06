import json
import os

from websocket import create_connection


class Metrics:
    def __init__(self, account_uid=None, project_uid=None, job_uid=None):
        host = os.getenv('HOST', 'cluster-0-beta.onepanel.io')

        if account_uid is None:
            account_uid = os.getenv('ACCOUNT_UID')

        if project_uid is None:
            project_uid = os.getenv('PROJECT_UID')

        if job_uid is None:
            job_uid = os.getenv('JOB_UID')

        self._endpoint = 'wss://{}/{}/projects/{}/jobs/{}/metrics/:9999'.format(host, account_uid, project_uid, job_uid)

        self._ws = create_connection(self._endpoint)

    def close(self):
        self._ws.close()

    def put(self, x_name, x_value, y_name, y_value):
        self._ws.send(json.dumps({
            "x_axis": x_name,
            "x_value": x_value,
            "metric": y_name,
            "value": y_value
        }))


if __name__ == "__main__":
    m = Metrics("andreyonepanel", "edge-cases", "321")
    m.put("x", 1, "y", 1)
    m.close()
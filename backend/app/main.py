from app.dao.configDataManager import ConfigManager
from app.view.appView import AppView
from flask_cors import CORS  # 新增导入


def main(config_path):
    config_manager = ConfigManager(config_path)
    flask_app_view = AppView(config_manager)
    flask_app = flask_app_view.app  # 获取Flask实例

    CORS(flask_app)  # 添加CORS支持

    flask_config_model = config_manager.config.flask
    flask_app.run(
        host=flask_config_model.host,
        port=flask_config_model.port,
        debug=flask_config_model.debug
    )

import os
import json
import sqlite3
from alembic import command, config
from src.models import GPTModel
from src.repository import Repository
from src.lib import db_session
from src.common import Settings, Constants


class Bootstrap:

    def seed_models(self, session):
        billing_file = os.path.join(os.path.dirname(__file__), 'models.json')
        with open(billing_file, 'r') as f:
            billing = json.load(f)

        for model in billing:
            for type in model['types']:
                billing_repo = Repository(GPTModel, session)
                data = {
                    "display_name": model['display_name'],
                    "input_cost": type['input_cost'],
                    "output_cost": type.get('output_cost'),
                    "model": model['model'],
                    "model_type": type['type'],
                }
                billing_repo.upsert(keys=['model', 'model_type'], data=data)
                
    def init_db(self):
        conn = sqlite3.connect(Constants.DB_PATH)
        conn.close()
        try:
            alembic_cfg = config.Config(f"{Constants.BASE_DIR}/src/alembic.ini")
            command.upgrade(alembic_cfg, "head")
        except Exception as e:
            print(f"Unable to run migrations. Please run manually with alembic upgrade head and rerun. {e}")
            
            
    def run(self):
        self.init_db()
        with db_session() as session:
            self.seed_models(session)


if __name__ == '__main__':
    Bootstrap().run()



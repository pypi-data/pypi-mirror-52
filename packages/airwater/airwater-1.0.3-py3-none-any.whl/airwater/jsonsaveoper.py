import os
import arrow

class JsonSaveOperator:

    def __init__(self, spider_name, json_save_dir="."):
        self.json_save_dir = json_save_dir
        self.spider_name = spider_name

    def new_json_save_file(self):
        execution_time = arrow.utcnow().to("Asia/Shanghai").for_json()
        if not os.path.exists(self.json_save_dir):
            os.makedirs(self.json_save_dir)
        json_save_file = "{}/{}.".format(self.json_save_dir, self.spider_name) + str(execution_time) + ".json"
        return json_save_file

    @classmethod
    def filter_latest_json_save_file(cls):
        json_files = [os.path.join(cls.json_save_dir, jf) for jf in os.listdir(cls.json_save_dir)]
        json_files = [jf for jf in json_files if jf.find(".json") > 0 and os.path.isfile(jf)]

        # logger.info(json_files)
        json_files.sort(key=lambda x: arrow.get(x[x.find(".") + 1:x.rfind(".json")], tzinfo="Asia/Shanghai"), reverse=True)
        logger.info(json_files)
        for jf in json_files[3:]:
            os.remove(jf)

        return None if not len(json_files) else json_files[0]
